import traceback
import uuid
from django.shortcuts import *
from .forms import *
from .models import *
from django.contrib import messages
from datetime import *
from datetime import date
from django.utils import timezone
import calendar as cal
from django.http import JsonResponse
from django.urls import reverse
from django.db import transaction
from collections import Counter, defaultdict
from django.http import HttpResponseBadRequest
import json
from django.db.models import Prefetch
from django.utils.timezone import now
from django.core.mail import send_mail
from django.db.models import Count,Q
from django.contrib.auth.hashers import check_password
import os
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.timezone import localtime, now
from django.urls import reverse
from datetime import date
from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime, time, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, datetime
from .models import Goal, Milestone, Todo, Habit, HabitTick, Login, DismissedNotification
from django.urls import reverse
from django.middleware.csrf import get_token
from .forms import MBTIForm, MBTI_QUESTIONS
from .models import MBTIExplanation





# Create your views here.
def calendar(request):
    return render(request,'calendar.html')

def calendar_view(request):
    return render(request, 'calendar_view.html')  # Include JS calendar here

def admin(request):
    return render(request,'admin.html')

from django.contrib import messages
from .models import Login
from django.shortcuts import render, redirect

# def logins(request):
#     if request.method=='POST':
#         form=LoginCheck(request.POST)
#         if form.is_valid():
#             email=form.cleaned_data['email']
#             password=form.cleaned_data['password']

#             try:
#                 user=Login.objects.get(email=email)

