from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
# from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def name(self):
        return "%s %s" % (self.first_name, self.last_name)


class Institute(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Skill_and_Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(upload_to="images/profile", null=True,
                                    default="../static/images/avatar.png", blank=True)
    institute_name = models.ForeignKey(to=Institute, on_delete=models.CASCADE, null=True)
    institute_certificate = models.ImageField(upload_to="images/certificate", null=False, blank=False)
    phone = PhoneNumberField(null=False, blank=False)
    # year_of_passing = models.DateField(null=True, blank=True)
    Experience = models.PositiveIntegerField(default=0, blank=True)
    Skills = models.ManyToManyField(to=Skill_and_Category, related_name="skill")
    ctc = models.IntegerField(null=True, blank=True)
    about = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return self.user.username

    def fullname(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def candidateemail(self):
        return self.user.email

    def is_active(self):
        return self.user.is_active

    def user_pic(self):
        if self.profile_pic.url is not None and self.user.is_active:
            return mark_safe(
                '<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">' + '<a href="{}">'.format(
                    self.profile_pic.url) + '<div class="relative w-12 h-12">' + '<img src="{}" alt="Avatar" class="rounded-full w-full h-full" />'.format(
                    self.profile_pic.url)
                + '<div class="absolute w-4 h-4 right-0 bottom-0 rounded-full bg-blue-400 text-white text-xs text-center leading-4">' + '✓</div>'
                + '</div>' + '</a>')
        elif self.profile_pic.url is not None:
            return mark_safe(
                '<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">' + '<a href="{}">'.format(
                    self.profile_pic.url) + '<div class="relative w-12 h-12">' + '<img src="{}" alt="Avatar" class="rounded-full w-full h-full" />'.format(
                    self.profile_pic.url)
                + '</div>' + '</a>')

    def institute_certificate_img(self):
        if self.institute_certificate.url is not None:
            return mark_safe(
                '<a href="{}">'.format(self.institute_certificate.url) + '<img src="{}" height="50"/>'.format(
                    self.institute_certificate.url) + '</a>')

    def Skill(self):
        return "\n , ".join([s.name for s in self.Skills.all()])


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20)
    company_name = models.CharField(max_length=60)
    company_description = models.CharField(max_length=300)

    def __str__(self):
        return self.user.username

    def fullname(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def is_active(self):
        return self.user.is_active


class RecruiterPosting(models.Model):
    user = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, default='', blank=True)

    job_title = models.CharField(max_length=200)
    # location = PlainLocationField(based_fields=['location'], zoom=7)
    job_description = models.CharField(max_length=1000)
    JOB_TYPE = (
        ('Full time', 'Full time'),
        ('Internship', 'Internship'),
    )
    job_type = models.CharField(choices=JOB_TYPE, max_length=100)
    ctc = models.CharField(max_length=200)
    skills = models.ForeignKey(Skill_and_Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title


class CandidateApply(models.Model):
    cand = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    apply = models.ForeignKey(RecruiterPosting, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='pending')

    def __str__(self):
        return self.cand.user.username

    def Skill(self):
        return "\n , ".join([s.name for s in self.cand.Skills.all()])
