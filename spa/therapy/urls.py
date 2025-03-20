from django.urls import path, include

from therapy.views import *

urlpatterns = [
    path('', index, name='index'),
    path('add_bid/', add_bid, name='add_bid'),

]

urlpatterns += [
    path("", include("django.contrib.auth.urls")),
    path('register/', Register.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path("update_user_info/", UpdateUserInfo.as_view(), name="update_user_info"),
    path("user_login/", UserLogin.as_view(), name="user_login"),
    path(
        "user_password_reset/", UserPasswordReset.as_view(), name="user_password_reset"
    ),
    path(
        "user_password_reset_done/",
        UserPasswordResetDone.as_view(),
        name="user_password_reset_done",
    )


]
