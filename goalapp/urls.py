from django.urls import *
from .import views

from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.admin,name='admin'),
    path('logins/',views.logins,name='logins'),
    path('logout/', views.logout_view, name='logout'),
    path('users/',views.users,name='users'),
    path('register/',views.register,name='register'),
    path('calendar/',views.calendar,name='calendar'),

    path('admin_user/',views.admin_user,name='admin_user'),
    path('user_home/',views.user_home,name='user_home'),
    path('userprofile/',views.edit_userprofile,name='userprofile'),
   
    path('goal_tracker/', views.goal_tracker, name='goal_tracker'),
    path('send_goal_reminder_email/',views.send_goal_reminder_email,name='send_goal_reminder_email'),
    path('send_milestone_reminder_email/',views.send_milestone_reminder_email,name='send_milestone_reminder_email'),
    path('reminder/', views.reminder, name='reminder'),
    path('todo/', views.todo_list, name='todo_list'),  # Default today
    path('todo/<int:year>/<int:month>/<int:day>/', views.todo_list, name='todo_list_date'),
    path('delete-todo/<int:year>/<int:month>/<int:day>/',views.delete_todo, name='delete_todo'),
    path('todo_search/',views.todo_search, name='todo_search'),
    path('daily-checkin/', views.daily_checkin_bonus, name='daily_checkin_bonus'),

    path('admin_reported_comments/',views.admin_reported_comments, name='admin_reported_comments'),
    path('admin_reported_posts/',views.admin_reported_posts, name='admin_reported_posts'),
    
    path('notifications/', views.notifications, name='notifications'),
    path('notification_create/', views.notification_create, name='notification_create'),
    path('calendar_view/', views.calendar_view, name='calendar_view'),
    path('habit_tracker/<int:year>/<int:month>/', views.habit_tracker, name='habit_tracker'),
    path('habit_link/<int:year>/<int:month>/<int:day>/', views.habit_link, name='habit_link'),
    path('save_habits/', views.save_habits, name='save_habits'),
    path('delete_habit/<int:habit_id>/',views.delete_habit, name='delete_habit'),
    path('diary_hub/', views.diary_hub, name='diary_hub'),
    # Diary Types
    path('text_diary/', views.text_diary, name='text_diary'),
    

    path('audio_diary/', views.audio_diary, name='audio_diary'),
    
    path('video_diary/', views.video_diary, name='video_diary'),
    
    # Entry Deletion
    path('delete_diary/<int:entry_id>/', views.delete_diary, name='delete_diary'),

    path('calendar/tasks/', views.calendar_tasks_json, name='calendar_tasks_json'),
    path('dismiss-notification/', views.dismiss_notification, name='dismiss_notification'),
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('challenges/join/<int:challenge_id>/', views.join_challenge, name='join_challenge'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path('admin_leaderboard/',views.admin_leaderboard,name='admin_leaderboard'),
    path('progress-tracking/', views.progress_tracking, name='progress_tracking'),
    path('recommendations/', views.view_recommendations, name='view_recommendations'),

    path('mbti_test/', views.mbti_test_view, name='mbti_test'),
    path('mbti_result/', views.mbti_result_view, name='mbti_result'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

  




  


  

   

