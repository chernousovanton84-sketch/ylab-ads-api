from celery import shared_task
from django.utils import timezone
from .models import Ad


@shared_task
def archive_expired_ads():
    """
    Переводит объявления из published в archived,
    если expires_at <= текущего времени.
    Безопасен при повторном запуске.
    """
    now = timezone.now()
    expired_ads = Ad.objects.filter(
        status="published",
        expires_at__isnull=False,
        expires_at__lte=now,
    )
    count = expired_ads.update(status="archived")
    return f"Archived {count} ads"
