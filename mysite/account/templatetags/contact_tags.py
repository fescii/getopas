from django import template
from ..models import Contact
from django.db.models import Count

register = template.Library()


#Get Most commented posts
@register.simple_tag
def check_follow(user_from,user_to):
    try:
        following = Contact.objects.get(user_from=user_from,user_to=user_to)
        if following:
            return 'Unfollow'
        else:
            return 'Follow'
    except Contact.DoesNotExist:
        return 'Follow'
