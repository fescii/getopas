from itertools import product
from multiprocessing import context
import re
from django.shortcuts import render, get_object_or_404
from .models import Product, PhysicalInfo, SoftwareInfo,Review
#from .forms import EmailIssueForm,FeedbackForm
from django.core.mail import send_mail

# Create your views here.
#List All Issues
def product_list(request):
    products = Product.published.all()[:3]
    return render(request,
                  'devices/product/products.html',
                  {'products': products})