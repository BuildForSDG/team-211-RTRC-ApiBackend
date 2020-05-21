from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail import EmailMessage
from phonenumber_field.modelfields import PhoneNumberField


class NationalIdType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = PhoneNumberField()
    name = models.CharField(max_length=150)
    national_id = models.CharField(max_length=150, null=True, unique=True)
    national_id_type = models.ForeignKey(NationalIdType, on_delete=models.SET_NULL, null=True, related_name='user_id_type')
    digital_address = models.CharField(max_length=150, null=True, unique=True)
    is_user = models.BooleanField(default=False)
    is_collector = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)

    def email_user(
            self, subject, message, from_email=settings.DEFAULT_FROM_EMAIL, **kwargs):
        """
        Sends an email to this User.
        """
        # message = render_to_string(html_email_template_name, context=context)
        email = EmailMessage(
            subject,
            message,
            from_email,
            [self.email]
            )

        email.content_subtype = "html"
        email.send()

