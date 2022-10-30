from django.urls import path
from . import views

app_name = 'magazine'

urlpatterns = [
# post views
    path('', views.issue_list, name='issue_list'),
    path('<int:id>/<slug:issue>/',views.issue_detail, name='issue_detail'),
    path('<int:issue_id>/share/', views.issue_share, name='issue_share')
]