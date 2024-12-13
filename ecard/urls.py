from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test

# Check if the user is an admin
def admin_required(user):
    return user.is_superuser

urlpatterns = [
    # User registration and profile-related URLs
    path('register/', views.user_registration, name='user_registration'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('verify/<int:user_id>/', views.verify_user, name='verify_user'),
    path("profile/", login_required(views.profile), name="profile"),  # Only logged-in users can access their profile

    # Admin dashboard (restricted to superusers)
    path('admin/', user_passes_test(admin_required)(views.admin_dashboard), name='admin_dashboard'),
]

# Authentication-related URLs
urlpatterns += [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
