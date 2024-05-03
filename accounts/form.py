# import self as self
import datetime

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import get_template

from .models import User, Recruiter, Candidate, Institute, Skill_and_Category
# from bootstrap_datepicker_plus import DatePickerInput
# from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from phonenumber_field.formfields import PhoneNumberField


class CandidateSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    # INSTITUTE_CHOICES = (
    #     ('1', 'Dehli University'),
    #     ('2', 'Bombay University'),
    #     ('3', 'Banglore University'),
    #     ('4', 'Kashmir University'),
    # )
    phone = PhoneNumberField()
    profile_pic = forms.ImageField()
    institute_name = forms.ModelChoiceField(queryset=Institute.objects.all())
    institute_certificate = forms.ImageField()
    # year_of_passing = forms.DateField(
    #     widget=DatePickerInput(format='%m/%d/%Y')
    # )
    experience = forms.IntegerField()
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill_and_Category.objects.all()
    )
    ctc=forms.IntegerField()
    about=company_description = forms.CharField(required=True,
                                          widget=forms.Textarea(attrs={'cols': '60', 'rows': ('rows', '15')}), )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'phone', 'profile_pic', 'institute_name',
            'institute_certificate', 'experience',
            'skills', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_candidate = True
        user.is_active = False
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        candidate = Candidate.objects.create(user=user)
        candidate.phone = self.cleaned_data.get('phone')
        candidate.profile_pic = self.cleaned_data.get('profile_pic')
        candidate.institute_name = self.cleaned_data.get('institute_name')
        candidate.institute_certificate = self.cleaned_data.get('institute_certificate')
        # candidate.year_of_passing = self.cleaned_data.get('year_of_passing')
        candidate.Experience = self.cleaned_data.get('experience')
        candidate.ctc=self.cleaned_data.get('ctc')
        candidate.about=self.cleaned_data.get('about')
        for s in self.cleaned_data.get('skills'):
            candidate.Skills.add(s)

        candidate.save()
        return user


class RecruiterSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    company_name = forms.CharField(required=True)
    company_description = forms.CharField(required=True,
                                          widget=forms.Textarea(attrs={'cols': '60', 'rows': ('rows', '15')}), )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_recruiter = True
        user.is_staff = True
        user.is_active = False
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        recruiter = Recruiter.objects.create(user=user)
        recruiter.phone_number = self.cleaned_data.get('phone_number')
        recruiter.company_name = self.cleaned_data.get('company_name')
        recruiter.company_description = self.cleaned_data.get('company_description')
        recruiter.save()
        return user
