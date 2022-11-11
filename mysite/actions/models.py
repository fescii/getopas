from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

# Create your models here.
class Action(models.Model):
    STATUS_CHOICES = (
        ('read', 'Read'),
        ('unread', 'Unread'),)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    user = models.ForeignKey('auth.User',related_name='actions',on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    #Update Status
    def update_status(self, status,*args, **kwargs):
        self.status = status
        super(Action, self).save(update_fields=['status'],*args, **kwargs)
    class Meta:
        indexes = [models.Index(fields=['-created']),
                   models.Index(fields=['target_ct', 'target_id']),
                   ]
        ordering = ['-created']

#User Action
class UserAction(models.Model):
    STATUS_CHOICES = (
        ('read', 'Read'),
        ('unread', 'Unread'),)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='notification')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    #Update Status
    def update_status(self, status,*args, **kwargs):
        self.status = status
        super(UserAction, self).save(update_fields=['status'],*args, **kwargs)

    #Update Delete
    def update_deleted(self, deleted,*args, **kwargs):
        self.deleted = deleted
        super(UserAction, self).save(update_fields=['deleted'],*args, **kwargs)

    def __str__(self):
        return f'Notification For {self.user}'