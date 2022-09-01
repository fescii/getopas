from itertools import product
from platform import release
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
class Product(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),)
    TYPE_CHOICES = (
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('other', 'Other'),)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True)
    model = models.CharField(max_length=250)
    series = models.CharField(max_length=250, default='None')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    company = models.CharField(max_length=250)
    release_date = models.DateTimeField(blank=True)
    price = models.CharField(max_length=250)
    about = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    product_views = models.IntegerField(default=0)
    tags = TaggableManager()

    #Updating Blog Post
    def update_product(self, name, model, company, release,price, about, *args, **kwargs):
        self.name = name
        self.model = model
        self.company = company
        self.release_date = release
        self.price = price
        self.about = about
        super(Product, self).save(update_fields=['name',
                                              'model',
                                              'company',
                                              'release_date',
                                              'price',
                                              'about'], *args, **kwargs)
    #Update Views
    def update_views(self, *args, **kwargs):
        self.product_views = self.product_views+1
        super(Product, self).save(*args, kwargs)

    #Overriding The Save Method
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)
    class Meta:
        ordering = ('-release_date',)
    def __str__(self):
        return self.name
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    def get_absolute_url(self):
        return reverse('devices:product_detail',
        args=[self.release_date.year,self.slug])

#Comments Model
class PhysicalInfo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='physical_info')
    screen = models.CharField(max_length=250)
    battery = models.CharField(max_length=250)
    camera = models.TextField()
    ram = models.CharField(max_length=250)
    rom = models.CharField(max_length=250)
    processor = models.TextField()
    added = models.BooleanField(default=False)

    class Meta:
        ordering = ('added',)

    """def __str__(self):
        return f'Comment By {self.name} on {self.post}'"""

class SoftwareInfo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='software_info')
    os_version = models.CharField(max_length=250)
    os_name = models.CharField(max_length=250)
    os_family = models.TextField()
    os_type = models.CharField(max_length=250)
    other_info = models.TextField()
    added = models.BooleanField(default=False)

    class Meta:
        ordering = ('added',)

#Review Model
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()
    remarks = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Feedback by {self.name} on {self.post}'