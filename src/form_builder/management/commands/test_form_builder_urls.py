from django.core.management.base import BaseCommand
from django.urls import reverse


class Command(BaseCommand):
    help = 'Test form builder URLs'

    def handle(self, *args, **options):
        try:
            list_forms_url = reverse('form_builder_list_forms')
            self.stdout.write(f"List forms URL: {list_forms_url}")
            
            upload_form_url = reverse('form_builder_upload_form')
            self.stdout.write(f"Upload form URL: {upload_form_url}")
            
            edit_form_url = reverse('form_builder_edit_form', kwargs={'form_id': 1})
            self.stdout.write(f"Edit form URL: {edit_form_url}")
            
            delete_form_url = reverse('form_builder_delete_form', kwargs={'form_id': 1})
            self.stdout.write(f"Delete form URL: {delete_form_url}")
            
            download_form_url = reverse('form_builder_download_form', kwargs={'form_id': 1})
            self.stdout.write(f"Download form URL: {download_form_url}")
            
            render_form_url = reverse('form_builder_render_form', kwargs={'form_id': 1})
            self.stdout.write(f"Render form URL: {render_form_url}")
            
            self.stdout.write(self.style.SUCCESS('All URLs are working correctly!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))