#                 if user.password==password:
#                     request.session['user_id']=user.id
#                     request.session['email']=user.email
#                     return redirect('user_home')
#                 else:
#                     messages.error(request,'Invalid username/email or password')
#             except User.DoesNotExist:
#                 messages.error(request,'User does not exist')
#     else:
#         form=LoginCheck()
#     return render(request,'login.html',{'form':form})
def logins(request):
    if request.method == 'POST':
        form = LoginCheck(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if email == 'admin@example.com' and password == 'admin123':
                    request.session['admin'] = '1'
                    return redirect('admin_user')
            else:
                messages.error(request,'Invalid credentials',extra_tags='supress')
    else:
        form = LoginCheck()   

    if request.method == 'POST':
        form = LoginCheck(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
                
            try:
                user = Login.objects.get(email=email)

                if user.password == password:
                    request.session['user_id'] = user.id
                    request.session['email'] = user.email

                    # Get pending goals and store in session or context
                    from .models import Goal  # Import inside function to avoid circular import
                    pending_goals = Goal.get_pending_goals_for_today(user)

                    # Store in session or pass via redirect (session used here for simplicity)
                    request.session['pending_goal_count'] = pending_goals.count()

                    return redirect('user_home')
                else:
                    messages.error(request, 'Invalid username/email or password')
            except Login.DoesNotExist:
                messages.error(request, 'User does not exist')
                
    else:
        form = LoginCheck()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    request.session.flush()  # clear all session data
    return redirect('logins')  # or redirect to your login page URL name
 
    
    
def users(request):
    if 'user_id' in request.session:
        return render(request,'user.html')
    else:
        return redirect('logins')
from .models import Goal, Login  # Ensure this import is at the top
from django.utils import timezone

# def users(request):
#     if 'user_id' in request.session:
#         user_id = request.session['user_id']
#         user = Login.objects.get(id=user_id)

#         # Get pending goals for today
#         pending_goals = Goal.get_pending_goals_for_today(user)
#         print(pending_goals)

#         return render(request, 'user.html', {
#             'pending_goals': pending_goals
#         })
#     else:
#         return redirect('logins')


def admin_user(request):
    if not request.session.get('admin'):
        return redirect('logins')
    c=User.objects.all()
    return render(request,'admin_user.html',{'c':c})

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        form1 = LoginForm(request.POST)
        if form.is_valid() and form1.is_valid():
            a = form1.save(commit=False)
            a.user_type = "user"
            a.save()
            b = form.save(commit=False)
            # Calculate age from date of birth
            dob = form.cleaned_data['date_of_birth']
            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            b.age = age
            b.login_id = a
            b.save()
            return redirect('register')
    else:
        form = UserForm()
        form1 = LoginForm()
    return render(request, 'register.html', {'form': form, 'form1': form1})
          
# your_app/views.py (replace or update relevant views)



from datetime import date, timedelta, datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.middleware.csrf import get_token
from .models import Login, Goal, Milestone, Todo, Habit, HabitTick, DismissedNotification

def user_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('logins')
    else:
        try:
            user = Login.objects.get(id=user_id)
        except Login.DoesNotExist:
            return redirect('logins')

        today = date.today()
        tomorrow = today + timedelta(days=1)
        habit_tracker_url = reverse('habit_tracker', args=[today.year, today.month])
        notifications = []

        # === GOALS ===
        # Overdue or Due Today
        pending_goals = Goal.objects.filter(user=user, completed=False, deadline__lte=today)
        for goal in pending_goals:
            days_overdue = (today - goal.deadline).days if goal.deadline else 0
            message = f"Goal '{goal.title}' is {'due today' if days_overdue == 0 else f'overdue by {days_overdue} day(s)'}. Please review or update."
            notifications.append({
                'id': f'goal_{goal.id}',
                'type': 'goal',
                'message': message,
                'date': goal.deadline.isoformat(),
                'link': reverse('goal_tracker')
            })

        # Upcoming Goals
        upcoming_goals = Goal.objects.filter(user=user, completed=False, deadline__gt=today)
        for goal in upcoming_goals:
            message = f"Goal '{goal.title}' is due on {goal.deadline.strftime('%B %d, %Y')}. Keep progressing!"
            notifications.append({
                'id': f'upcoming_goal_{goal.id}',
                'type': 'upcoming_goal',
                'message': message,
                'date': goal.deadline.isoformat(),
                'link': reverse('goal_tracker')
            })

        # Overdue or Due Today
        pending_milestones = Milestone.objects.filter(goal__user=user, completed=False, deadline__lte=today)
        for milestone in pending_milestones:
            days_overdue = (today - milestone.deadline).days if milestone.deadline else 0
            status_message = 'due today' if days_overdue == 0 else f'overdue by {days_overdue} day(s)'
            message = f"Milestone '{milestone.name}' for goal '{milestone.goal.title}' is {status_message}. {'It has been marked as missed.' if milestone.missed else 'Take action to complete it!'}"
            notifications.append({
                'id': f'milestone_{milestone.id}',
                'type': 'milestone',
                'message': message,
                'date': milestone.deadline.isoformat(),
                'link': reverse('goal_tracker')
            })

        # Upcoming Milestones
        upcoming_milestones = Milestone.objects.filter(goal__user=user, completed=False, deadline__gt=today)
        for milestone in upcoming_milestones:
            message = f"Milestone '{milestone.name}' for goal '{milestone.goal.title}' is due on {milestone.deadline.strftime('%B %d, %Y')}."
            notifications.append({
                'id': f'upcoming_milestone_{milestone.id}',
                'type': 'upcoming_milestone',
                'message': message,
                'date': milestone.deadline.isoformat(),
                'link': reverse('goal_tracker')
            })

        # === TO-DOS ===
        # Due Today
        pending_todos = Todo.objects.filter(user=user, completed=False, date=today)
        for todo in pending_todos:
            message = f"You have a task due today: '{todo.task[:50]}...'"
            notifications.append({
                'id': f'todo_{todo.id}',
                'type': 'todo',
                'message': message,
                'date': today.isoformat(),
                'link': reverse('todo_list_date', args=[today.year, today.month, today.day])
            })

        # Upcoming To-Dos
        upcoming_todos = Todo.objects.filter(user=user, completed=False, date__gte=today)
        for todo in upcoming_todos:
            message = f"Upcoming task: '{todo.task[:50]}...' due on {todo.date.strftime('%B %d, %Y')}."
            notifications.append({
                'id': f'upcoming_todo_{todo.id}',
                'type': 'upcoming_todo',
                'message': message,
                'date': todo.date.isoformat(),
                'link': reverse('todo_list_date', args=[todo.date.year, todo.date.month, todo.date.day])
            })

        # === HABITS ===
        for check_day in [today, tomorrow]:
            habits = Habit.objects.filter(user=user, year=check_day.year, month=check_day.month)
            if habits.exists():
                habit_ids = habits.values_list('id', flat=True)
                checked_ids = HabitTick.objects.filter(
                    habit_id__in=habit_ids,
                    day=check_day.day,
                    month=check_day.month,
                    year=check_day.year,
                    checked=True
                ).values_list('habit_id', flat=True)
                pending_habits = habits.exclude(id__in=checked_ids)
                if pending_habits.exists() and today in [check_day, check_day - timedelta(days=1)]:
                    notifications.append({
                        'id': f'habit_{check_day.isoformat()}',
                        'type': 'habit',
                        'message': f"You have pending habits to check for {check_day.strftime('%B %d, %Y')}. Stay on track!",
                        'date': check_day.isoformat(),
                        'link': reverse('habit_tracker', args=[check_day.year, check_day.month])
                    })

        # === FILTER OUT DISMISSED ===
        dismissed_ids = DismissedNotification.objects.filter(user=user).values_list('notification_id', flat=True)
        notifications = [n for n in notifications if n['id'] not in dismissed_ids]

        # === SORT ===
        notifications.sort(key=lambda x: (
            x['type'] != 'habit',
            x['date'] == today.isoformat(),
            -(today - datetime.fromisoformat(x['date']).date()).days
        ))

        context = {
            'habit_tracker_url': habit_tracker_url,
            'notifications': notifications,
            'today': today,
            'email': request.session.get('email', 'User'),
            'csrf_token': get_token(request),
        }

        return render(request, 'user_home.html', context)

    # return redirect('logins')

def dismiss_notification(request):
    if 'user_id' in request.session:
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            notification_id = request.POST.get('notification_id')
            if not notification_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid notification ID'})

            user = get_object_or_404(Login, id=request.session.get('user_id'))
            DismissedNotification.objects.get_or_create(user=user, notification_id=notification_id)
            return JsonResponse({'status': 'success', 'message': 'Notification dismissed'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    else:
        return redirect('logins')   


def edit_userprofile(request):
    if 'user_id' in request.session:
        id=request.session.get('user_id')
    
        user=get_object_or_404(Login,id=id)
        user_data=get_object_or_404(User,login_id=user)
        login_data=get_object_or_404(Login,id=user.id)
        if request.method=='POST':
            form=UserForm(request.POST,instance=user_data)
            form1=EmailForm(request.POST,instance=login_data)
            if form.is_valid() and form1.is_valid():
                form.save()
                form1.save()
                return redirect('user_home')
        else: 
            form=UserForm(instance=user_data)
            form1=EmailForm(instance=login_data)
            return render(request,'edit_userprofile.html',{'form':form,'form1':form1})
    else:
        return redirect('logins')    
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Goal, Milestone, Login
from django.utils import timezone

from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Goal, Milestone, Login

def goal_tracker(request):
    if 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            print("Session user_id:", user_id)
            print("User exists:", Login.objects.filter(id=user_id).exists())

            try:
                user = Login.objects.get(id=user_id)
            except Login.DoesNotExist:
                return redirect('logins')

            current_year = date.today().year
            year = request.GET.get('year', current_year)

            try:
                year = int(year)
            except ValueError:
                year = current_year

            goals = Goal.objects.filter(user=user, start_date__year=year).prefetch_related('milestones')
            analytics = Goal.get_analytics(user, year)

            if request.method == 'POST':
                if 'delete_goal' in request.POST:
                    goal_id = request.POST.get('delete_goal')
                    Goal.objects.filter(id=goal_id, user=user).delete()
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'status': 'success',
                            'analytics': Goal.get_analytics(user, year),
                            'message': 'Goal deleted successfully.'
                        })
                    return redirect('goal_tracker')

                if 'delete_milestone' in request.POST:
                    milestone_id = request.POST.get('delete_milestone')
                    Milestone.objects.filter(id=milestone_id, goal__user=user).delete()
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'status': 'success',
                            'analytics': Goal.get_analytics(user, year),
                            'message': 'Milestone deleted successfully.'
                        })
                    return redirect('goal_tracker')

                today = date.today()
                reminder_window_start = today + timedelta(days=1)
                reminder_window_end = today + timedelta(days=3)

                for goal in Goal.objects.filter(user=user):
                    goal_id = str(goal.id)
                    goal.title = request.POST.get(f'goal_title_{goal_id}')
                    start_date_str = request.POST.get(f'goal_start_{goal_id}')
                    goal.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else today
                    deadline_str = request.POST.get(f'goal_deadline_{goal_id}')
                    goal.deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date() if deadline_str else None
                    goal_completed = bool(request.POST.get(f'goal_completed_{goal_id}'))
                    completed_date_str = request.POST.get(f'goal_completed_date_{goal_id}')
                    goal.completed_date = datetime.strptime(completed_date_str, '%Y-%m-%d').date() if completed_date_str else None
                    days_spent_str = request.POST.get(f'goal_days_spent_{goal_id}')
                    goal.days_spent = int(days_spent_str) if days_spent_str and days_spent_str.isdigit() else None
                    goal.completed = goal_completed
                    goal.save()

                    if goal.deadline and not goal.completed and reminder_window_start <= goal.deadline <= reminder_window_end:
                        send_goal_reminder_email(user.email, goal.title, goal.deadline)

                    # ✅ Sequential milestone completion enforcement
                    milestones = list(goal.milestones.all().order_by('deadline'))
                    previous_completed = True

                    for i, milestone in enumerate(milestones):
                        milestone.name = request.POST.get(f'milestone_name_{goal_id}_{i}')
                        milestone.progress = request.POST.get(f'milestone_progress_{goal_id}_{i}')
                        milestone_deadline_str = request.POST.get(f'milestone_date_{goal_id}_{i}')
                        milestone.deadline = datetime.strptime(milestone_deadline_str, '%Y-%m-%d').date() if milestone_deadline_str else None

                        milestone_completed_requested = bool(request.POST.get(f'milestone_completed_{goal_id}_{i}'))
                        milestone.completed = milestone_completed_requested if previous_completed else False

                        milestone_completed_date_str = request.POST.get(f'milestone_completed_date_{goal_id}_{i}')
                        milestone.completed_date = datetime.strptime(milestone_completed_date_str, '%Y-%m-%d').date() if milestone_completed_date_str else None
                        milestone.save()

                        previous_completed = milestone.completed

                        if milestone.completed and milestone.completed_date and milestone.deadline:
                            delay_days = (milestone.completed_date - milestone.deadline).days
                            if delay_days > 0:
                                for subsequent_milestone in milestones[i + 1:]:
                                    if subsequent_milestone.deadline:
                                        subsequent_milestone.deadline += timedelta(days=delay_days)
                                        subsequent_milestone.save()

                        if milestone.deadline and not milestone.completed and reminder_window_start <= milestone.deadline <= reminder_window_end:
                            send_milestone_reminder_email(user.email, milestone.name, goal.title, milestone.deadline)

                    # ✅ New milestones for existing goals
                    new_milestone_keys = [k for k in request.POST if k.startswith(f'milestone_name_{goal_id}new')]
                    for key in new_milestone_keys:
                        name = request.POST.get(key)
                        if name:
                            suffix = key.split("_name_")[-1]
                            milestone_deadline_str = request.POST.get(f'milestone_date_{suffix}')
                            milestone_deadline = datetime.strptime(milestone_deadline_str, '%Y-%m-%d').date() if milestone_deadline_str else None
                            milestone_completed = bool(request.POST.get(f'milestone_completed_{suffix}'))
                            milestone_completed_date_str = request.POST.get(f'milestone_completed_date_{suffix}')
                            milestone_completed_date = datetime.strptime(milestone_completed_date_str, '%Y-%m-%d').date() if milestone_completed_date_str else None
                            new_milestone = Milestone.objects.create(
                                goal=goal,
                                name=name,
                                progress=request.POST.get(f'milestone_progress_{suffix}', ''),
                                deadline=milestone_deadline,
                                completed=milestone_completed,
                                completed_date=milestone_completed_date
                            )
                            if milestone_deadline and not milestone_completed and reminder_window_start <= milestone_deadline <= reminder_window_end:
                                send_milestone_reminder_email(user.email, new_milestone.name, goal.title, milestone_deadline)

                # ✅ Process new goals
                new_goal_keys = [k for k in request.POST if k.startswith('goal_title_') and 'new_' in k]
                for key in new_goal_keys:
                    goal_id = key.split('goal_title_')[1]
                    title = request.POST.get(key)
                    if title:
                        start_date_str = request.POST.get(f'goal_start_{goal_id}')
                        deadline_str = request.POST.get(f'goal_deadline_{goal_id}')
                        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date() if deadline_str else None
                        completed = bool(request.POST.get(f'goal_completed_{goal_id}'))
                        completed_date_str = request.POST.get(f'goal_completed_date_{goal_id}')
                        completed_date = datetime.strptime(completed_date_str, '%Y-%m-%d').date() if completed_date_str else None
                        days_spent_str = request.POST.get(f'goal_days_spent_{goal_id}')
                        days_spent = int(days_spent_str) if days_spent_str and days_spent_str.isdigit() else None
                        new_goal = Goal.objects.create(
                            title=title,
                            start_date=datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else today,
                            deadline=deadline,
                            completed=completed,
                            completed_date=completed_date,
                            days_spent=days_spent,
                            user=user
                        )

                        if deadline and not completed and reminder_window_start <= deadline <= reminder_window_end:
                            send_goal_reminder_email(user.email, new_goal.title, deadline)

                        milestone_keys = [k for k in request.POST if k.startswith(f'milestone_name_{goal_id}new')]
                        for mkey in milestone_keys:
                            name = request.POST.get(mkey)
                            if name:
                                suffix = mkey.split("_name_")[-1]
                                milestone_deadline_str = request.POST.get(f'milestone_date_{suffix}')
                                milestone_deadline = datetime.strptime(milestone_deadline_str, '%Y-%m-%d').date() if milestone_deadline_str else None
                                milestone_completed = bool(request.POST.get(f'milestone_completed_{suffix}'))
                                milestone_completed_date_str = request.POST.get(f'milestone_completed_date_{suffix}')
                                milestone_completed_date = datetime.strptime(milestone_completed_date_str, '%Y-%m-%d').date() if milestone_completed_date_str else None
                                new_milestone = Milestone.objects.create(
                                    goal=new_goal,
                                    name=name,
                                    progress=request.POST.get(f'milestone_progress_{suffix}', ''),
                                    deadline=milestone_deadline,
                                    completed=milestone_completed,
                                    completed_date=milestone_completed_date
                                )
                                if milestone_deadline and not milestone_completed and reminder_window_start <= milestone_deadline <= reminder_window_end:
                                    send_milestone_reminder_email(user.email, new_milestone.name, new_goal.title, milestone_deadline)

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'analytics': Goal.get_analytics(user, year),
                        'message': 'Goals and milestones saved successfully.'
                    })

                messages.success(request, "Goals and milestones saved successfully.")
                return redirect('goal_tracker')

            # ✅ Preprocess milestones for frontend control (can_complete flag)
            goals_with_flags = []
            for goal in goals:
                milestones = list(goal.milestones.all().order_by('deadline'))
                milestone_data = []
                for i, ms in enumerate(milestones):
                    can_complete = (i == 0 or milestones[i - 1].completed)
                    milestone_data.append({'obj': ms, 'can_complete': can_complete})
                goals_with_flags.append({'goal': goal, 'milestones': milestone_data})

            return render(request, 'goal_tracker.html', {
                'goals_with_flags': goals_with_flags,
                'current_year': year,
                'analytics': analytics,
                    'today': date.today(),  # ✅ Add this line

            })

        except Exception as e:
            print("EXCEPTION:", e)
            traceback.print_exc()
            return redirect('goal_tracker')
    else:
        return redirect('logins')
    
