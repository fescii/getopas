from django import template
from ..models import Issue


register = template.Library()
@register.simple_tag
def total_issues():
    return Issue.published.count()


@register.inclusion_tag('magazine/issue/latest-issues.html')
def show_latest_issues(count=4):
    latest_posts = Issue.published.order_by('-publish')[:count]
    return {'latest_issues': latest_posts}