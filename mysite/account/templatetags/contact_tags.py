from django import template
from ..models import Contact
from django.db.models import Count
from django.contrib.auth.models import User

register = template.Library()


#Check-if-user-is-following
@register.simple_tag
def check_follow(user_from,user_to):
    try:
        following = Contact.objects.get(user_from=user_from,user_to=user_to)
        if following:
            return f'Unfollow'
        else:
            return f'Follow'
    except Contact.DoesNotExist:
        return f'Follow'

#Check-if-user-is-following
@register.simple_tag
def check_following(user_from,user_to):
    try:
        user_one = User.objects.get(id=user_from)
        user_two = User.objects.get(id=user_to)
        following = Contact.objects.get(user_from=user_one,user_to=user_two)
        if following:
            return f'Unfollow'
        else:
            return f'Follow'
    except Contact.DoesNotExist:
        return f'Follow'

#Place-apostrophe
def add_apostrophe(word):
    if word[-1] == 's':
        return f"{word}'"
    else:
        return f"{word}'s"

register.filter('add_apostrophe',add_apostrophe)