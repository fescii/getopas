from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers  import TaggableManager
from django.urls import reverse

# Create your models here.
#Creating Our own Manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='published')

#Creating Issues Manager
class Issue(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),)
    no = models.IntegerField()
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='magazine_posts')
    description = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    tags = TaggableManager()
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('magazine:issue_detail',
                       args=[self.publish.year,
                             self.no, self.slug])

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

#Feedback Model
class Feedback(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='feedbacks')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Feedback by {self.name} on {self.post}'