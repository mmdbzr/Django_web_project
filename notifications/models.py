from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    TYPE_CHOICES = (
        ('in_app', 'In-App'),
        ('email', 'Email'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='in_app')

    def __str__(self):
        return f"Notif for {self.user.username}: {self.message[:30]}"
