from re import template
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

#app_name = 'editor'
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
    path('@<str:username>', views.user_profile, name='profile'),
    path('users/', views.list_users, name='list_users'),
    path('users/edit-user-<str:user_id>', views.moderate_user, name='moderate_user'),
    path('users/remove-user-<str:user_id>', views.remove_user, name='remove_user'),

    #Articles
    path('add-article/', views.create_post, name='create_post'),
    path('my-articles/', views.user_post_list, name='user_post_list'),
    path('edit-article/<int:pk>/', views.edit_blog_post, name='edit_blog_post'),
    path('edit-article/tags/<int:pk>/', views.edit_blog_post_tags, name='edit_blog_post_tags'),
    path('edit-article/cover/<int:pk>/', views.edit_blog_post_cover, name='edit_blog_post_cover'),
    path('delete-article/<int:pk>/', views.delete_post, name='delete_post'),

    #Newsletters Paths
    path('add-newsletter/', views.create_magazine, name='new_newsletter'),
    path('my-newsletters/', views.user_issue_list, name='user_issue_list'),
    path('edit-newsletter/<int:pk>/', views.edit_newsletter, name='edit_newsletter'),
    path('edit-newsletter/cover/<int:pk>/', views.edit_newsletter_cover, name='edit_newsletter_cover'),
    path('edit-newsletter/tags/<int:pk>/', views.edit_newsletter_tags, name='edit_newsletter_tags'),
    path('delete-newsletter/<int:pk>/', views.delete_issue, name='delete_issue'),
    path('my-newsletters/<int:pk>/sections', views.user_issue_section_list, name='user_issue_section_list'),
    path('my-newsletters/<int:pk>/sections/add', views.create_section, name='new_newsletter'),
    path('my-newsletters/<str:issue_id>/sections/add-section-<str:section_id>', views.add_section, name='add_section'),
    path('my-newsletters/<str:issue_id>/sections/remove-section-<str:section_id>', views.remove_section, name='remove_section'),
    path('my-newsletters/<str:issue_id>/sections/delete-section-<str:section_id>', views.delete_section, name='delete_section'),
    path('my-newsletters/<str:issue_id>/sections/edit-section-<str:section_id>', views.edit_section, name='edit_section'),

    #Products Path
    path('add-product/', views.create_product, name='new_product'),
    path('product/cover/<int:pk>/', views.edit_product_cover, name='edit_product_cover'),
    path('products/', views.user_product_list, name='user_product_list'),
    path('product/<str:product_id>/<str:product_name>/edit', views.edit_product, name='edit_product'),
    path('product/<str:product_id>/<str:product_name>/tags-edit', views.edit_product_tags, name='edit_product_tags'),
    path('product/<str:pk>/add-physical-info', views.add_physical_info, name='add_physical_info'),
    path('product/<str:pk>/add-software-info', views.add_software_info, name='add_software_info'),
    path('product/<int:pk>/delete', views.delete_product, name='delete_product'),
    path('product/<str:pk>/physical-info', views.show_physical_info, name='product_physical_info'),
    path('product/<str:pk>/software-info', views.show_software_info, name='product_software_info'),
    path('product/<str:product_id>/physical-info/edit-<str:info_id>', views.edit_physical_info, name='edit_physical_info'),
    path('product/<str:product_id>/software-info/edit<str:info_id>', views.edit_software_info, name='edit_software_info'),

    #Images
    path('product/<str:pk>/images', views.show_product_images, name='images'),
    path('product/<str:product_id>/images/add', views.add_image, name='add_image'),
    path('product/<str:product_id>/images/remove-<str:image_id>', views.delete_image, name='delete_image'),
]