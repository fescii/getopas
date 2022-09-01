import email
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers  import TaggableManager
from django.conf import settings
from django.utils.text import slugify

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
        .filter(status='published')
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    blog_views = models.IntegerField(default=0)
    tags = TaggableManager()

    #Updating Blog Post
    def update_post(self, title, body, status, *args, **kwargs):
        self.title = title
        self.body = body
        self.status = status
        super(Post, self).save(update_fields=['title',
                                              'body',
                                              'status'], *args, **kwargs)
    #Update Views
    def update_views(self, *args, **kwargs):
        self.blog_views =self.blog_views+1
        super(Post, self).save(*args, kwargs)
    #Overriding The Save Method
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    def get_absolute_url(self):
        return reverse('blog:post_detail',
        args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

#Comments Model
class BlogComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment By {self.name} on {self.post}'