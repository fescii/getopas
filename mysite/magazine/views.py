from django.shortcuts import render, get_object_or_404
from .models import Issue

# Create your views here.

#List All Issues
def issue_list(request):
    issues = Issue.published.all()
    return render(request,
                  'magazine/issue/issues.html',
                  {'posts': issues})


def issue_detail(request, year, no, issue):
    issue = get_object_or_404(Issue,
                             slug=issue,
                             status='published',
                             publish__year=year,
                             no = no)
    return render(request,
                  'magazine/issue/issue-detail.html',
                  {'issue': issue})