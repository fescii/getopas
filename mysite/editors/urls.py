from re import template
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'editors'
urlpatterns = [
    #path('', include('django.contrib.auth.urls')),

    #Dashboard path
    path('', views.dashboard, name='dashboard'),

    #Articles
    path('add-article/', views.create_post, name='create_post'),
    path('my-articles/', views.user_post_list, name='user_post_list'),
    path('recent-articles/', views.new_articles, name='new_articles'),
    path('edit-article/<int:pk>/', views.edit_blog_post, name='edit_blog_post'),
    path('edit-article/tags/<int:pk>/', views.edit_blog_post_tags, name='edit_blog_post_tags'),
    path('edit-article/cover/<int:pk>/', views.edit_blog_post_cover, name='edit_blog_post_cover'),
    path('delete-article/<int:pk>/', views.delete_post, name='delete_post'),
    path('save/', views.save_post, name='save'),

    #Newsletters Paths
    path('add-newsletter/', views.create_magazine, name='new_newsletter'),
    path('top-newsletters/', views.top_newsletters, name='top_newsletters'),
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