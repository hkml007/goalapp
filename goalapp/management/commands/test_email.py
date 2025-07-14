from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import traceback

class Command(BaseCommand):
    help = "Send a test email to confirm SMTP settings"

    def handle(self, *args, **kwargs):
        try:
            send_mail(
                subject='✅ Test Email',
                message='This is a test email from Django.',
                from_email='fathimashaji661@gmail.com',
                recipient_list=['hkml1431@gmail.com'],  # <-- Replace this
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS("✅ Test email sent successfully."))
        except Exception:
            self.stdout.write(self.style.ERROR("❌ Email failed. Traceback below:"))
            self.stdout.write(traceback.format_exc())
