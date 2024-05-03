# Generated by Django 4.2 on 2023-05-01 08:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_candidate', models.BooleanField(default=False)),
                ('is_recruiter', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill_and_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_pic', models.ImageField(blank=True, default='../static/images/avatar.png', null=True, upload_to='images/profile')),
                ('institute_certificate', models.ImageField(upload_to='images/certificate')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('Experience', models.PositiveIntegerField(blank=True, default=0)),
                ('ctc', models.IntegerField(blank=True, null=True)),
                ('about', models.CharField(blank=True, max_length=300, null=True)),
                ('Skills', models.ManyToManyField(related_name='skill', to='accounts.skill_and_category')),
                ('institute_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.institute')),
            ],
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(max_length=20)),
                ('company_name', models.CharField(max_length=60)),
                ('company_description', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='RecruiterPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, default='', max_length=200)),
                ('job_title', models.CharField(max_length=200)),
                ('job_description', models.CharField(max_length=1000)),
                ('job_type', models.CharField(choices=[('Full time', 'Full time'), ('Internship', 'Internship')], max_length=100)),
                ('ctc', models.CharField(max_length=200)),
                ('skills', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.skill_and_category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.recruiter')),
            ],
        ),
        migrations.CreateModel(
            name='CandidateApply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='pending', max_length=100)),
                ('apply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.recruiterposting')),
                ('cand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.candidate')),
            ],
        ),
    ]