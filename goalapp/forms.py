from django import forms
from .models import *
from django import forms
from .models import Challenge, ChallengeProgress
from django.core.exceptions import ValidationError
from datetime import date


#(user input)

#user model
class UserForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-Binary', 'Non-Binary'),
        ('Transgender', 'Transgender'),
        ('Other', 'Other'),
    ]
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select)

    class Meta:
        model = User
        fields = ['name', 'username', 'date_of_birth', 'gender', 'age', 'contact_no']
        widgets = {
            'age': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }
       
#login model
class LoginForm(forms.ModelForm):
    class Meta:
        model=Login
        fields=['email','password',]

class LoginCheck(forms.Form):
    email=forms.EmailField()
    password=forms.CharField()
    
    
class EmailForm(forms.ModelForm):
    class Meta:
        model=Login
        fields=['email']



class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['date','task']        

class NotificationForm(forms.ModelForm):
    class Meta:
        model=Notification
        fields=['notification']     



class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name']



class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")
        if start_date and start_date < date.today():
            raise ValidationError("Start date cannot be in the past.")
        return cleaned_data

class ChallengeProgressForm(forms.ModelForm):
    class Meta:
        model = ChallengeProgress
        fields = ['progress', 'completed']
        widgets = {
            'progress': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }




from django import forms

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
#             widget=forms.RadioSelect,
#             required=True
#         )
#     return fields

# class MBTIForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(MBTIForm, self).__init__(*args, **kwargs)
#         for field_name, field in get_mbti_form_fields().items():
#             self.fields[field_name] = field

# # Note: MBTI_QUESTIONS should be imported or defined in the same file if not already available
# # For this example, assume it's imported from views.py or defined here
# MBTI_QUESTIONS = [
#     ("I enjoy socializing with others.", "E/I"),
#     ("I prefer concrete facts over abstract ideas.", "S/N"),
#     ("I make decisions based on logic.", "T/F"),
#     ("I like to plan my day in advance.", "J/P"),
#     # Add more questions for a full test
# ]

# from django import forms
#  # ensure you centralize this

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
#             widget=forms.RadioSelect,
#             required=True
#         )
#     return fields

# class MBTIForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(MBTIForm, self).__init__(*args, **kwargs)
#         self.fields.update(get_mbti_form_fields())






from django import forms
from .mbti_data import MBTI_QUESTIONS, MBTI_CHOICES

class MBTIForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, (question, _) in enumerate(MBTI_QUESTIONS):
            self.fields[f"q_{i}"] = forms.ChoiceField(
                label=question,
                choices=MBTI_CHOICES,
                widget=forms.RadioSelect,
                required=True
            )