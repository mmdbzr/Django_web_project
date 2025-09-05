from django.db.models.signals import post_save
from django.dispatch import receiver
from jobs.models import Application, Job
from notifications.models import Notification

# ۱. وقتی کارجو درخواست می‌دهد → نوتیفیکیشن برای کارفرما
@receiver(post_save, sender=Application)
def notify_employer_new_application(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.job.user,  # کارفرما
            message=f"{instance.user.username} برای '{instance.job.title}' درخواست داد",
            type='in_app'
        )

# ۲. وقتی کارفرما آگهی جدید ایجاد می‌کند → نوتیفیکیشن برای همه جویای کار
@receiver(post_save, sender=Job)
def notify_seekers_new_job(sender, instance, created, **kwargs):
    if created:
        seekers = instance.user.__class__.objects.filter(role='seeker')
        for seeker in seekers:
            Notification.objects.create(
                user=seeker,
                message=f"آگهی جدید '{instance.title}' توسط {instance.user.username} منتشر شد",
                type='in_app'
            )
