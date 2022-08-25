import re
from django.shortcuts import render, get_object_or_404
from .models import Issue,Feedback
from .forms import EmailIssueForm,FeedbackForm
from django.core.mail import send_mail

# Create your views here.

#List All Issues
def issue_list(request):
    issues = Issue.published.all()[:3]
    return render(request,
                  'magazine/issue/issues.html',
                  {'issues': issues})


def issue_detail(request, year, no, issue):
    issue = get_object_or_404(Issue,
                             slug=issue,
                             status='published',
                             publish__year=year,
                             no = no)

    #List of active Feedbacks for current issue
    feedbacks = issue.feedbacks.filter(active=True)

    new_feedback  = None

    if request.method == 'POST':
        #A feedback was Posted
        feedback_form = FeedbackForm(data=request.POST)
        if feedback_form.is_valid():
            #Create feedback object but we're not saving it to DB yet
            new_feedback = feedback_form.save(commit=False)
            #Assigning the current issue to the feedback
            new_feedback.issue = issue
            #Saving the feedback object to the Database
            new_feedback.save()
    else:
        feedback_form = FeedbackForm()

    return render(request,
                  'magazine/issue/issue-detail.html',
                  {'issue': issue,
                   'feedbacks':feedbacks,
                  'new_feedback': new_feedback,
                  'feedback_form':feedback_form})

#Share Issue By E-mail
def issue_share(request, issue_id):
    #Retrieving Issue by id
    issue = get_object_or_404(Issue, id=issue_id, status='published')
    sent = False
    #Checking the request method
    if request.method == 'POST':
        #Then form was submitted
        form = EmailIssueForm(request.POST)
        #Checking if the form submitted is valid
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            #...Send Email
            post_url = request.build_absolute_uri(issue.get_absolute_url())
            subject = f"{cd['name']} recommends you read "\
                        f"{issue.title}"
            message = f"Read {issue.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailIssueForm()

    return render(request, 'magazine/issue/share.html',
                  {'issue': issue,
                   'form':form,
                   'sent':sent})