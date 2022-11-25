from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'editors'
urlpatterns = [
    #path('', include('django.contrib.auth.urls')),

    #Dashboard path
    path('home', views.dashboard, name='home'),
    path('newsletters', views.newsletters, name='newsletters'),
    path('create', views.create_options, name='create_options'),

    #Articles
    path('explore/<str:topic>', views.explore, name='explore'),
    path('explore', views.explore_topics, name='explore_topics'),
    path('feeds', views.feeds, name='feeds'),
    path('for-you', views.interest, name='interest'),
    path('trending', views.trending, name='trending'),
    path('recent', views.recent, name='recent'),
    path('my-list', views.my_list, name='my_list'),

    #Articles-actions
    path('create/article', views.create_post, name='create_post'),
    path('my-publications/', views.user_post_list, name='user_post_list'),
    path('my-drafts/', views.user_drafted_list, name='user_drafted_list'),
    path('edit-article/<int:pk>/', views.edit_blog_post, name='edit_blog_post'),
    path('edit-article/tags/<int:pk>/', views.edit_blog_post_tags, name='edit_blog_post_tags'),
    path('edit-article/cover/<int:pk>/', views.edit_blog_post_cover, name='edit_blog_post_cover'),
    path('delete-article/<int:pk>/', views.delete_post, name='delete_post'),
    path('save/', views.save_post, name='save'),
    path('like/', views.like_comment, name='like_comment'),

    #Notifications
    path('notifications', views.actions, name='actions'),
    path('notifications/read', views.read_actions, name='actions_read'),
    path('notifications/unread', views.unread_actions, name='actions_unread'),
    path('notifications/removed', views.removed_actions, name='actions_removed'),
    path('notification-action/', views.notification_action, name='notification_action'),

    #Themes
    path('themes', views.theme_list, name='theme_list'),
    path('use-theme', views.use_theme, name='use_theme'),

    #Newsletters Paths
    path('add-newsletter/', views.create_magazine, name='new_newsletter'),
    path('my-newsletters/', views.user_issue_list, name='user_issue_list'),
    path('like-newsletter/', views.like_newsletter, name='like_newsletter'),
    path('newsletters/explore/<str:topic>', views.explore_newsletter_topic, name='explore_newsletter_topic'),
    path('newsletters/popular', views.popular_newsletters, name='popular_newsletters'),
    path('newsletters/for-you', views.interest_newsletters, name='interest_newsletters'),
    path('newsletters/recent', views.recent_newsletters, name='recent_newsletters'),
    path('edit-newsletter/<int:pk>/', views.edit_newsletter, name='edit_newsletter'),
    path('edit-newsletter/cover/<int:pk>/', views.edit_newsletter_cover, name='edit_newsletter_cover'),
    path('edit-newsletter/tags/<int:pk>/', views.edit_newsletter_tags, name='edit_newsletter_tags'),
    path('delete-newsletter/<int:pk>/', views.delete_issue, name='delete_issue'),
]