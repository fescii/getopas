from django.urls import path
from . import views

app_name = 'devices'

urlpatterns = [
# post views
    path('', views.product_list, name='product_list'),
    path('<int:year>/<slug:issue>/',views.product_detail, name='product_detail'),
    #path('<int:issue_id>/share/', views.issue_share, name='issue_share')
]