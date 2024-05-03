from django.contrib import admin
from django.core.mail import EmailMessage
from django.template.loader import get_template

from .models import User, Candidate, Recruiter, RecruiterPosting, CandidateApply, Institute, Skill_and_Category


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'is_candidate', 'is_recruiter']
    search_fields = ['first_name']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['user','pk','user_pic', 'first_name', 'last_name', 'candidateemail','institute_name', 'institute_certificate_img',
                    'Experience','phone','Skill', 'is_active','about']
    autocomplete_fields = ['Skills']
    search_fields = ['user','user__email','phone']
    actions = ['active_user', 'inactive_user']


    def active_user(self, request, queryset):
        for c in list(queryset):
            User.objects.filter(id=c.user.id).update(is_active=True)

            context = {

                'name': c.user.name()
            }
            message = get_template("emails/candidatesignupconfirm.html").render(context)
            mail = EmailMessage(
                subject="Candidate Approval Login",
                body=message,
                from_email='qasimyousaf703@gmail.com',
                to=[c.user.email],

            )
            mail.content_subtype = "html"
            mail.send()

    def inactive_user(self, request, queryset):
        for c in list(queryset):
            User.objects.filter(id=c.user.id).update(is_active=False)
            context = {

                'name': c.user.name()
            }
            message = get_template("emails/candidaterejectedmail.html").render(context)
            mail = EmailMessage(
                subject="Candidate Rejected",
                body=message,
                from_email='qasimyousaf703@gmail.com',
                to=[c.user.email],

            )
            mail.content_subtype = "html"
            mail.send()

    active_user.short_description = "Active Candidate User"
    inactive_user.short_description = "InActive Candidate User"


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'phone_number', 'company_name', 'company_description',
                    'is_active']
    list_filter = ['company_name', 'user__is_active']

    actions = ['active_user', 'inactive_user']

    def active_user(self, request, queryset):
        for c in list(queryset):
            User.objects.filter(id=c.user.id).update(is_active=True)
            context = {

                'name': 'Qasim'
            }
            message = get_template("emails/rectuirloginapproval.html").render(context)
            mail = EmailMessage(
                subject="Candidate Approval Login",
                body=message,
                from_email='qasimyousaf703@gmail.com',
                to=['oneskill.contact@gmail.com', 'myownbusinessmail321@gmail.com'],

            )
            mail.content_subtype = "html"
            mail.send()

    def inactive_user(self, request, queryset):
        for c in list(queryset):
            User.objects.filter(id=c.user.id).update(is_active=False)
            context = {

                'name': 'Qasim'
            }
            message = get_template("emails/rectuirrejected.html").render(context)
            mail = EmailMessage(
                subject="Candidate Approval Login",
                body=message,
                from_email='qasimyousaf703@gmail.com',
                to=['oneskill.contact@gmail.com', 'myownbusinessmail321@gmail.com'],

            )
            mail.content_subtype = "html"
            mail.send()

    active_user.short_description = "Active Recruiter User"
    inactive_user.short_description = "InActive Recruiter User"


@admin.register(RecruiterPosting)
class RecruiterPostingAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'job_description', 'job_type', 'ctc', 'skills','company_name','user']
    list_filter = ('job_description', 'job_type')
    search_fields = ['job_type', 'job_description']


@admin.register(CandidateApply)
class CandidateApplyAdmin(admin.ModelAdmin):
    list_display = ['cand', 'apply','status']


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Skill_and_Category)
class Skill_and_CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
