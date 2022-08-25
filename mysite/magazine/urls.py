from django.urls import path
from . import views


app_name = 'magazine'

urlpatterns = [
# post views
    path('', views.issue_list, name='issue_list'),
    path('<int:year>/<int:no>/<slug:issue>/',views.post_detail, name='issue_detail'),
]