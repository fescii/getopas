from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers  import TaggableManager
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify

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
    no = models.IntegerField(editable=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='magazine_posts')
    description = models.TextField(editable=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', editable=True)
    cover = models.ImageField(upload_to='issues/%Y/%m/%d',
                              blank=True)
    issue_views = models.IntegerField(default=0)
    tags = TaggableManager()

    #Updating an Issue
    def update_issue(self, no, cover, title, description, status, *args, **kwargs):
        self.no = no
        self.cover = cover
        self.title = title
        self.description = description
        self.status = status
        super(Issue, self).save(update_fields=['no',
                                               'cover',
                                               'title',
                                              'description',
                                              'status'], *args, **kwargs)
    #Update Views
    def update_views(self, *args, **kwargs):
        self.issue_views =self.issue_views+1
        super(Issue, self).save(*args, kwargs)
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

    def Tag(self):
        return ",".join([str(p) for p in self.Tags.all()])

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    def get_absolute_url(self):
        return reverse('magazine:issue_detail',
                       args=[self.publish.year,
                             self.no, self.slug])
    #Overriding The Save Method
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)


#Section Model
class Section(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='sections')
    name = models.TextField(max_length=250)
    page = models.IntegerField()
    body = models.TextField()
    added = models.BooleanField(default=False)

#Feedback Model
class Feedback(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='feedbacks')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Feedback by {self.name} on {self.post}'