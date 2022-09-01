from itertools import product
from multiprocessing import context
import re
from django.shortcuts import render, get_object_or_404
from .models import Product, PhysicalInfo, SoftwareInfo,Review
#from .forms import EmailIssueForm,FeedbackForm
from django.core.mail import send_mail

# Create your views here.
#List Products
def product_list(request):
    products = Product.published.all()[:3]
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

    """#List of All Sections Belonging to the current Issue
    #sections = issue.sections.filter(added=True)
    #List of active Feedbacks for current issue
    #feedbacks = issue.feedbacks.filter(active=True)
    #feedback_form = None
    #new_feedback  = None
    if user.is_authenticated:
        if request.method == 'POST':
           #A feedback was Posted
            feedback_form = FeedbackForm(data=request.POST)
            if feedback_form.is_valid():
                #Create feedback object but we're not saving it to DB yet
                new_feedback = feedback_form.save(commit=False)
                #Assigning the current user and issue to the feedback
                new_feedback.issue = issue
                new_feedback.author = user
                #Save the comment to the databases
                new_feedback.save()
            else:
                feedback_form = FeedbackForm()
        else:
            feedback_form = FeedbackForm()"""

    return render(request,
                  'devices/products/product-detail.html',
                  {'product': product,})