def send_milestone_reminder_email(user_email, milestone_name, goal_title, deadline):
  
    try:
        if isinstance(deadline, datetime):
            deadline = deadline.strftime('%Y-%m-%d')
        subject = "⏰ Milestone Reminder"
        message = f"Reminder! Your milestone '{milestone_name}' for goal '{goal_title}' is due on {deadline}."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email to {user_email}: {str(e)}")
        return False

def send_goal_reminder_email(user_email, goal_title, deadline):
    
    try:
        if isinstance(deadline, datetime):
            deadline = deadline.strftime('%Y-%m-%d')
        subject = "⏰ Goal Deadline Reminder"
        message = f"Reminder! Your goal '{goal_title}' is due on {deadline}."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email to {user_email}: {str(e)}")
        return False
    


def reminder(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('logins')

        today = timezone.now().date()
        user_goals = Goal.objects.filter(user_id=user_id).prefetch_related('milestones')

        incomplete_milestones = []
        missed_milestones = []

        for goal in user_goals:
            for milestone in goal.milestones.all():
                # Check if milestone is incomplete and has a deadline
                if not milestone.completed and milestone.deadline:
                    days_left = (milestone.deadline - today).days

                    if days_left >= 0:
                        # Assign color code for urgency
                        if days_left == 0:
                            color = 'danger'   # Due today
                        elif days_left <= 3:
                            color = 'warning'  # Due soon
                        else:
                            color = 'success'  # Plenty of time

                        # Send email reminder if urgent and user has email
                        try:
                            if days_left <= 3 and goal.user.email:
                                send_milestone_reminder_email(
                                    user_email=goal.user.email,
                                    milestone_name=milestone.name,
                                    goal_title=goal.title,
                                    deadline=milestone.deadline
                                )
                        except Exception as e:
                            print(f"Email sending failed: {e}")
                            messages.warning(request, f"Reminder email could not be sent for milestone '{milestone.name}'.")

                        # Add to upcoming milestones
                        incomplete_milestones.append({
                            'goal': goal,
                            'milestone': milestone,
                            'days_left': days_left,
                            'urgency': color
                        })
                    else:
                        # Add to missed milestones
                        missed_milestones.append({
                            'goal': goal,
                            'milestone': milestone,
                            'days_overdue': abs(days_left)
                        })

        return render(request, 'reminder.html', {
            'incomplete_milestones': incomplete_milestones,
            'missed_milestones': missed_milestones
        })
    else:
        return redirect('logins')


def todo_list(request, year=None, month=None, day=None):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user = get_object_or_404(Login, id=user_id)

        # Default to today
        if year is None or month is None or day is None:
            selected_date = date.today()
            return redirect('todo_list_date', year=selected_date.year, month=selected_date.month, day=selected_date.day)

        selected_date = date(year, month, day)

        if request.method == 'POST':
            if 'save_changes' in request.POST:
                for key in request.POST:
                    if key.startswith('task_') and '_text' in key:
                        task_id = key.split('_')[1]
                        task = get_object_or_404(Todo, id=task_id, user=user)
                        task.task = request.POST[key]
                        task.completed = f'task_{task_id}_completed' in request.POST
                        task.save()

                for key in request.POST:
                    if key.startswith('new_task_') and not key.endswith('_completed'):
                        task_index = key.split('_')[2]
                        task_text = request.POST.get(f'new_task_{task_index}', '').strip()
                        completed = request.POST.get(f'new_task_{task_index}_completed') == 'on'

                        if task_text:
                            Todo.objects.create(
                                user=user,
                                date=selected_date,
                                task=task_text,
                                completed=completed
                            )
                return redirect('todo_list_date', year=year, month=month, day=day)

            elif 'delete_task' in request.POST:
                task_id = request.POST.get('delete_task')
                Todo.objects.filter(id=task_id, user=user).delete()
                return redirect('todo_list_date', year=year, month=month, day=day)

            elif 'delete_all' in request.POST:
                Todo.objects.filter(user=user, date=selected_date).delete()
                return redirect('todo_list_date', year=year, month=month, day=day)

        todos = Todo.objects.filter(user=user, date=selected_date).order_by('created_at')
        prev_date = selected_date - timedelta(days=1)
        next_date = selected_date + timedelta(days=1)

        return render(request, 'todo_list.html', {
            'date': selected_date.strftime("%B %d, %Y"),
            'tasks': todos,
            'prev_date': prev_date,
            'next_date': next_date,
            'year': year,
            'month': month,
            'day': day
        })
    else:
        return redirect('logins')
def delete_todo(request, year, month, day):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        if request.method == 'POST':
            user = get_object_or_404(Login, id=user_id)
            Todo.objects.filter(user=user, date=date(year, month, day)).delete()

        return redirect('todo_list', year=year, month=month, day=day)
    else:
        return redirect('logins')

def todo_search(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')  
        if not user_id:
            return redirect('login')  

        user = get_object_or_404(Login, id=user_id)
        search_date = request.GET.get('date') 

        tasks = []
        if search_date:
            tasks = Todo.objects.filter(user=user, date=search_date).order_by('created_at')

        return render(request, 'todo_search.html', {
            'tasks': tasks,
            'search_date': search_date,
        })
    else:
        return redirect('logins')


def daily_checkin_bonus(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user = get_object_or_404(Login, id=user_id)
        daily_checkin, created = DailyCheck.objects.get_or_create(
            login_id=user,
            defaults={'streak': 0, 'longest_streak': 0}
        )

        today = timezone.now().date()
        can_checkin = daily_checkin.last_checkin != today

        if request.method == 'POST':
            if not can_checkin:
                return JsonResponse({
                    'success': False,
                    'error': 'You have already checked in today!'
                })

            daily_checkin.update_streak()
            return JsonResponse({
                'success': True,
                'streak': daily_checkin.streak,
                'last_checkin': daily_checkin.last_checkin.strftime('%Y-%m-%d')
            })

        if not can_checkin:
            tomorrow = today + timedelta(days=1)
            midnight = datetime.combine(tomorrow, time(0, 0), tzinfo=timezone.get_current_timezone())
            seconds_until_midnight = (midnight - timezone.now()).total_seconds()
        else:
            seconds_until_midnight = 0

        context = {
            'daily_checkin': daily_checkin,
            'can_checkin': can_checkin,
            'seconds_until_midnight': int(seconds_until_midnight),
            'checkin_history': daily_checkin.get_checkin_history()
        }
        return render(request, 'daily_checkin.html', context)
    else:
        return redirect('logins')


def notification_create(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Notification created successfully!")
            return redirect('notification_list')
    else:
        form = NotificationForm()
    return render(request, 'notification_create.html', {'form': form})




def habit_link(request, year, month, day):
    return render(request, 'habit_link.html', {
        'year': year,
        'month': month,
        'day': day,
    })


def habit_tracker(request, year, month):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user = get_object_or_404(Login, id=user_id)

        # Navigation logic
        prev_month = month - 1 if month > 1 else 12
        prev_year = year - 1 if month == 1 else year
        next_month = month + 1 if month < 12 else 1
        next_year = year + 1 if month == 12 else year

        num_days = cal.monthrange(year, month)[1]
        days_range = list(range(1, num_days + 1))

        # Fetch existing habits
        habits = Habit.objects.filter(user=user, year=year, month=month)

        habit_ids = [habit.id for habit in habits]
        existing_ticks = HabitTick.objects.filter(
            habit_id__in=habit_ids,
            day__in=days_range
        ).values_list('habit_id', 'day', 'checked')

        habit_logs = defaultdict(dict)
        for habit_id, day, checked in existing_ticks:
            habit_logs[habit_id][day] = checked

        for habit in habits:
            for day in days_range:
                if day not in habit_logs[habit.id]:
                    habit_logs[habit.id][day] = False

        # Get current date
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day

        context = {
            'habits': habits.order_by('id'),
            'habit_logs': habit_logs,
            'days_range': days_range,
            'month': month,
            'year': year,
            'calendar_month': cal.month_name[month],
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
            'current_year': current_year,
            'current_month': current_month,
            'current_day': current_day,
        }

        return render(request, 'habit_tracker.html', context)
    else:
        return redirect('logins')


def save_habits(request):
    if 'user_id' in request.session:
        if not request.session.get('user_id'):
            return redirect('login')
            
        if request.method == 'POST':
            try:
                year = int(request.POST.get('year'))
                month = int(request.POST.get('month'))
            except (ValueError, TypeError):
                return HttpResponseBadRequest("Invalid date parameters")
    
            user = get_object_or_404(Login, id=request.session['user_id'])
            updates = []
            new_habits = defaultdict(lambda: {'name': '', 'days': {}})
            
            # Get current date for validation
            current_date = datetime.now()
            current_year = current_date.year
            current_month = current_date.month
            current_day = current_date.day
    
            def is_future_date(day):
                if year > current_year:
                    return True
                if year < current_year:
                    return False
                if month > current_month:
                    return True
                if month < current_month:
                    return False
                return day > current_day
    
            # First pass: Collect new habit data
            for key in request.POST:
                if key.startswith('habit_new_'):
                    parts = key.split('_')
                    if len(parts) < 4:
                        continue
                    
                    temp_id = parts[2]
                    
                    if parts[3] == 'name':
                        new_habits[temp_id]['name'] = request.POST[key].strip()
                    elif parts[3].isdigit():
                        day = int(parts[3])
                        if not is_future_date(day):
                            new_habits[temp_id]['days'][day] = request.POST[key] == 'on'
    
            # Second pass: Process existing habits
            for key in request.POST:
                if key.startswith('habit_') and not key.startswith('habit_new_'):
                    parts = key.split('_')
                    if len(parts) != 3:
                        continue
                    
                    try:
                        habit_id = int(parts[1])
                        day = int(parts[2])
                        if is_future_date(day):
                            continue
                        habit = Habit.objects.get(id=habit_id, user=user)
                        updates.append(
                            HabitTick(
                                habit=habit,
                                day=day,
                                month=month,
                                year=year,
                                checked=request.POST[key] == 'on'
                            )
                        )
                    except (Habit.DoesNotExist, ValueError):
                        continue
                    
            with transaction.atomic():
                # Create new habits
                for temp_id, data in new_habits.items():
                    if data['name']:
                        habit = Habit.objects.create(
                            user=user,
                            name=data['name'],
                            year=year,
                            month=month
                        )
                        for day, checked in data['days'].items():
                            if not is_future_date(day):
                                updates.append(
                                    HabitTick(
                                        habit=habit,
                                        day=day,
                                        month=month,
                                        year=year,
                                        checked=checked
                                    )
                                )
    
                # Clear existing ticks
                HabitTick.objects.filter(
                    habit__user=user,
                    month=month,
                    year=year
                ).delete()
                
                # Create all ticks
                HabitTick.objects.bulk_create(updates)
    
            return redirect('habit_tracker', year=year, month=month)
    
        return HttpResponseBadRequest("Invalid request")
    else:
        return redirect('logins')

def delete_habit(request, habit_id):
    if 'user_id' in request.session:
        if not request.session.get('user_id'):
            return redirect('login')

        user = get_object_or_404(Login, id=request.session['user_id'])
        habit = get_object_or_404(Habit, id=habit_id, user=user)

        if request.method == 'POST':
            with transaction.atomic():
                habit_year = habit.year
                habit_month = habit.month
                habit.delete()

            return redirect('habit_tracker', year=habit_year, month=habit_month)

        return HttpResponseBadRequest("Invalid request")
    else:
        return redirect('logins')



def diary_hub(request):
    if 'user_id' in request.session:
    # Check if user is logged in via session
        if 'user_id' not in request.session:
            return redirect('logins')  # Redirect to login page

        return render(request, 'diary/diary_hub.html')
    else:
        return redirect('logins')

# import json, base64, uuid
from django.core.files.base import ContentFile
def text_diary(request):
    if 'user_id' not in request.session:
        return redirect('logins')

    user = get_object_or_404(Login, id=request.session['user_id'])
    selected_date = request.GET.get('date', timezone.now().date().isoformat())

    edit_entry = None
    if 'edit' in request.GET:
        try:
            edit_entry = DiaryEntry.objects.get(id=request.GET['edit'], user=user, entry_type='text')
        except DiaryEntry.DoesNotExist:
            pass

    if request.method == 'POST':
        try:
            # Handle deletion
            if 'delete_entry_id' in request.POST:
                entry_to_delete = get_object_or_404(DiaryEntry, id=request.POST['delete_entry_id'], user=user, entry_type='text')
                entry_to_delete.delete()
                return redirect(f"{request.path}?date={selected_date}")

            # Get content and photos
            content = request.POST.get('content', '').strip()
            photos = request.FILES.getlist('photos')

            # ❗ Correct handling of captured photos
            captured_photos_raw = request.POST.get('captured_photos', '[]')
            try:
                captured_photos = json.loads(captured_photos_raw)
            except json.JSONDecodeError:
                captured_photos = []

            print(f"Captured photos count: {len(captured_photos)}")

            has_photos = bool(photos) or bool(captured_photos)
            if not content and not has_photos:
                return render(request, 'diary/text_diary.html', {
                    'entries': DiaryEntry.objects.filter(user=user, entry_type='text', date=selected_date).order_by('-time'),
                    'selected_date': selected_date,
                    'edit_entry': edit_entry,
                    'error': 'Content cannot be empty.'
                })

            entry_id = request.POST.get('entry_id')
            if entry_id:
                # Update existing entry
                entry = get_object_or_404(DiaryEntry, id=entry_id, user=user, entry_type='text')
                entry.content = content if content else f"Captured Photo Entry on {selected_date}"
                entry.edited_time = timezone.now()
                entry.save()
            else:
                # Create new entry
                entry = DiaryEntry.objects.create(
                    user=user,
                    entry_type='text',
                    content=content if content else f"Captured Photo Entry on {selected_date}",
                    date=selected_date
                )

            # Handle uploaded photos
            if photos:
                existing_photos_count = entry.photos.count()
                if existing_photos_count + len(photos) > 5:
                    return HttpResponseBadRequest("You can only attach or capture up to 5 photos per entry.")
                for photo in photos:
                    DiaryPhoto.objects.create(diary_entry=entry, photo=photo)

            # Handle captured photos (base64)
            if captured_photos:
                existing_photos_count = entry.photos.count()
                if existing_photos_count + len(captured_photos) > 5:
                    return HttpResponseBadRequest("You can only attach or capture up to 5 photos per entry.")
                for captured_photo in captured_photos:
                    if captured_photo.startswith('data:image/jpeg;base64,'):
                        try:
                            format, imgstr = captured_photo.split(';base64,')
                            ext = 'jpg'
                            unique_filename = f'captured_photo_{uuid.uuid4()}.{ext}'
                            data = ContentFile(base64.b64decode(imgstr), name=unique_filename)
                            photo_instance = DiaryPhoto.objects.create(diary_entry=entry, photo=data)
                            print(f"Saved photo: {photo_instance.photo.url}")
                        except Exception as e:
                            print(f"Failed to save captured photo: {e}")

            return redirect(f"{request.path}?date={selected_date}")

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

    entries = DiaryEntry.objects.filter(
        user=user,
        entry_type='text',
        date=selected_date
    ).order_by('-time')

    context = {
        'entries': entries,
        'selected_date': selected_date,
        'edit_entry': edit_entry,
    }

    return render(request, 'diary/text_diary.html', context)
  
def audio_diary(request):
    if 'user_id' in request.session:
        if 'user_id' not in request.session:
            return redirect('logins')

        user = get_object_or_404(Login, id=request.session['user_id'])
        selected_date = request.GET.get('date', date.today().isoformat())

        if request.method == 'POST':
            try:
                audio_file = request.FILES.get('audio_file')
                duration = request.POST.get('duration', 0)

                if audio_file:
                    file_path = f'audios/user_{user.id}/{audio_file.name}'
                    saved_path = default_storage.save(file_path, audio_file)

                    DiaryEntry.objects.create(
                        user=user,
                        entry_type='audio',
                        file=saved_path,
                        duration=timedelta(seconds=int(duration)),
                        date=selected_date
                    )

                return redirect('audio_diary')

            except Exception as e:
                return HttpResponseBadRequest(f"Error: {str(e)}")

        entries = DiaryEntry.objects.filter(
            user=user,
            entry_type='audio',
            date=selected_date
        ).order_by('-time')

        return render(request, 'diary/audio_diary.html', {
            'entries': entries,
            'selected_date': selected_date
        })
    else:
        return redirect('logins')


def video_diary(request):
    if 'user_id' in request.session:
        if 'user_id' not in request.session:
            return redirect('logins')

        user = get_object_or_404(Login, id=request.session['user_id'])
        selected_date = request.GET.get('date', date.today().isoformat())

        if request.method == 'POST':
            try:
                video_file = request.FILES.get('video_file')
                duration = request.POST.get('duration', 0)

                if video_file:
                    # Save to user-specific directory
                    file_path = f'videos/user_{user.id}/{video_file.name}'
                    saved_path = default_storage.save(file_path, video_file)

                    # Create entry with duration
                    DiaryEntry.objects.create(
                        user=user,
                        entry_type='video',
                        file=saved_path,
                        duration=timedelta(seconds=int(duration)),
                        date=selected_date
                    )

                return redirect('video_diary')

            except Exception as e:
                return HttpResponseBadRequest(f"Error: {str(e)}")

        entries = DiaryEntry.objects.filter(
            user=user,
            entry_type='video',
            date=selected_date
        ).order_by('-time')

        return render(request, 'diary/video_diary.html', {
            'entries': entries,
            'selected_date': selected_date
        })
    else:
        return redirect('logins')

import os
import logging

def delete_diary(request, entry_id):
    # Session validation
    if 'user_id' in request.session:
        if 'user_id' not in request.session:
            return redirect('logins')

        user = get_object_or_404(Login, id=request.session['user_id'])
        entry = get_object_or_404(DiaryEntry, id=entry_id, user=user)

        # Delete associated files if they exist
        if entry.file:  # For audio/video entries
            try:
                file_path = entry.file.path
                if os.path.exists(file_path):
                    os.remove(file_path)  # Try deleting the file
            except PermissionError as e:
                # Log the error (you can also handle retries here if needed)
                logging.error(f"Failed to delete file {file_path}: {e}")
            except Exception as e:
                # Catch any other errors
                logging.error(f"Unexpected error deleting file {file_path}: {e}")

        # Delete the diary entry from the database
        entry.delete()

        # Redirect back to the previous page or default to 'diary_hub'
        return redirect(request.META.get('HTTP_REFERER', 'diary_hub'))
    else:
        return redirect('logins')

def calendar_tasks_json(request):
    if 'user_id' in request.session:
    # Check if user is authenticated via session
        user_id = request.session.get('user_id')
        if not user_id or not Login.objects.filter(id=user_id).exists():
            return JsonResponse([], safe=False)  # Return empty events if not authenticated

        try:
            user = Login.objects.get(id=user_id)
            # Get the year from request or default to current year
            year = request.GET.get('year', date.today().year)
            try:
                year = int(year)
            except ValueError:
                year = date.today().year

            # Fetch user-specific todos, goals, and milestones for the given year
            todos = Todo.objects.filter(user=user, date__year=year)
            goals = Goal.objects.filter(user=user, deadline__year=year)
            milestones = Milestone.objects.filter(goal__user=user, deadline__year=year)

            events = []

            # Add todo events with bullet marker
            for task in todos:
                events.append({
                    "id": task.id,
                    "title": f'• {task.task}',  # Bullet for todos
                    "fullTitle": task.task,  # Store full title for modal
                    "start": task.date.isoformat(),
                    "allDay": True,
                    "type": "todo",
                    "backgroundColor": "transparent",  # No background
                    "markerColor": "#28a745" if task.completed else "#dc3545",  # Green if done, red if not
                    "textColor": "#28a745" if task.completed else "#dc3545",  # Match marker color
                })

            # Add goal deadlines as events
            for goal in goals:
                if goal.deadline:
                    events.append({
                        "id": f"goal_{goal.id}",
                        "title": '★',  # Only star for calendar display
                        "fullTitle": goal.title,  # Full title for modal
                        "start": goal.deadline.isoformat(),
                        "allDay": True,
                        "type": "goal",
                        "backgroundColor": "transparent",  # No background
                        "markerColor": "#ffca28" if goal.completed else "#d32f2f",  # Yellow for completed, red for pending
                        "textColor": "#ffca28" if goal.completed else "#d32f2f",  # Match marker color
                    })

            # Add milestone deadlines as events
            for milestone in milestones:
                if milestone.deadline:
                    events.append({
                        "id": f"milestone_{milestone.id}",
                        "title": '✓',  # Only tick for calendar display
                        "fullTitle": milestone.name,  # Full name for modal
                        "start": milestone.deadline.isoformat(),
                        "allDay": True,
                        "type": "milestone",
                        "backgroundColor": "transparent",  # No background
                        "markerColor": "#4caf50" if milestone.completed else "#ef5350",  # Green for completed, red for pending
                        "textColor": "#4caf50" if milestone.completed else "#ef5350",  # Match marker color
                    })

            return JsonResponse(events, safe=False)

        except Exception as e:
            print(f"Error in calendar_tasks_json: {e}")
            traceback.print_exc()
            return JsonResponse([], safe=False)
    else:
        return redirect('logins')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Challenge, ChallengeProgress, Login


def calculate_leaderboard_entry(progress):
    
    updates = progress.updates.all()
    # Get unique update dates
    update_dates = sorted(set(update.update_date for update in updates))
    points = len(update_dates)  # 1 point per unique day

    # Calculate streak
    if update_dates:
        streak = 1
        max_streak = 1
        for i in range(1, len(update_dates)):
            if (update_dates[i] - update_dates[i-1]).days == 1:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 1
        progress.streak = streak
        progress.save()

        # Streak bonuses
        if max_streak >= 3:
            points += 3
        if max_streak >= 5:
            points += 5

        # Calculate badges
        badges = []
        if max_streak >= 3:
            badges.append("Bronze")
        if max_streak >= 5:
            badges.append("Silver")
        if max_streak >= 7:
            badges.append("Gold")
    else:
        progress.streak = 0
        progress.save()
        max_streak = 0
        badges = []

    return {
        'user': progress.user,
        'points': points,
        'streak': max_streak,
        'badges': badges,
        'updates_count': len(update_dates),
    }

# Existing challenge_list view (abridged, with leaderboard removed since it's now in a separate page)
def challenge_list(request):
    if 'user_id'in request.session:
        user_email = request.session.get('email')
        if not user_email:
            return redirect('login')

        try:
            user = Login.objects.get(email=user_email)
        except Login.DoesNotExist:
            return redirect('login')

        if request.method == 'POST':
            if 'create_challenge' in request.POST:
                form = ChallengeForm(request.POST)
                if form.is_valid():
                    challenge = form.save(commit=False)
                    challenge.user = user
                    challenge.save()
                    messages.success(request, 'Challenge created successfully!')
                else:
                    messages.error(request, 'Error creating challenge. Please check the form.')
                return redirect('challenge_list')

            if 'delete_challenge' in request.POST:
                challenge_id = request.POST.get('challenge_id')
                challenge = get_object_or_404(Challenge, id=challenge_id)
                if challenge.user != user:
                    messages.error(request, 'You are not authorized to delete this challenge.')
                    return redirect('challenge_list')
                challenge.delete()
                messages.success(request, 'Challenge deleted successfully!')
                return redirect('challenge_list')

            if 'join_challenge' in request.POST:
                challenge_id = request.POST.get('challenge_id')
                challenge = get_object_or_404(Challenge, id=challenge_id)
                current_date = timezone.now().date()
                if not (challenge.start_date <= current_date <= challenge.end_date):
                    messages.error(request, 'You can only join this challenge between its start and end dates.')
                    return redirect('challenge_list')
                ChallengeProgress.objects.get_or_create(user=user, challenge=challenge)
                messages.success(request, 'You have joined the challenge!')
                return redirect('challenge_list')

            if 'unjoin_challenge' in request.POST:
                challenge_id = request.POST.get('challenge_id')
                challenge = get_object_or_404(Challenge, id=challenge_id)
                progress = ChallengeProgress.objects.filter(user=user, challenge=challenge).first()
                if progress:
                    progress.delete()
                    messages.success(request, 'You have unjoined the challenge!')
                else:
                    messages.error(request, 'You are not part of this challenge.')
                return redirect('challenge_list')

            if 'post_update' in request.POST:
                challenge_id = request.POST.get('challenge_id')
                challenge = get_object_or_404(Challenge, id=challenge_id)
                progress = ChallengeProgress.objects.filter(user=user, challenge=challenge).first()
                if not progress:
                    messages.error(request, 'You must join the challenge to post an update.')
                    return redirect('challenge_list')

                current_date = timezone.now().date()
                update_date_str = request.POST.get('update_date')
                try:
                    update_date = timezone.datetime.strptime(update_date_str, '%Y-%m-%d').date() if update_date_str else current_date
                except ValueError:
                    messages.error(request, 'Invalid date format.')
                    return redirect('challenge_list')

                if not (challenge.start_date <= update_date <= challenge.end_date):
                    messages.error(request, 'Updates can only be posted between the challenge’s start and end dates.')
                    return redirect('challenge_list')

                text = request.POST.get('text', '')
                photo = request.FILES.get('photo')
                video = request.FILES.get('video')

                if not text and not photo and not video:
                    messages.error(request, 'Please provide some content for your update.')
                    return redirect('challenge_list')

                update = ChallengeUpdate(
                    challenge_progress=progress,
                    text=text,
                    update_date=update_date
                )
                if photo:
                    update.photo = photo
                if video:
                    update.video = video
                update.save()
                messages.success(request, 'Update posted successfully!')
                return redirect('challenge_list')

            if 'delete_update' in request.POST:
                update_id = request.POST.get('update_id')
                update = get_object_or_404(ChallengeUpdate, id=update_id)
                if update.challenge_progress.user != user:
                    messages.error(request, 'You are not authorized to delete this update.')
                    return redirect('challenge_list')
                update.delete()
                messages.success(request, 'Update deleted successfully!')
                return redirect('challenge_list')

            if 'report_post' in request.POST:
                update_id = request.POST.get('update_id')
                update = get_object_or_404(ChallengeUpdate, id=update_id)
                if update.challenge_progress.user == user:
                    messages.error(request, 'You cannot report your own post.')
                    return redirect('challenge_list')
                update.reported = True
                update.save()
                # Notify the post owner
                Notification.objects.create(
                    user=update.challenge_progress.user,
                    notification=f"Your post in '{update.challenge_progress.challenge.title}' is under review due to a user report."
                )
                messages.success(request, 'Post reported successfully!')
                return redirect('challenge_list')

            if 'like_update' in request.POST:
                update_id = request.POST.get('update_id')
                update = get_object_or_404(ChallengeUpdate, id=update_id)
                Like.objects.get_or_create(update=update, user=user)
                messages.success(request, 'Update liked!')
                return redirect('challenge_list')

            if 'unlike_update' in request.POST:
                update_id = request.POST.get('update_id')
                update = get_object_or_404(ChallengeUpdate, id=update_id)
                like = Like.objects.filter(update=update, user=user).first()
                if like:
                    like.delete()
                    messages.success(request, 'Update unliked!')
                return redirect('challenge_list')

            if 'comment_update' in request.POST:
                update_id = request.POST.get('update_id')
                comment_text = request.POST.get('comment_text')
                parent_id = request.POST.get('comment_id')
                update = get_object_or_404(ChallengeUpdate, id=update_id)
                if comment_text:
                    comment_data = {
                        'update': update,
                        'user': user,
                        'text': comment_text
                    }
                    if parent_id:
                        parent = get_object_or_404(Comment, id=parent_id)
                        comment_data['parent'] = parent
                    Comment.objects.create(**comment_data)
                    messages.success(request, 'Comment posted!')
                else:
                    messages.error(request, 'Comment cannot be empty.')
                return redirect('challenge_list')

            if 'delete_comment' in request.POST:
                comment_id = request.POST.get('comment_id')
                comment = get_object_or_404(Comment, id=comment_id)
                if comment.user != user:
                    messages.error(request, 'You are not authorized to delete this comment.')
                    return redirect('challenge_list')
                comment.delete()
                messages.success(request, 'Comment deleted successfully!')
                return redirect('challenge_list')

            if 'edit_comment' in request.POST:
                comment_id = request.POST.get('comment_id')
                comment_text = request.POST.get('comment_text')
                comment = get_object_or_404(Comment, id=comment_id)
                if comment.user != user:
                    messages.error(request, 'You are not authorized to edit this comment.')
                    return redirect('challenge_list')
                if comment_text:
                    comment.text = comment_text
                    comment.save()
                    messages.success(request, 'Comment updated successfully!')
                else:
                    messages.error(request, 'Comment cannot be empty.')
                return redirect('challenge_list')

            if 'report_comment' in request.POST:
                comment_id = request.POST.get('comment_id')
                comment = get_object_or_404(Comment, id=comment_id)
                if comment.user == user:
                    messages.error(request, 'You cannot report your own comment.')
                    return redirect('challenge_list')
                comment.reported = True
                comment.save()
                # Notify the comment owner
                Notification.objects.create(
                    user=comment.user,
                    notification=f"Your comment on a post in '{comment.update.challenge_progress.challenge.title}' is under review due to a user report."
                )
                messages.success(request, 'Comment reported successfully!')
                return redirect('challenge_list')

            if 'like_comment' in request.POST:
                comment_id = request.POST.get('comment_id')
                comment = get_object_or_404(Comment, id=comment_id)
                CommentLike.objects.get_or_create(comment=comment, user=user)
                messages.success(request, 'Comment liked!')
                return redirect('challenge_list')

            if 'unlike_comment' in request.POST:
                comment_id = request.POST.get('comment_id')
                comment = get_object_or_404(Comment, id=comment_id)
                like = CommentLike.objects.filter(comment=comment, user=user).first()
                if like:
                    like.delete()
                    messages.success(request, 'Comment unliked!')
                return redirect('challenge_list')

        challenges = Challenge.objects.all().order_by('-created_at')

        challenge_data = []
        for challenge in challenges:
            challenge.is_creator = (challenge.user == user)
            challenge.has_joined = ChallengeProgress.objects.filter(user=user, challenge=challenge).exists()

            has_liked_data = {}
            comment_liked_data = {}
            for progress in challenge.progress.all():
                has_liked = {}
                comment_likes = {}
                for update in progress.updates.all():
                    has_liked[update.id] = Like.objects.filter(update=update, user=user).exists()
                    for comment in update.comments.all():
                        comment_likes[comment.id] = CommentLike.objects.filter(comment=comment, user=user).exists()
                has_liked_data[progress.id] = has_liked
                comment_liked_data[progress.id] = comment_likes

            challenge_data.append({
                'challenge': challenge,
                'has_liked_data': has_liked_data,
                'comment_liked_data': comment_liked_data,
            })

        return render(request, 'challenge_list.html', {
            'challenge_data': challenge_data,
            'user': user,
            'form': ChallengeForm(),
            'current_date': timezone.now().date(),
        })
    else:
        return redirect('logins')
    
# New leaderboard view
def leaderboard(request):
    if 'user_id' in request.session:
        challenges = Challenge.objects.all().order_by('-created_at')
    
        for challenge in challenges:
            leaderboard = []
            for progress in challenge.progress.all():
                entry = calculate_leaderboard_entry(progress)
                leaderboard.append(entry)
            challenge.leaderboard = sorted(leaderboard, key=lambda x: x['points'], reverse=True)
    
        return render(request, 'leaderboard.html', {
            'challenges': challenges,
        })
    else:
        return redirect('logins')

def join_challenge(request, challenge_id):
    user_email = request.session.get('email')
    if not user_email:
        return redirect('logins')

    try:
        user = Login.objects.get(email=user_email)
    except Login.DoesNotExist:
        return redirect('logins')

    challenge = get_object_or_404(Challenge, id=challenge_id)
    ChallengeProgress.objects.get_or_create(user=user, challenge=challenge)
    return redirect('challenge_list')


def admin_leaderboard(request):
    challenges = Challenge.objects.all().order_by('-created_at')

    for challenge in challenges:
        leaderboard = []
        for progress in challenge.progress.all():
            entry = calculate_leaderboard_entry(progress)
            leaderboard.append(entry)
        challenge.leaderboard = sorted(leaderboard, key=lambda x: x['points'], reverse=True)

    return render(request, 'adminleaderboard.html', {
        'challenges': challenges,
    })

def progress_tracking(request):
    if 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, "You must be logged in.")
                return redirect('logins')

            try:
                user = Login.objects.get(id=user_id)
            except Login.DoesNotExist:
                messages.error(request, "User account not found.")
                return redirect('logins')

            current_year = date.today().year  # 2025
            year = request.GET.get('year', current_year)

            try:
                year = int(year)
            except ValueError:
                year = current_year

            # Fetch goals with related milestones
            goals = Goal.objects.filter(user=user, start_date__year=year).prefetch_related('milestones')

            # Calculate analytics
            analytics = Goal.get_analytics(user, year)

            return render(request, 'progress_tracking.html', {
                'goals': goals,
                'current_year': year,
                'analytics': analytics
            })

        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('progress_tracking')
    else:
        return redirect('logins')    


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import ChallengeUpdate, Notification  # Adjust the import based on your project structure

def admin_reported_posts(request):
    if not request.session.get('admin'):
        return redirect('logins')  # Admin not logged in

    reported_posts = ChallengeUpdate.objects.filter(reported=True).order_by('-created_at')

    if request.method == 'POST':
        if 'delete_post' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(ChallengeUpdate, id=post_id, reported=True)

            # Notify the post owner before deletion
            Notification.objects.create(
                user=post.challenge_progress.user,
                notification=f"Your post in '{post.challenge_progress.challenge.title}' has been deleted due to a user report."
            )
            post.delete()
            messages.success(request, 'Reported post deleted successfully!')
            return redirect('admin_reported_posts')

    return render(request, 'admin_reported_posts.html', {
        'reported_posts': reported_posts,
        'current_date': timezone.now().date(),
    })


def admin_reported_comments(request):
    if not request.session.get('admin'):
        return redirect('logins')
    reported_comments = Comment.objects.filter(reported=True).order_by('-created_at')
  
    if request.method == 'POST':
        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id, reported=True)
            # Notify the comment owner before deletion
            Notification.objects.create(
                user=comment.user,
                notification=f"Your comment on a post in '{comment.update.challenge_progress.challenge.title}' has been deleted due to a user report."
            )
            comment.delete()
            messages.success(request, 'Reported comment deleted successfully!')
            return redirect('admin_reported_comments')   


    return render(request, 'admin_reported_comments.html', {
        'reported_comments': reported_comments,
        'current_date': timezone.now().date(),
    })


# def mbti_test_view(request):
#     if not request.session.session_key:
#         request.session.save()

#     if request.method == 'POST':
#         form = MBTIForm(request.POST)
#         if form.is_valid():
#             answers = {key: value for key, value in form.cleaned_data.items()}
#             scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
#             response_weights = {'SA': 2, 'A': 1, 'N': 0, 'D': -1, 'SD': -2}

#             for i, (_, trait) in enumerate(MBTI_QUESTIONS):
#                 answer = answers.get(f"q_{i}")
#                 if trait in ['E', 'S', 'T', 'J']:
#                     scores[trait] += response_weights.get(answer, 0)
#                 else:  # I, N, F, P
#                     opposite = {'I': 'E', 'N': 'S', 'F': 'T', 'P': 'J'}[trait]
#                     scores[opposite] -= response_weights.get(answer, 0)

#             mbti_type = ''.join([
#                 'I' if scores.get('I', 0) >= scores.get('E', 0) else 'E',
#                 'S' if scores.get('S', 0) >= scores.get('N', 0) else 'N',
#                 'T' if scores.get('T', 0) >= scores.get('F', 0) else 'F',
#                 'J' if scores.get('J', 0) >= scores.get('P', 0) else 'P'
#             ])

#             profile = MBTIExplanation.objects.create(
#                 session_key=request.session.session_key,
#                 mbti_type=mbti_type
#             )
#             request.session['latest_mbti_id'] = profile.id
#             request.session['mbti_answers'] = {}
#             return redirect('mbti_result')
#     else:
#         form = MBTIForm()

#     return render(request, 'mbti_test.html', {
#         'form': form,
#         'total_questions': len(MBTI_QUESTIONS)
#     })

# def mbti_result_view(request):
#     if not request.session.session_key:
#         request.session.save()
#     session_key = request.session.session_key

#     profiles = MBTIExplanation.objects.filter(session_key=session_key).order_by('-date_taken')
#     latest = None
#     latest_id = request.session.get('latest_mbti_id')
#     if latest_id:
#         try:
#             latest = profiles.get(id=latest_id)
#         except MBTIExplanation.DoesNotExist:
#             latest = profiles.first()
#     else:
#         latest = profiles.first()

#     type_counts = Counter(profile.mbti_type for profile in profiles)

#     explanation = None
#     if latest:
#         try:
#             explanation = MBTIExplanation.objects.get(type_code=latest.mbti_type)
#         except MBTIExplanation.DoesNotExist:
#             explanation = None

#     return render(request, 'mbti_result.html', {
#         'latest_profile': latest,
#         'all_profiles': profiles,
#         'type_counts': dict(type_counts),
#         'insight_text': explanation.description if explanation else "No insight available.",
#         'explanation_text': explanation.explanation if explanation else "",
#         'tips_list': explanation.growth_tips if explanation else [],
#         'match_text': explanation.matches if explanation else "",
#     })


# import logging
# from django.shortcuts import render, redirect
# from django.contrib.sessions.models import Session
# from collections import Counter
# from .models import MBTIProfile, MBTIExplanation
# from .forms import MBTIForm
# from django.utils import timezone

# # Set up logging
# logger = logging.getLogger(__name__)

# MBTI_QUESTIONS = [
#     # Extraversion (E) - 8 questions
#     ("You enjoy vibrant social events with lots of people.", 'E'),
#     ("You feel energized by meeting new people and networking.", 'E'),
#     ("You prefer to lead conversations in group settings.", 'E'),
#     ("You enjoy being the center of attention at social gatherings.", 'E'),
#     ("You find it easy to strike up conversations with strangers.", 'E'),
#     ("You thrive in busy, lively environments.", 'E'),
#     ("You enjoy participating in group activities or team sports.", 'E'),
#     ("You feel comfortable expressing yourself in large gatherings.", 'E'),
#     # Introversion (I) - 8 questions
#     ("You often think about what you should have said in a conversation long after it has taken place.", 'I'),
#     ("You prefer to work alone rather than in a team.", 'I'),
#     ("You feel more comfortable in small, familiar groups than large crowds.", 'I'),
#     ("You need time alone to recharge after social interactions.", 'I'),
#     ("You enjoy solitary activities like reading or writing.", 'I'),
#     ("You prefer one-on-one conversations over group discussions.", 'I'),
#     ("You often reflect deeply before sharing your thoughts.", 'I'),
#     ("You feel drained after prolonged social events.", 'I'),
#     # Sensing (S) - 8 questions
#     ("You focus on the present moment rather than future possibilities.", 'S'),
#     ("You prefer concrete facts and details over abstract ideas.", 'S'),
#     ("You rely on past experiences to guide your decisions.", 'S'),
#     ("You enjoy tasks that involve practical, hands-on activities.", 'S'),
#     ("You notice details in your surroundings that others might miss.", 'S'),
#     ("You prefer clear, step-by-step instructions for tasks.", 'S'),
#     ("You value tried-and-true methods over experimental approaches.", 'S'),
#     ("You focus on what is happening now rather than what might happen.", 'S'),
#     # Intuition (N) - 8 questions
#     ("You often spend time exploring unrealistic yet intriguing ideas.", 'N'),
#     ("You are drawn to possibilities and what could be in the future.", 'N'),
#     ("You enjoy thinking about abstract concepts and theories.", 'N'),
#     ("You often notice patterns and connections others overlook.", 'N'),
#     ("You like to imagine different scenarios and outcomes.", 'N'),
#     ("You are excited by innovative and unconventional ideas.", 'N'),
#     ("You enjoy exploring the 'big picture' rather than focusing on details.", 'N'),
#     ("You often think about how current actions might shape the future.", 'N'),
#     # Thinking (T) - 8 questions
#     ("You make decisions based on logical analysis rather than emotions.", 'T'),
#     ("You prioritize objective criteria when solving problems.", 'T'),
#     ("You prefer to keep discussions focused on facts rather than feelings.", 'T'),
#     ("You are comfortable giving constructive criticism to improve outcomes.", 'T'),
#     ("You value fairness and consistency in decision-making.", 'T'),
#     ("You analyze problems systematically before acting.", 'T'),
#     ("You prefer debates that focus on logic over emotional appeals.", 'T'),
#     ("You prioritize efficiency when completing tasks.", 'T'),
#     # Feeling (F) - 8 questions
#     ("If your friend is sad about something, your first instinct is to support them emotionally, not try to solve their problem.", 'F'),
#     ("You consider your personal values when making decisions.", 'F'),
#     ("You are deeply affected by others' emotions and experiences.", 'F'),
#     ("You strive to maintain harmony in your relationships.", 'F'),
#     ("You make decisions based on how they impact others’ feelings.", 'F'),
#     ("You empathize easily with people in difficult situations.", 'F'),
#     ("You prioritize relationships over strict adherence to rules.", 'F'),
#     ("You feel fulfilled when helping others emotionally.", 'F'),
#     # Judging (J) - 8 questions
#     ("You prefer a planned and organized approach to life.", 'J'),
#     ("You like to have a detailed schedule and stick to it.", 'J'),
#     ("You feel satisfied when tasks are completed ahead of deadlines.", 'J'),
#     ("You prefer to make decisions quickly to move forward.", 'J'),
#     ("You organize your workspace to stay efficient.", 'J'),
#     ("You prefer to have a clear plan before starting a project.", 'J'),
#     ("You feel uneasy when plans are left open-ended.", 'J'),
#     ("You like to set goals and follow through systematically.", 'J'),
#     # Perceiving (P) - 8 questions
#     ("Your travel plans are more likely to look like a rough list of ideas than a detailed itinerary.", 'P'),
#     ("You enjoy keeping your options open and being flexible.", 'P'),
#     ("You prefer spontaneous activities over planned ones.", 'P'),
#     ("You feel comfortable adapting to last-minute changes.", 'P'),
#     ("You enjoy exploring new possibilities without a fixed plan.", 'P'),
#     ("You prefer to start projects and figure out details as you go.", 'P'),
#     ("You feel constrained by strict schedules or routines.", 'P'),
#     ("You like to keep your approach open to new opportunities.", 'P'),
# ]

# def mbti_test_view(request):
#     if not request.session.session_key:
#         request.session.save()

#     if request.method == 'POST':
#         form = MBTIForm(request.POST)
#         if form.is_valid():
#             answers = {key: value for key, value in form.cleaned_data.items()}
#             scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
#             response_weights = {'SA': 2, 'A': 1, 'N': 0, 'D': -1, 'SD': -2}

#             for i, (_, trait) in enumerate(MBTI_QUESTIONS):
#                 answer = answers.get(f"q_{i}")
#                 weight = response_weights.get(answer, 0)
#                 if trait in scores:
#                     scores[trait] += weight

#             mbti_type = ''.join([
#                 'E' if scores['E'] >= scores['I'] else 'I',
#                 'S' if scores['S'] >= scores['N'] else 'N',
#                 'T' if scores['T'] >= scores['F'] else 'F',
#                 'J' if scores['J'] >= scores['P'] else 'P'
#             ])

#             if not MBTIProfile.objects.filter(session_key=request.session.session_key).exists():
#                 date_taken = timezone.make_aware(datetime.datetime(2025, 7, 10, 15, 25))
#             else:
#                 date_taken = timezone.now()

#             profile = MBTIProfile.objects.create(
#                 session_key=request.session.session_key,
#                 mbti_type=mbti_type,
#                 date_taken=date_taken
#             )
#             request.session['latest_mbti_id'] = profile.id
#             return redirect('mbti_result')
#         else:
#             logger.error("Form invalid: %s", form.errors)
#     else:
#         form = MBTIForm()

#     return render(request, 'mbti_test.html', {'form': form, 'total_questions': len(MBTI_QUESTIONS)})


# def mbti_result_view(request):
#     if not request.session.session_key:
#         request.session.save()
#     session_key = request.session.session_key

#     profiles = MBTIProfile.objects.filter(session_key=session_key).order_by('-date_taken')
#     latest = profiles.first()
#     type_counts = Counter(profile.mbti_type for profile in profiles)

#     explanation = None
#     if latest:
#         try:
#             explanation = MBTIExplanation.objects.get(type_code=latest.mbti_type)
#         except MBTIExplanation.DoesNotExist:
#             explanation = None

#     return render(request, 'mbti_result.html', {
#         'latest_profile': latest,
#         'all_profiles': profiles,
#         'type_counts': dict(type_counts),
#         'insight_text': explanation.description if explanation else "No insight available.",
#         'explanation_text': explanation.explanation if explanation else "",
#         'tips_list': explanation.growth_tips if explanation else [],
#         'match_text': explanation.matches if explanation else ""
#     })
# from django import forms
# from .views import MBTI_QUESTIONS

# MBTI_CHOICES = (
#     ('SA', 'Strongly Agree'),
#     ('A', 'Agree'),
#     ('N', 'Neutral'),
#     ('D', 'Disagree'),
#     ('SD', 'Strongly Disagree'),
# )

# def get_mbti_form_fields():
#     fields = {}
#     for i, (question, _) in enumerate(MBTI_QUESTIONS):
#         fields[f'q_{i}'] = forms.ChoiceField(
#             label=question,
#             choices=MBTI_CHOICES,
#             widget=forms.RadioSelect(attrs={'class': 'space-x-2'}),
#             required=True
#         )
#     return fields

# class MBTIForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(MBTIForm, self).__init__(*args, **kwargs)
#         self.fields.update(get_mbti_form_fields())
# def user_home_view(request):
#     if not request.session.session_key:
#         request.session.save()
#     session_key = request.session.session_key

#     profiles = MBTIProfile.objects.filter(session_key=session_key).order_by('-date_taken')
#     latest = profiles.first() if profiles.exists() else None

#     return render(request, 'user_home.html', {
#         'latest_profile': latest,
#         'profile_count': profiles.count()
#     })




# from django.shortcuts import render, redirect
# from .forms import MBTIForm
# from .mbti_data import MBTI_QUESTIONS, RESPONSE_WEIGHTS
# from .models import MBTIProfile, MBTIExplanation
# from collections import Counter
# from django.utils import timezone
# import datetime

# def mbti_test_view(request):
#     if not request.session.session_key:
#         request.session.save()

#     if request.method == 'POST':
#         form = MBTIForm(request.POST)
#         if form.is_valid():
#             answers = {key: value for key, value in form.cleaned_data.items()}
#             scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

#             for i, (_, trait) in enumerate(MBTI_QUESTIONS):
#                 weight = RESPONSE_WEIGHTS.get(answers.get(f'q_{i}'), 0)
#                 scores[trait] += weight

#             mbti_type = ''.join([
#                 'E' if scores['E'] >= scores['I'] else 'I',
#                 'S' if scores['S'] >= scores['N'] else 'N',
#                 'T' if scores['T'] >= scores['F'] else 'F',
#                 'J' if scores['J'] >= scores['P'] else 'P',
#             ])

#             profile = MBTIProfile.objects.create(
#                 session_key=request.session.session_key,
#                 mbti_type=mbti_type,
#                 date_taken=timezone.now()
#             )
#             request.session['latest_mbti_id'] = profile.id
#             return redirect('mbti_result')
#     else:
#         form = MBTIForm()

#     return render(request, 'mbti_test.html', {'form': form})

# def mbti_result_view(request):
#     session_key = request.session.session_key
#     profiles = MBTIProfile.objects.filter(session_key=session_key).order_by('-date_taken')
#     latest = profiles.first()
#     type_counts = Counter(p.mbti_type for p in profiles)
#     explanation = MBTIExplanation.objects.filter(type_code=latest.mbti_type).first() if latest else None

#     return render(request, 'mbti_result.html', {
#         'latest_profile': latest,
#         'type_counts': dict(type_counts),
#         'insight_text': explanation.description if explanation else '',
#         'explanation_text': explanation.explanation if explanation else '',
#         'tips_list': explanation.growth_tips if explanation else [],
#         'match_text': explanation.matches if explanation else '',
#     })
from django.shortcuts import render, redirect
from .forms import MBTIForm
from .mbti_data import MBTI_QUESTIONS, RESPONSE_WEIGHTS, ALL_MBTI_TYPES
from .models import MBTIProfile, MBTIExplanation
from collections import Counter
from django.utils import timezone
import logging
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-GUI environments
import matplotlib.pyplot as plt
import io
import base64

# Set up logging
logger = logging.getLogger(__name__)

def mbti_test_view(request):
    if 'user_id'in request.session:
        if not request.session.session_key:
            request.session.save()

        if request.method == 'POST':
            form = MBTIForm(request.POST)
            if form.is_valid():
                answers = {key: value for key, value in form.cleaned_data.items()}
                scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

                for i, (_, trait) in enumerate(MBTI_QUESTIONS):
                    weight = RESPONSE_WEIGHTS.get(answers.get(f'q_{i}'), 0)
                    scores[trait] += weight

                mbti_type = ''.join([
                    'E' if scores['E'] >= scores['I'] else 'I',
                    'S' if scores['S'] >= scores['N'] else 'N',
                    'T' if scores['T'] >= scores['F'] else 'F',
                    'J' if scores['J'] >= scores['P'] else 'P',
                ])

                profile = MBTIProfile.objects.create(
                    session_key=request.session.session_key,
                    mbti_type=mbti_type,
                    date_taken=timezone.now()
                )
                request.session['latest_mbti_id'] = profile.id
                logger.info(f"Created profile: {mbti_type} for session {request.session.session_key}")
                return redirect('mbti_result')
        else:
            form = MBTIForm()

        return render(request, 'mbti_test.html', {'form': form})
    else:
        return redirect(logins)

def mbti_result_view(request):
    if 'user_id'in request.session:
        session_key = request.session.session_key
        profiles = MBTIProfile.objects.filter(session_key=session_key).order_by('-date_taken')
        latest = profiles.first()
        # Initialize type_counts with all 16 MBTI types, defaulting to 0
        type_counts = Counter({mbti: 0 for mbti in ALL_MBTI_TYPES})
        # Update with actual counts from profiles
        type_counts.update(p.mbti_type for p in profiles)
        logger.debug(f"Debug: profiles = {list(profiles.values())}")
        logger.debug(f"Debug: type_counts = {dict(type_counts)}")
        explanation = MBTIExplanation.objects.filter(type_code=latest.mbti_type).first() if latest else None

        # Generate bar graph
        plt.figure(figsize=(10, 6))
        if type_counts:
            types = list(type_counts.keys())
            counts = list(type_counts.values())
            plt.bar(types, counts, color='skyblue')
            plt.xlabel('MBTI Types')
            plt.ylabel('Frequency')
            plt.title('Distribution of MBTI Types')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            bar_graph = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
        else:
            bar_graph = None

        return render(request, 'mbti_result.html', {
            'latest_profile': latest,
            'profiles': profiles,
            'type_counts': dict(type_counts),
            'insight_text': explanation.description if explanation else '',
            'explanation_text': explanation.explanation if explanation else '',
            'tips_list': explanation.growth_tips if explanation else [],
            'match_text': explanation.matches if explanation else '',
            'bar_graph': bar_graph,
        })
    else:
        return redirect(logins)

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import AIInsight, Goal, Milestone, Login


def generate_ai_insight_for_user(login_user):
    """
    Generate AI insights based on user's goals and milestones.
    Stores personalized analysis, motivation, and strategies.
    """
    goals = Goal.objects.filter(user=login_user)

    for goal in goals:
        total_milestones = goal.milestones.count()
        completed_milestones = goal.milestones.filter(completed=True).count()
        milestone_accuracy = (completed_milestones / total_milestones) * 100 if total_milestones > 0 else 0

        if goal.completed and goal.completed_date:
            days_spent = (goal.completed_date - goal.start_date).days
        else:
            days_spent = None

        # Determine insight content based on performance
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

        # Prevent duplicate entries
        if not AIInsight.objects.filter(user=login_user, goal=goal).exists():
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


def view_recommendations(request):
    """
    Display AI insights for the logged-in user.
    Generates insights on-the-fly if not already stored.
    """
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Adjust to your login route

    try:
        login_user = Login.objects.get(id=user_id)

        # Generate insights if none exist
        if not AIInsight.objects.filter(user=login_user).exists():
            generate_ai_insight_for_user(login_user)

        insights = AIInsight.objects.filter(user=login_user).order_by('-generated_on')

    except Login.DoesNotExist:
        insights = []

    return render(request, 'recommendations.html', {'insights': insights})


def notifications(request):
    user_email = request.session.get('email')
    if not user_email:
        messages.error(request, 'You must be logged in to view notifications.')
        return redirect('login')

    try:
        user = Login.objects.get(email=user_email)
    except Login.DoesNotExist:
        return redirect('login')

    notifications = Notification.objects.filter(user=user).order_by('-current_date')

    return render(request, 'notifications.html', {
        'notifications': notifications,
        'user': user,
        'current_date': timezone.now().date(),
    })





