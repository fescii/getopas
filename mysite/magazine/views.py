from django.shortcuts import render, get_object_or_404
from .models import Issue

# Create your views here.

def post_list(request):
    issues = Issue.published.all()
    return render(request, 'magazine/issue/issues.html', {'posts': issues})