from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers  import TaggableManager
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from django.db.models import Count

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', editable=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    title = models.CharField(max_length=250)
    owner = models.CharField(max_length=250)
    release = models.CharField(max_length=250)
    description = models.TextField(editable=True)
    platform = models.CharField(max_length=250)
    cover = models.ImageField(upload_to='issues/%Y/%m/%d',
                              blank=True)
    issue_views = models.IntegerField(default=0)
    link = models.CharField(max_length=1000)
    tags = TaggableManager()

    #Updating an Issue
    def update_issue(self,title,owner,release, description,platform, status,link, *args, **kwargs):
        self.title = title
        self.owner = owner
        self.release = release
        self.description = description
        self.platform = platform
        self.status = status
        self.link = link
        super(Issue, self).save(update_fields=['title','owner','release',
                                              'description','platform',
                                              'status','link',], *args, **kwargs)
    #Update Views
    def update_views(self, *args, **kwargs):
        self.issue_views =self.issue_views+1
        super(Issue, self).save(*args, kwargs)

     #Update Cover
    def update_cover(self, cover,*args, **kwargs):
        self.cover = cover
        super(Issue, self).save(update_fields=['cover'],*args, **kwargs)

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
                       args=[self.id, self.slug])
    #Overriding The Save Method
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)

    #Recently added Posts
    def recently_added(self, count):
        issues = Issue.published.order_by('-publish')[:count]
        return issues

    #Most Viewed Posts
    def most_liked(self, count):
        issues = Issue.published.annotate(total_comments = Count('issue_likes')).order_by('-total_comments')[:count]
        return issues


#Section Model
class Issue_likes(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_users_likes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'{self.user} likes {self.issue}'


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