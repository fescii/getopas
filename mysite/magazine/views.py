from django.shortcuts import render, get_object_or_404
from .models import Issue
from .forms import EmailIssueForm
from django.core.mail import send_mail

# Create your views here.

#List All Issues
def issue_list(request):
    issues = Issue.published.all()
    return render(request,
                  'magazine/issue/issues.html',
                  {'issues': issues})


def issue_detail(request, year, no, issue):
    issue = get_object_or_404(Issue,
                             slug=issue,
                             status='published',
                             publish__year=year,
                             no = no)
    return render(request,
                  'magazine/issue/issue-detail.html',
                  {'issue': issue})


#Share Issue By E-mail
def issue_share(request, issue_id):
    #Retrieving Issue by id
    issue = get_object_or_404(Issue,
                              id=issue_id,
                              status='published')
    sent = False

    #Checking the request method
    if request == 'POST':
        #Then form was submitted
        form = EmailIssueForm(request.POST)
        #Checking if the form submitted is valid
        if form.is_valid():
            #Form fields passed validation
            form_data = form.cleaned_data
            #...Send Mail
            issue_url = request.build_absolute_uri(issue.get_absolute_url())
            subject = f"{form_data['name']} recommends you read "\
                       f"{issue.title}"
            message = f"Read {issue.title} at {issue_url}\n\n" \
                      f"{form_data['name']}\s comments: {form_data['comments']}"
            send_mail(subject, message, 'admin@opus.com', [form_data['to']])
            sent = True
    else:
        form = EmailIssueForm()

    return render(request, 'magazine/issue/share.html',
                  {'issue': issue,
                   'form':form,
                   'sent':sent})