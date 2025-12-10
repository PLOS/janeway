import re

from collections.abc import Iterable
from email.utils import parseaddr

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import sanitize_address
from django.utils.encoding import force_str
from django.utils.html import strip_tags

from journal.models import Journal
from utils import setting_handler
from utils import notify
from utils.logger import get_logger

logger = get_logger(__name__)

SANITIZE_FROM_RE = re.compile('\r|\n|\t|"|<|>|,')


def sanitize_from(from_):
    return re.sub(SANITIZE_FROM_RE, "", from_)


def get_attr_or_key(source, key, default=None, call_method=False):
    """
    Safely get `key` from `source`, handling both dicts and objects.

    Args:
        source: Dictionary or object to extract value from
        key: Key (dict) or attribute name (object) to retrieve
        default: Value to return if key/attribute not found
        call_method: If True and value is callable, invoke it

    Returns:
        The value associated with key, or default if not found

    Examples:
        >>> get_attr_or_key({"name": "John"}, "name")
        'John'
        >>> get_attr_or_key(user, "email")
        'user@example.com'
        >>> get_attr_or_key(user, "full_name", call_method=True)
        'John Doe'
    """
    if isinstance(source, dict):
        value = source.get(key, default)
    else:
        value = getattr(source, key, default)

    if call_method and callable(value):
        return value()
    return value


def get_journal_from_request(request):
    """
    Extract and reconstruct Journal from request (HttpRequest or dict).
    Returns Journal instance or None.
    """
    if not request:
        return None

    journal_data = get_attr_or_key(request, "journal")

    if not journal_data:
        return None

    # If it's already a Journal instance, use it
    if isinstance(journal_data, Journal):
        return journal_data

    # If it's a dict with a code, fetch the Journal
    if isinstance(journal_data, dict):
        code = journal_data.get("code")
        if code:
            try:
                return Journal.objects.get(code=code)
            except Journal.DoesNotExist:
                logger.warning(f"Journal with code '{code}' not found")

    return None


