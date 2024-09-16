from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.UserLoginViews.as_view(), name="login"),
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout, name="logout"),
    path("users-cart/", views.users_cart, name="users_cart"),
]
