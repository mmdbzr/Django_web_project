from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User
from notifications.models import Notification  # مدل Notification که ساختیم

def upload_to_resume(instance, filename):
    return f'resumes/{instance.user.id}/{filename}'

# -------------------------
# Job مدل
# -------------------------
class JobManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = JobManager()

    def __str__(self):
        return self.title

# -------------------------
# Application مدل
# -------------------------
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در حال بررسی'),
        ('accepted', 'پذیرفته شده'),
        ('rejected', 'رد شده'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to=upload_to_resume)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} applied to {self.job.title} - {self.status}"

# -------------------------
# سیگنال ارسال Notification خودکار برای کارفرما
# -------------------------
@receiver(post_save, sender=Application)
def send_application_notification(sender, instance, created, **kwargs):
    if created:
        job_owner = instance.job.user
        message = f"{instance.user.username} برای شغل '{instance.job.title}' درخواست ارسال کرده است."
        # ایجاد Notification داخل دیتابیس
        Notification.objects.create(
            user=job_owner,
            message=message,
            type='in_app'
        )