def send_email(
    subject,
    to,
    html,
    journal,
    request,
    bcc=None,
    cc=None,
    attachment=None,
    replyto=None,
):
    repository = get_attr_or_key(request, "repository")
    press = get_attr_or_key(request, "press")
    main_contact = get_attr_or_key(press, "main_contact")

    if journal:
        from_email = setting_handler.get_setting(
            "general", "from_address", journal
        ).value
        html = "{0}<br />{1}".format(html, journal.name)
    elif repository:
        # fetches the default setting for this email.
        subject = setting_handler.get_email_subject_setting(
            "email_subject", subject, journal=None
        )
        from_email = main_contact
    else:
        from_email = main_contact

    if isinstance(to, str):
        if settings.DUMMY_EMAIL_DOMAIN in to:
            to = []
        else:
            to = [to]
    elif isinstance(to, Iterable):
        to = [email for email in to if not settings.DUMMY_EMAIL_DOMAIN in email]

    user = get_attr_or_key(request, "user")
    user_is_anonymous = get_attr_or_key(user, "is_anonymous")
    user_email = get_attr_or_key(user, "email")

    # Handle user_full_name because in serialized requests it's a string,
    # in the HttpRequest, it's a method that needs to be called
    if isinstance(user, dict):
        user_full_name = user.get("full_name", "")
    else:
        user_full_name = user.full_name() if user and hasattr(user, "full_name") else ""

    if (
        request
        and user
        and not user_is_anonymous
        and user_email
        and user_email not in to
    ):
        reply_to = [user_email]
        full_from_string = '"{0}" <{1}>'.format(
            sanitize_from(user_full_name),
            from_email,
        )
    else:
        reply_to = []
        if request:
            site_type = get_attr_or_key(request, "site_type")

            # Handle site_type which might not exist in serialized request
            if site_type:
                name = get_attr_or_key(site_type, "name")
                if name:
                    full_from_string = '"{0}" <{1}>'.format(
                        sanitize_from(name), from_email
                    )
                else:
                    full_from_string = from_email
            else:
                full_from_string = from_email
        else:
            full_from_string = from_email

    # handle django 3.2 raising an exception when invalid characters are found
    # during sanitization (call ported from Django 1.11)
    full_from_string = parseaddr(force_str(full_from_string))
    # As per #3545, not all backends sanitize from string before .send()
    full_from_string = sanitize_address(
        full_from_string,
        settings.DEFAULT_CHARSET,
    )

    # if a replyto is passed to this function, use that.
    if replyto:
        reply_to = replyto

    # if there is no reply_to set yet, check if the journal has a custom
    # replyto_address and use that.
    if not reply_to:
        custom_reply_to = setting_handler.get_setting(
            "general",
            "replyto_address",
            journal,
        ).value
        if custom_reply_to:
            reply_to = (custom_reply_to,)

    # reply_to must always be a tuple or list.
    if reply_to and not isinstance(reply_to, (tuple, list)):
        reply_to = [reply_to]

    kwargs = dict(
        bcc=bcc,
        cc=cc,
    )
    if reply_to:
        # Avoid empty mailboxes for servers not compliant with RFC 5322
        kwargs["reply_to"] = reply_to

    msg = EmailMultiAlternatives(
        subject, strip_tags(html), full_from_string, to, **kwargs
    )
    msg.attach_alternative(html, "text/html")

    if attachment:
        for file_ in attachment:
            file_.open()
            msg.attach(file_.name, file_.read(), file_.content_type)
            file_.close()

    elif request:
        # FILES aren't JSON-serializable, so the files are only attached for HttpRequest objects
        # TODO: If attached files are required, we'd likely need to retrieve them from a file storage (filesystem, S3, etc.)
        files = get_attr_or_key(request, "FILES")
        if files and hasattr(files, "getlist"):
            file_list = files.getlist("attachment")
            if file_list:
                for file in file_list:
                    file.open()
                    msg.attach(file.name, file.read(), file.content_type)
                    file.close()
    return msg.send()


def notify_hook(**kwargs):
    # dummy mock-up of new notification hook defer

    # action is a list of notification targets
    # if the "all" variable is passed, then some types of notification might act, like Slack.
    # Email, though, should only send if it's specifically an email in action, not on "all".
    action = kwargs.pop("action", [])

    if "email" not in action:
        # email is only sent if list of actions includes "email"
        return

    # pop the args
    subject = kwargs.pop("subject", "")
    to = kwargs.pop("to", "")
    html = kwargs.pop("html", "")
    bcc = kwargs.pop("bcc", [])
    cc = kwargs.pop("cc", [])
    attachment = kwargs.pop("attachment", None)
    request = kwargs.pop("request", None)
    task = kwargs.pop("task", None)
    custom_reply_to = kwargs.pop("custom_reply_to", None)

    if request:
        journal = get_journal_from_request(request)
        subject_setting_value = setting_handler.get_email_subject_setting(
            "email_subject", subject, journal
        )
        if journal:
            subject = f"[{journal.code}] {subject_setting_value}"
        else:
            subject = subject_setting_value

    # call the method
    if not task:
        response = send_email(
            subject,
            to,
            html,
            journal,
            request,
            bcc,
            cc,
            attachment,
            replyto=custom_reply_to,
        )
    else:
        response = send_email(
            task.email_subject,
            task.email_to,
            task.email_html,
            task.email_journal,
            request,
            task.email_bcc,
            task.email_cc,
            replyto=custom_reply_to,
        )

    log_dict = kwargs.get("log_dict", None)

    if not type(to) in [list, tuple, set]:
        to = [to]

    if log_dict:
        notify_contents = {
            "log_dict": log_dict,
            "request": request,
            "response": response,
            "action": ["email_log"],
            "html": html,
            "to": to,
            "email_subject": subject,
            "cc": cc,
            "bcc": bcc,
        }
        notify.notification(**notify_contents)


def plugin_loaded():
    pass
