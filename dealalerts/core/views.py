from django.shortcuts import render

# Create your views here.
# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta

from .models import (
    Deal,
    Category,
    UserTrackedCategory,
    UserDealHistory,
    UserNotification,
    NotificationChannel,
    Plan,
)


# ── LANDING ─────────────────────────────────────────────────

def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/landing.html")


# ── REGISTER ────────────────────────────────────────────────

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name  = request.POST.get("last_name")
        email      = request.POST.get("email")
        password1  = request.POST.get("password1")
        password2  = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "core/register.html", {"form": request.POST})

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "core/register.html", {"form": request.POST})

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "core/register.html", {"form": request.POST})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )

        # Assign free plan
        free_plan        = Plan.objects.get(name="free")
        user.profile.plan = free_plan
        user.profile.save()

        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("onboarding")

    return render(request, "core/register.html", {"form": {}})


# ── LOGIN ────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email    = request.POST.get("email")
        password = request.POST.get("password")
        user     = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            # Redirect to next page if it exists, otherwise dashboard
            next_url = request.GET.get("next", "dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "core/login.html", {"form": request.POST})

    return render(request, "core/login.html", {"form": {}})


# ── LOGOUT ──────────────────────────────────────────────────

@login_required
def logout_view(request):
    logout(request)
    return redirect("landing")


# ── ONBOARDING ──────────────────────────────────────────────

@login_required
def onboarding(request):
    categories = Category.objects.all()

    if request.method == "POST":
        selected_values = request.POST.getlist("categories")

        for value in selected_values:
            category = Category.objects.get(value=value)
            UserTrackedCategory.objects.get_or_create(user=request.user, category=category)

        return redirect("dashboard")

    return render(request, "core/onboarding.html", {
        "categories": categories,
    })


# ── DASHBOARD ───────────────────────────────────────────────

@login_required
def dashboard(request):
    user               = request.user
    tracked_categories = UserTrackedCategory.objects.filter(user=user).select_related("category")
    tracked_ids        = tracked_categories.values_list("category_id", flat=True)
    deals              = Deal.objects.filter(category_id__in=tracked_ids).order_by("-created_at")
    deal_history       = UserDealHistory.objects.filter(user=user).select_related("deal__category").order_by("-viewed_at")
    user_categories    = Category.objects.filter(id__in=tracked_ids)

    # Week stats
    week_ago   = timezone.now() - timedelta(days=7)
    week_deals = Deal.objects.filter(created_at__gte=week_ago, category_id__in=tracked_ids)

    return render(request, "core/dashboard.html", {
        "deals":              deals,
        "tracked_categories": tracked_categories,
        "deal_history":       deal_history,
        "categories":         user_categories,
        "active_deal_count":  deals.count(),
        "total_saved":        0,       # hook up later
        "price_alert_count":  0,       # hook up later
        "week_stats": {
            "new_deals":          week_deals.count(),
            "notifications_sent": 0,   # hook up later
            "avg_discount":       0,   # hook up later
        },
    })


# ── ADD TO HISTORY ───────────────────────────────────────────

@login_required
@require_POST
def add_to_history(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    UserDealHistory.objects.get_or_create(user=request.user, deal=deal)
    return JsonResponse({"status": "ok"})


# ── PRICING ──────────────────────────────────────────────────

def pricing(request):
    plans = Plan.objects.all().order_by("price")
    return render(request, "core/pricing.html", {
        "plans": plans,
    })


# ── SETTINGS ─────────────────────────────────────────────────

@login_required
def settings_view(request):
    user           = request.user
    all_categories = Category.objects.all()
    tracked_values = UserTrackedCategory.objects.filter(
        user=user
    ).values_list("category__value", flat=True)

    for category in all_categories:
        category.is_tracked = category.value in tracked_values

    threshold_options = [
        (10, "10% or more"),
        (20, "20% or more"),
        (30, "30% or more"),
        (40, "40% or more"),
        (50, "50% or more"),
    ]

    notifications = {
        "email":    UserNotification.objects.filter(user=user, channel__name="email",    is_active=True).exists(),
        "sms":      UserNotification.objects.filter(user=user, channel__name="sms",      is_active=True).exists(),
        "whatsapp": UserNotification.objects.filter(user=user, channel__name="whatsapp", is_active=True).exists(),
    }

    return render(request, "core/settings.html", {
        "user":              user,
        "all_categories":    all_categories,
        "threshold_options": threshold_options,
        "notifications":     notifications,
        "next_billing_date": "N/A",   # hook up Stripe later
        "payment_method":    None,    # hook up Stripe later
        "billing_history":   [],      # hook up Stripe later
        "plan_features": [
            f"Up to {user.profile.plan.max_tracked_categories} tracked categories",
            "Email notifications",
            "Instant deal alerts",
        ],
    })


@login_required
def settings_profile(request):
    if request.method == "POST":
        user            = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name  = request.POST.get("last_name")
        user.email      = request.POST.get("email")
        user.username   = request.POST.get("email")
        user.save()

        user.profile.phone = request.POST.get("phone")
        user.profile.save()

        messages.success(request, "Profile updated successfully.")
    return redirect("settings")


@login_required
def settings_password(request):
    if request.method == "POST":
        user             = request.user
        current_password = request.POST.get("current_password")
        new_password1    = request.POST.get("new_password1")
        new_password2    = request.POST.get("new_password2")

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
        elif len(new_password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully.")

    return redirect("settings")


@login_required
def settings_categories(request):
    if request.method == "POST":
        user            = request.user
        selected_values = request.POST.getlist("categories")

        # Check plan limit
        if len(selected_values) > user.profile.plan.max_tracked_categories:
            messages.error(request, f"Your plan allows a maximum of {user.profile.plan.max_tracked_categories} categories.")
            return redirect("settings")

        # Remove all and re-add selected
        UserTrackedCategory.objects.filter(user=user).delete()
        for value in selected_values:
            category = Category.objects.get(value=value)
            UserTrackedCategory.objects.create(user=user, category=category)

        messages.success(request, "Categories updated successfully.")
    return redirect("settings")


@login_required
def settings_notifications(request):
    if request.method == "POST":
        user     = request.user
        channels = ["email", "sms", "whatsapp"]

        for channel_name in channels:
            channel  = NotificationChannel.objects.get(name=channel_name)
            is_active = channel_name in request.POST

            notification, created = UserNotification.objects.get_or_create(
                user=user,
                channel=channel,
                defaults={"destination": user.email, "is_active": is_active}
            )
            if not created:
                notification.is_active = is_active
                notification.save()

        messages.success(request, "Notification preferences updated.")
    return redirect("settings")


@login_required
def settings_threshold(request):
    if request.method == "POST":
        threshold            = request.POST.get("threshold", 20)
        request.user.profile.alert_threshold = int(threshold)
        request.user.profile.save()
        messages.success(request, "Alert threshold updated.")
    return redirect("settings")


@login_required
def settings_frequency(request):
    if request.method == "POST":
        profile              = request.user.profile
        profile.instant_alerts = "instant_alerts" in request.POST
        profile.daily_digest   = "daily_digest"   in request.POST
        profile.digest_time    = request.POST.get("digest_time", "09:00")
        profile.save()
        messages.success(request, "Notification frequency updated.")
    return redirect("settings")


# ── CANCEL SUBSCRIPTION ──────────────────────────────────────

@login_required
@require_POST
def cancel_subscription(request):
    # Hook up Stripe later
    free_plan             = Plan.objects.get(name="free")
    request.user.profile.plan = free_plan
    request.user.profile.save()
    messages.success(request, "Subscription cancelled. You've been moved to the free plan.")
    return redirect("settings")


# ── DOWNLOAD INVOICE ─────────────────────────────────────────

@login_required
def download_invoice(request, id):
    # Hook up Stripe later
    messages.info(request, "Invoice download coming soon.")
    return redirect("settings")