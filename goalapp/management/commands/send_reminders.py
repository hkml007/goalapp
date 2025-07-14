from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from goalapp.models import Milestone, Login
from django.conf import settings
import traceback

class Command(BaseCommand):
    help = 'Send daily milestone reminder emails'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        self.stdout.write(self.style.NOTICE(f"📅 Today is {today}"))

        login_users = Login.objects.all()
        self.stdout.write(self.style.NOTICE(f"👥 Total Login users: {login_users.count()}"))

        for login_user in login_users:
            self.stdout.write(f"👤 Processing: {login_user.email}")

            if not login_user.email:
                self.stdout.write(self.style.WARNING(f"⚠️ Skipping user with no email"))
                continue

            # Fetch all milestones linked to this login user through their goals
            milestones = Milestone.objects.filter(
                goal__user=login_user,
                completed=False,
                deadline__gte=today
            )

            self.stdout.write(f"📌 Found {milestones.count()} upcoming/incomplete milestone(s)")

            if not milestones.exists():
                self.stdout.write(f"ℹ️ No milestones to email for {login_user.email}")
                continue

            # Build the email content
            subject = '⏰ Daily Goal Reminder'
            message = "Here are your upcoming or due milestones:\n\n"

            for m in milestones:
                days_left = (m.deadline - today).days
                urgency = (
                    "⚠️ URGENT! " if days_left == 0 else
                    f"⏳ {days_left} day(s) left - "
                )
                message += f"{urgency}{m.name} (Deadline: {m.deadline})\n"

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [login_user.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Reminder email sent to {login_user.email}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Failed to send email to {login_user.email}: {str(e)}"))
                self.stdout.write(traceback.format_exc())

        self.stdout.write(self.style.SUCCESS('✅ Reminder emails processed!'))
