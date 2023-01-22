from re import template
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

#app_name = 'account'
urlpatterns = [
    #path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    #Change password urls
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='account/templates/registration/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/templates/registration/password_change_done.html'),
         name='password_change_done'),

    # reset password urls
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='account/templates/registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/templates/registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/templates/registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/templates/registration/password_reset_complete.html'),
         name='password_reset_complete'),


    #Register urls
    path('register/', views.register, name='register'),
    path('join/', views.get_started, name='get_started'),

    #Edit user info path
    path('@<str:username>/edit', views.edit, name='edit'),
    path('@<str:username>', views.user_profile, name='profile'),
    path('@<str:username>/following/', views.following, name='following'),
    path('@<str:username>/followers/', views.followers, name='followers'),
    path('people/', views.user_list, name='user_list'),
    path('top-users/', views.top_users, name='top_users'),
    path('new-users/', views.new_users, name='new_users'),
    path('user/follow', views.user_follow, name='user_follow'),
    path('manage-users/', views.list_users, name='list_users'),
    path('users/edit-user-<str:user_id>', views.moderate_user, name='moderate_user'),
    path('users/remove-user-<str:user_id>', views.remove_user, name='remove_user'),
]