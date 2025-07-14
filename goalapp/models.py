from django.db import models
from django.core.validators import *
from django.utils import timezone
import calendar
from datetime import date
from django.contrib.postgres.fields import JSONField
from django.db.models import Count, Sum, Avg
from mptt.models import MPTTModel, TreeForeignKey
from datetime import timedelta


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100)
    age = models.IntegerField()
    contact_no = models.CharField(max_length=15)
    login_id = models.ForeignKey('Login', on_delete=models.CASCADE)
   

class Login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # store hashed
    user_type = models.CharField(max_length=100)
    
    
    @property
    def username(self):
        user = User.objects.filter(login_id=self).first()
        return user.username if user else "Unknown"
        
    
    

class Goal(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    deadline = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)  # Track completion date
    days_spent = models.IntegerField(null=True, blank=True)


    def save(self, *args, **kwargs):
        # If the goal is marked as completed and wasn't previously completed
        if self.completed and self.completed_date is None:
            self.completed_date = timezone.now().date()  # Set to current date (May 23, 2025)
        # If the goal is marked as not completed, reset completed_date and days_spent
        elif not self.completed:
            self.completed_date = None
            self.days_spent = None
        # Calculate days_spent if completed and both dates are available
        if self.completed and self.completed_date and self.start_date:
            days = (self.completed_date - self.start_date).days
            self.days_spent = max(1, days)  # Ensure at least 1 day
        super().save(*args, **kwargs)


    def completion_rate(self):
        """Calculate the percentage of milestones completed for this goal."""
        total_milestones = self.milestones.count()
        if total_milestones == 0:
            return 0
        completed_milestones = self.milestones.filter(completed=True).count()
        return (completed_milestones / total_milestones) * 100 if total_milestones > 0 else 0

    @classmethod
    def get_analytics(cls, user, year):
        """Return aggregated analytics for the user's goals in a given year."""
        goals = cls.objects.filter(user=user, start_date__year=year)
        total_goals = goals.count()
        completed_goals = goals.filter(completed=True).count()
        completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0
        avg_days_spent = goals.filter(completed=True).aggregate(avg_days=Avg('days_spent'))['avg_days'] or 0
        total_milestones = Milestone.objects.filter(goal__in=goals).count()
        completed_milestones = Milestone.objects.filter(goal__in=goals, completed=True).count()
        milestone_completion_rate = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
    
    
        return {
            'total_goals': total_goals,
            'completed_goals': completed_goals,
            'completion_rate': round(completion_rate, 2),
            'avg_days_spent': round(avg_days_spent, 2) if avg_days_spent else 0,
            'total_milestones': total_milestones,
            'completed_milestones': completed_milestones,
            'milestone_completion_rate': round(milestone_completion_rate, 2),
        }    
    @classmethod
    def get_pending_goals_for_today(cls, user):
        today = timezone.now().date()
        return cls.objects.filter(
            user=user,
            completed=False,
            deadline__isnull=False,
            deadline__gte=today
        )


 
class Milestone(models.Model):
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=255)
    progress = models.TextField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    missed = models.BooleanField(default=False)
    @classmethod
    def get_pending_milestone_for_today(cls, user):
        today = timezone.now().date()
        return cls.objects.filter(
            goal__user=user,
            completed=False,
            deadline=today
        )


     
class Todo(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE)
    date = models.DateField()
    task = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    @classmethod
    def get_pending_todo_for_today(cls, user):
        today = timezone.now().date()
        return cls.objects.filter(
            user=user,
            completed=False,
            date=today
        )

    

class Notification(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE,related_name='notifications',null=True, blank=True)
    notification = models.TextField(default="")
    current_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} at {self.current_date.strftime('%Y-%m-%d %H:%M')}"  




