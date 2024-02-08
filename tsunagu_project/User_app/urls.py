from django.urls import path,include
from User_app import views
from User_app.models import *
from django.contrib.auth import views as auth_views

urlpatterns = [
path('signup/', views.signup,name='sign-up'),
path('signin/',views.signin,name='sign-in'),
path('signout/',views.signout,name='sign-out'),
path('reset_password/',auth_views.PasswordResetView.as_view(template_name='user/password_reset_form.html'),name="reset_password"),
path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name="password_reset_done"),
path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name="password_reset_confirm"),
path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name="password_reset_complete"),

    path('profile/edit', views.EditProfile, name="editprofile"),








]