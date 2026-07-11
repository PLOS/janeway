__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

from django.urls import re_path

from form_builder import views

urlpatterns = [
    # List forms view
    re_path(r"^$", views.list_forms, name="form_builder_list_forms"),
    # Upload form view
    re_path(r"^form/upload/$", views.upload_form, name="form_builder_upload_form"),
    # Edit form view
    re_path(
        r"^form/(?P<form_id>[0-9a-zA-Z-]+)/edit/$",
        views.edit_form,
        name="form_builder_edit_form",
    ),
    # Delete form view
    re_path(
        r"^form/(?P<form_id>[0-9a-zA-Z-]+)/delete/$",
        views.delete_form,
        name="form_builder_delete_form",
    ),
    # Download form as JSON view
    re_path(
        r"^form/(?P<form_id>[0-9a-zA-Z-]+)/download/$",
        views.download_form,
        name="form_builder_download_form",
    ),
    # Render form view
    re_path(
        r"^form/(?P<form_id>[0-9a-zA-Z-]+)/render/$",
        views.render_form,
        name="form_builder_render_form",
    ),
]
