from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email sending'

    def handle(self, *arts, **options):
        subject = 'Test email from Django'
        message = 'The is a test email sent from Django.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['noelle@ygitc.com']

        try:
            send_mail(subject, message, from_email, recipient_list)
            self.stdout.write(self.style.SUCCESS('Successfully sent test email'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send test email: {str(e)}'))
            