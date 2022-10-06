from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from account.models import Profile
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
    cover = models.ImageField(upload_to='articles/%Y/%m/%d',
                              blank=True)
    tags = TaggableManager()

    users_save = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='posts_saved',blank=True)


    #Updating Blog Post
    def update_post(self, title, body, status, *args, **kwargs):
        self.title = title
        self.body = body
        self.status = status
        super(Post, self).save(update_fields=['title','body',
                                              'status'], *args, **kwargs)
    #Update Views
    def update_views(self, *args, **kwargs):
        self.blog_views =self.blog_views+1
        super(Post, self).save(*args, kwargs)

    #Update Cover
    def update_cover(self, cover,*args, **kwargs):
        self.cover = cover
        super(Post, self).save(update_fields=['cover'],*args, **kwargs)

    #Overriding The Save Method
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)

    #Most Viewed Posts
    def most_viewed(self, count=5):
        posts = Post.published.order_by('-blog_views')[:count]
        return posts

    #Recently added Posts
    def recently_added(self, count):
        posts = Post.published.order_by('-publish')[:count]
        return posts


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


    def __str__(self):
        return f'Saved By {self.name} on {self.post}'


#Bookmark Model
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='saved')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('added',)
    # Save Article
    def save_article(self,post, user,*args, **kwargs):
        self.post = post
        self.user = user
        super(Bookmark, self).save(update_fields=['post','user'],*args, **kwargs)

    def __str__(self):
        return f'Saved By {self.user} on {self.post}'