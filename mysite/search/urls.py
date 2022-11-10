from django.urls import path
from . import views


app_name = 'search'

urlpatterns = [
    path('', views.query_search, name='item_search'),
    #path('newsletters/<str:search>', views.issue_search, name='issue_search'),
]