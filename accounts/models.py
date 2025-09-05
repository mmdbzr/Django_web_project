from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from PIL import Image
import os
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='seeker')

    def __str__(self):
        return self.username

    @property
    def is_seeker(self):
        return self.role == 'seeker'

    @property
    def is_employer(self):
        return self.role == 'employer'

    @property
    def is_admin(self):
        return self.role == 'admin'


def user_avatar_path(instance, filename):
    return f'profiles/user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    avatar = ProcessedImageField(
        upload_to=user_avatar_path,
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 85},
        blank=True,
        null=True
    )
    avatar_thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar and not self.avatar_thumbnail:
            img = Image.open(self.avatar.path)
            img.thumbnail((100, 100))  # تولید بند‌انگشتی
            thumb_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f'user_{self.user.id}')
            os.makedirs(thumb_dir, exist_ok=True)
            thumb_path = os.path.join(thumb_dir, f'thumb_{os.path.basename(self.avatar.name)}')
            img.save(thumb_path)
            self.avatar_thumbnail.name = os.path.relpath(thumb_path, settings.MEDIA_ROOT)
            super().save(*args, **kwargs)

    def __str__(self):
        return f'Profile: {self.user.username}'
