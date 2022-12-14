import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action,UserAction


def create_action(user, verb,type, target=None):
    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb= verb,
                                            created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)
    if not similar_actions:
        # no existing actions found
        action = Action(user=user,
                        verb=verb,
                        type=type,
                        target=target)
        action.save()
        return True
    return False

def create_user_action(action, user,status, deleted=False):
    # check for any similar action made in the last minute
    similar_actions = UserAction.objects.filter(user=user,
                                            action= action)
    if not similar_actions:
        # no existing actions found
        user_action = UserAction(action=action,
                        user=user,
                        status=status,
                        deleted=deleted)
        user_action.save()
        return True
    return False