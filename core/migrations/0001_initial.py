# Generated by Django 5.1 on 2024-08-20 15:23

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BehaviorChallenges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Hobbies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='StandardTestScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('score', models.IntegerField(verbose_name='score')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='email')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('phone', models.CharField(max_length=10, verbose_name='phone')),
                ('age', models.CharField(max_length=3, verbose_name='age')),
                ('gender', models.CharField(max_length=20, verbose_name='gender')),
                ('occupation', models.CharField(max_length=150, verbose_name='occupation')),
                ('education_level', models.CharField(max_length=100, verbose_name='education level')),
                ('number_of_children', models.IntegerField(verbose_name='number of children')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailVerificationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('age', models.CharField(max_length=3, verbose_name='age')),
                ('gender', models.CharField(max_length=20, verbose_name='gender')),
                ('learning_style', models.CharField(max_length=100, verbose_name='learning style')),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='GPA')),
                ('adding_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('behavior_challenges', models.ManyToManyField(related_name='children', to='core.behaviorchallenges')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('hobbies', models.ManyToManyField(related_name='children', to='core.hobbies')),
                ('standard_test_score', models.ManyToManyField(related_name='children', to='core.standardtestscore')),
            ],
        ),
    ]
