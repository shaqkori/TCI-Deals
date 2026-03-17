# core/models.py

from django.db import models
from django.contrib.auth.models import User


# ── PLANS ───────────────────────────────────────────────────

class Plan(models.Model):
    name                   = models.CharField(max_length=50, unique=True)
    max_tracked_categories = models.IntegerField()
    price                  = models.DecimalField(max_digits=10, decimal_places=2)
    allows_sms             = models.BooleanField(default=False)
    allows_whatsapp        = models.BooleanField(default=False)
    created_at             = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ── USER PROFILE ────────────────────────────────────────────
# Extends Django's built in User model with extra fields

class UserProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    plan            = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, default=1)
    phone           = models.CharField(max_length=20, blank=True, null=True)
    alert_threshold = models.IntegerField(default=20)  # minimum discount % to alert
    instant_alerts  = models.BooleanField(default=True)
    daily_digest    = models.BooleanField(default=False)
    digest_time     = models.CharField(max_length=5, default="09:00")
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {self.plan}"


# ── CATEGORIES ──────────────────────────────────────────────

class Category(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name_plural = "Categories"


# ── DEALS ───────────────────────────────────────────────────

class Deal(models.Model):
    name          = models.CharField(max_length=255)
    category      = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount      = models.CharField(max_length=100, blank=True)
    img_url       = models.URLField(blank=True, null=True)
    src_url       = models.URLField()
    camel_url     = models.URLField(blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


# ── USER TRACKED CATEGORIES ─────────────────────────────────

class UserTrackedCategory(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tracked_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} — {self.category.label}"

    class Meta:
        verbose_name_plural = "User Tracked Categories"
        unique_together     = ("user", "category")


# ── USER DEAL HISTORY ───────────────────────────────────────

class UserDealHistory(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deal_history")
    deal      = models.ForeignKey(Deal, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {self.deal.name}"

    class Meta:
        verbose_name_plural = "User Deal History"
        unique_together     = ("user", "deal")
        ordering            = ["-viewed_at"]


# ── NOTIFICATIONS ───────────────────────────────────────────

class NotificationChannel(models.Model):
    name = models.CharField(max_length=50, unique=True)  # email, whatsapp, sms

    def __str__(self):
        return self.name


class UserNotification(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    channel     = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)
    destination = models.CharField(max_length=255)  # email address or phone number
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {self.channel.name}"

    class Meta:
        unique_together = ("user", "channel")


# ── AUTO CREATE PROFILE ON USER CREATION ────────────────────
# This makes sure every new user gets a profile automatically

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()