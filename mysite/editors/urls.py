from re import template
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    #path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    #Change password urls
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='editors/templates/registration/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='editors/templates/registration/password_change_done.html'),
         name='password_change_done'),

    # reset password urls
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='editors/templates/registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='editors/templates/registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='editors/templates/registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='editors/templates/registration/password_reset_complete.html'),
         name='password_reset_complete'),
    #Register urls
    path('register/', views.register, name='register'),
    #Dashboard path
    path('', views.dashboard, name='dashboard'),
    #Edit user info path
    path('edit-info/', views.edit, name='edit'),
    path('add-article/', views.create_post, name='create_post'),
    path('my-articles/', views.user_post_list, name='user_post_list'),
    path('edit-article/<int:pk>/', views.edit_blog_post, name='edit_blog_post'),
]