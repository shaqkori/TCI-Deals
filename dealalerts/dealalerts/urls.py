"""
URL configuration for dealalerts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("",                          views.landing,                name="landing"),
    path("register/",                 views.register,               name="register"),
    path("login/",                    views.login_view,             name="login"),
    path("logout/",                   views.logout_view,            name="logout"),
    path("onboarding/",               views.onboarding,             name="onboarding"),
    path("dashboard/",                views.dashboard,              name="dashboard"),
    path("pricing/",                  views.pricing,                name="pricing"),
    path("settings/",                 views.settings_view,          name="settings"),
    path("settings/profile/",         views.settings_profile,       name="settings_profile"),
    path("settings/password/",        views.settings_password,      name="settings_password"),
    path("settings/categories/",      views.settings_categories,    name="settings_categories"),
    path("settings/notifications/",   views.settings_notifications, name="settings_notifications"),
    path("settings/threshold/",       views.settings_threshold,     name="settings_threshold"),
    path("settings/frequency/",       views.settings_frequency,     name="settings_frequency"),
    path("cancel-subscription/",      views.cancel_subscription,    name="cancel_subscription"),
    path("invoices/<int:id>/",         views.download_invoice,       name="download_invoice"),
    path("deals/<int:deal_id>/history/", views.add_to_history,      name="add_to_history"),
]