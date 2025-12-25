from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import pyotp


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


# Create your models here.
class UserProfile(TimestampModel):
    class Type(models.TextChoices):
        student = 'student', 'студент'
        tutor = 'tutor', 'преподаватель'

    name = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, blank=True)
    type = models.TextField(choices=Type, null=True, blank=True)
    totp_key = models.CharField(max_length=128, null=True, blank=True, default=pyotp.random_hex)

    class Meta:
        permissions = [
                    
            ("can_see_all_students", "Может видеть всех студентов"),
            ("can_create_students", "Может создавать студентов"),
            ("can_update_students", "Может редактировать студентов"),
            ("can_delete_students", "Может удалять студентов"),
            ("can_see_himself", "Может видеть только себя"),

            ("can_see_test_questions", "Может видеть вопросы тестов"),
            ("can_create_test_questions", "Может создавать вопросы тестов"),
            ("can_update_test_questions", "Может редактировать вопросы тестов"),
            ("can_delete_test_questions", "Может удалять вопросы тестов"),

            ("can_see_test_question_variants", "Может видеть варианты вопросов"),
            ("can_create_test_question_variants", "Может создавать варианты вопросов"),
            ("can_update_test_question_variants", "Может редактировать варианты вопросов"),
            ("can_delete_test_question_variants", "Может удалять варианты вопросов"),

            ("can_see_all_results", "Может видеть все результаты"),
            ("can_see_own_results", "Может видеть только свои результаты"),

            ("can_see_all_tutors", "Может видеть всех преподавателей"),
            ("can_see_his_tutor", "Может видеть своего преподавателя"),
            ("can_create_tutors", "Может создавать преподавателей"),
            ("can_update_tutors", "Может редактировать преподавателей"),
            ("can_delete_tutors", "Может удалять преподавателей"),
        ]
    
    def save(self, *args, **kwargs):
        if self.id is None: 
            self.totp_key = pyotp.random_base32()

        super().save(*args, **kwargs)

    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)