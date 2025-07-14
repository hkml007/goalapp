from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.core.mail import send_mail
from goalapp.models import Login, Milestone
from django.conf import settings

import logging

# Setup logging
logger = logging.getLogger(__name__)

def send_reminders_job():
    today = timezone.now().date()
    print(f"📅 Running reminder job at {timezone.now()}")
    logger.info(f"📅 Running reminder job at {timezone.now()}")

    for user in Login.objects.all():
        if not user.email:
            continue

        milestones = Milestone.objects.filter(
            goal__user=user,
            completed=False,
            deadline__gte=today
        )

        if not milestones.exists():
            continue

        subject = '⏰ Daily Goal Reminder'
        message = "Here are your upcoming or due milestones:\n\n"

        for m in milestones:
            days_left = (m.deadline - today).days
            urgency = "⚠️ URGENT! " if days_left == 0 else f"⏳ {days_left} day(s) left - "
            message += f"{urgency}{m.name} (Deadline: {m.deadline})\n"

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            print(f"✅ Email sent to {user.email}")
            logger.info(f"✅ Email sent to {user.email}")
        except Exception as e:
            print(f"❌ Failed to send email to {user.email}: {str(e)}")
            logger.error(f"❌ Failed to send email to {user.email}: {str(e)}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # 🕒 Daily at 8 AM
    scheduler.add_job(send_reminders_job, 'cron', hour=8, minute=0)
    
    # 🧪 TEST MODE: Uncomment to run every 30 seconds while developing
    # scheduler.add_job(send_reminders_job, 'interval', seconds=30)

    scheduler.start()
    print("✅ APScheduler started (daily 8 AM job)")
    logger.info("✅ APScheduler started (daily 8 AM job)")