class Habit(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    month = models.IntegerField(default=1)
    year = models.IntegerField(default=2025)
    
class HabitTick(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    day = models.IntegerField()
    month = models.IntegerField(default=1)
    year = models.IntegerField(default=2025)
    checked = models.BooleanField(default=False)


  
class DiaryEntry(models.Model):
    ENTRY_TYPE_CHOICES = [('text', 'Text'), ('audio', 'Audio'), ('video', 'Video')]
    
    user = models.ForeignKey('Login', on_delete=models.CASCADE)  # Link to Login
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    content = models.TextField(blank=True, null=True)  # For text or file paths
    date = models.DateField(auto_now_add=True)          # Auto-set date
    time = models.TimeField(auto_now_add=True)          # Auto-set time
    file = models.FileField(upload_to='diary_media/', blank=True, null=True)  # For audio/video
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.entry_type} entry by {self.user.email}"
    

class DiaryPhoto(models.Model):
    diary_entry = models.ForeignKey(DiaryEntry, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='diary_photos/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Photo for {self.diary_entry.id}"

 

class DailyReminder(models.Model):
    user           = models.OneToOneField('Login', on_delete=models.CASCADE)
    enabled        = models.BooleanField(default=False)
    reminder_time  = models.TimeField(default='21:00')


class Challenge(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='challenges')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def can_edit(self, user):
        return self.user == user

class ChallengeProgress(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='progress')
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    progress = models.TextField(blank=True, null=True)  # User can update progress
    joined_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    streak = models.IntegerField(default=0)

    class Meta:
        unique_together = ('challenge', 'user')  # Prevent duplicate joins

    def __str__(self):
        return f"{self.user.email} - {self.challenge.title}"

class ChallengeUpdate(models.Model):
    challenge_progress = models.ForeignKey(ChallengeProgress, on_delete=models.CASCADE, related_name='updates')
    text = models.TextField(blank=True)
    photo = models.ImageField(upload_to='challenge_updates/%Y/%m/%d/', blank=True, null=True)
    video = models.FileField(upload_to='challenge_updates/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_date = models.DateField(default=timezone.now)
    reported = models.BooleanField(default=False)

    def __str__(self):
        return f"Update by {self.challenge_progress.user.username} on {self.update_date}"

class Like(models.Model):
    update = models.ForeignKey(ChallengeUpdate, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('update', 'user')

    def __str__(self):
        return f"{self.user.username} likes update {self.update.id}"

class Comment(MPTTModel):
    update = models.ForeignKey(ChallengeUpdate, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reported = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Comment by {self.user.username} on update {self.update.id}"

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"
    

class DailyCheck(models.Model):
    login_id = models.ForeignKey('Login', on_delete=models.CASCADE)
    last_checkin = models.DateField(default=timezone.now)
    streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_streak_update = models.DateField(default=timezone.now)

    def update_streak(self):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        # Update streak
        if self.last_checkin == yesterday:
            self.streak += 1
        elif self.last_checkin < yesterday:
            self.streak = 1  # Reset streak if a day was missed

        self.longest_streak = max(self.streak, self.longest_streak)
        self.last_checkin = today
        self.last_streak_update = today
        self.save()

    def get_checkin_history(self, days=7):
        today = timezone.now().date()
        history = []
        for i in range(days - 1, -1, -1):
            date = today - timedelta(days=i)
            checked_in = DailyCheck.objects.filter(
                login_id=self.login_id,
                last_checkin=date
            ).exists()
            history.append({'date': date, 'checked_in': checked_in})
        return history 
    

class MBTIProfile(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    mbti_type = models.CharField(max_length=4)
    date_taken = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.session_key} – {self.mbti_type} on {self.date_taken.strftime('%Y-%m-%d %H:%M')}"

class MBTIExplanation(models.Model):
    type_code = models.CharField(max_length=4, unique=True)  # e.g., INFP
    description = models.TextField()  # Short insight
    explanation = models.TextField()  # Deep dive
    growth_tips = models.JSONField(default=list)  # List of tips
    matches = models.TextField(blank=True, default="")  # Best matches

    def __str__(self):
        return self.type_code


class DismissedNotification(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='dismissed_notifications')
    notification_id = models.CharField(max_length=50)  # e.g., 'goal_1', 'milestone_2'
    dismissed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'notification_id')
    
    def __str__(self):
        return f"{self.user.email} dismissed {self.notification_id}"    
    


def generate_ai_insight_for_user(login_user):
    goals = Goal.objects.filter(user=login_user)
    
    if not goals.exists():
        return None

    for goal in goals:
        total_milestones = goal.milestones.count()
        completed_milestones = goal.milestones.filter(completed=True).count()
        milestone_accuracy = (completed_milestones / total_milestones) * 100 if total_milestones > 0 else 0

        days_spent = (goal.completed_date - goal.start_date).days if goal.completed and goal.completed_date else None

        # Construct insight texts based on performance
        if milestone_accuracy >= 80 and goal.completed:
            feedback = f"You successfully completed '{goal.title}' with high milestone accuracy ({milestone_accuracy:.0f}%)."
            motivation = "Outstanding job! You're on track to achieve even greater goals."
            strategy = "Continue your consistent approach and consider mentoring others."
            score = 95
        elif 50 <= milestone_accuracy < 80:
            feedback = f"'{goal.title}' shows moderate milestone completion at {milestone_accuracy:.0f}%."
            motivation = "You're progressing, but a tighter focus could elevate your performance."
            strategy = "Break larger milestones into smaller, trackable tasks."
            score = 70
        else:
            feedback = f"'{goal.title}' reflects a low milestone completion rate ({milestone_accuracy:.0f}%)."
            motivation = "Don't be discouraged. Every failure is a step toward success."
            strategy = "Re-evaluate your goal structure and set weekly targets."
            score = 40

        # Save or update AIInsight
        AIInsight.objects.create(
            user=login_user,
            goal=goal,
            feedback_summary=feedback,
            motivational_message=motivation,
            strategy_suggestion=strategy,
            performance_score=score,
            milestone_accuracy=milestone_accuracy,
            reviewed=False
        )
class AIInsight(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE)
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE, null=True, blank=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    
    feedback_summary = models.TextField(help_text="Personalized analysis or insight")
    motivational_message = models.TextField(help_text="Tailored motivational prompt")
    strategy_suggestion = models.TextField(help_text="Recommended strategy for overcoming roadblocks")
    performance_score = models.FloatField(default=0.0, help_text="Numeric performance metric (0-100)")
    milestone_accuracy = models.FloatField(default=0.0, help_text="Milestone completion rate")
    
    reviewed = models.BooleanField(default=False, help_text="Whether user has seen this insight")

    class Meta:
        ordering = ['-generated_on']

    def __str__(self):
        return f"AI Insight for {self.user.email} on {self.generated_on.strftime('%Y-%m-%d')}"
