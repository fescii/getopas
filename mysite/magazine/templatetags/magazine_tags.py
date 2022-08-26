from django import template
from ..models import Issue
from django.db.models import Count

#Counting Total Issues
register = template.Library()
@register.simple_tag
def total_issues():
    return Issue.published.count()

#Fetching 4 recent issues
@register.inclusion_tag('magazine/issue/latest-issues.html')
def show_latest_issues(count=4):
    latest_posts = Issue.published.order_by('-publish')[:count]
    return {'latest_issues': latest_posts}

#Fetching 4 most viewed Issues
@register.inclusion_tag('magazine/issue/most-viewed-issues.html')
def show_latest_issues(count=4):
    latest_posts = Issue.published.order_by('-issue_views')[:count]
    return {'latest_issues': latest_posts}


#Fetching issues with the most feedbacks
@register.simple_tag
def get_issues_with_most_feedback(count=5):
    return  Issue.published.annotate(
        total_feedbacks=Count('feedbacks'))\
            .order_by('-total_feedbacks')[:count]


