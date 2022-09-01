from itertools import product
from multiprocessing import context
import re
from django.shortcuts import render, get_object_or_404
from .models import Product, PhysicalInfo, SoftwareInfo,Review
from .forms import ReviewForm
from django.core.mail import send_mail

# Create your views here.
#List Products
def product_list(request):
    products = Product.published.all()
    return render(request,
                  'devices/products/products.html',
                  {'products': products})

#Product Detail Page
def product_detail(request, year, product):
    product = get_object_or_404(Product,
                             status='published',
                             release_date__year=year)
    #Get The Current User
    user = request.user

    #Update Views count on each visit
    if product:
        product.update_views()
    #List of active Reviews for current product
    reviews = product.reviews.filter(active=True)

    #Adding New Review
    review_form = None
    new_review  = None

    #Allow Only Registered Users To Enter Reviews
    if user.is_authenticated:
        if request.method == 'POST':
           #A feedback was Posted
            review_form = ReviewForm(data=request.POST)
            if feedback_form.is_valid():
                #Create feedback object but we're not saving it to DB yet
                new_review = feedback_form.save(commit=False)
                #Assigning the current user and issue to the feedback
                new_review.product = product
                new_review.author = user
                #Save the comment to the databases
                new_review.save()
            else:
                feedback_form = ReviewForm()
        else:
            feedback_form = ReviewForm()
    """#List of All Sections Belonging to the current Issue
    #sections = issue.sections.filter(added=True)"""

    return render(request,
                  'devices/products/product-detail.html',
                  {'product': product,
                   'review_form':review_form})