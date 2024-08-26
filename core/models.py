from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None 
    email = models.EmailField(_("email"), unique=True, db_index=True)
    name = models.CharField(_("name"), max_length=255)
    phone = models.CharField(_("phone"),unique=True, max_length=10)
    age = models.CharField(_("age"), max_length=3)
    gender = models.CharField(_("gender"), max_length=20)
    occupation = models.CharField(_("occupation"), max_length=150)
    education_level = models.CharField(_("education level"), max_length=100)
    number_of_children = models.IntegerField(_("number of children"))
    parenting_style = models.CharField(_("parenting style"), max_length=150, default="Supportive")
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False, verbose_name='active')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'phone', 'age', 'gender', 'occupation', 'education_level', 'number_of_children']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Hobbies(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BehaviorChallenges(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class StandardTestScore(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Child(models.Model):
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=3)
    gender = models.CharField(max_length=20)
    learning_style = models.CharField(max_length=100)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    grade = models.CharField(max_length=10)
    hobbies = models.ManyToManyField(Hobbies, related_name="children")
    behavior_challenges = models.ManyToManyField(BehaviorChallenges, related_name="children")
    standard_test_score = models.ManyToManyField(StandardTestScore, through='TestScoreThroughModel', related_name="children")
    adding_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class TestScoreThroughModel(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    standard_test_score = models.ForeignKey(StandardTestScore, on_delete=models.CASCADE)
    score = models.IntegerField()

class EmailVerificationToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.email}"
