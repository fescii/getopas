from itertools import product
from platform import release
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers  import TaggableManager
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import get_object_or_404


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
    title = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    cover = models.ImageField(upload_to='devices/%Y/%m/%d',
                              blank=True)
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

    #Updating Product
    def update_product(self, title, name, cover, model, series, company, release,price, about, *args, **kwargs):
        self.title = title
        self.name = name
        self.cover = cover
        self.model = model
        self.series = series
        self.company = company
        self.release_date = release
        self.price = price
        self.about = about
        super(Product, self).save(update_fields=['title','name','cover','model',
                                              'series','company','release_date',
                                              'price','about'], *args, **kwargs)
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


    #Updating Physical Info
    def update_physical_info(self, screen, battery, camera, ram, rom, processor,added,*args, **kwargs):
        self.screen = screen
        self.battery = battery
        self.camera = camera
        self.ram = ram
        self.rom = rom
        self.processor = processor
        self.added = added
        super(PhysicalInfo, self).save(update_fields=['screen',
                                              'battery'
                                              'camera',
                                              'ram'
                                              'rom',
                                              'processor',
                                              'added',], *args, **kwargs)

    class Meta:
        ordering = ('added',)

    """def __str__(self):
        return f'Comment By {self.name} on {self.post}'"""

class SoftwareInfo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='software_info')
    os_version = models.CharField(max_length=250)
    os_name = models.CharField(max_length=250)
    os_family = models.TextField()
    os_ui = models.CharField(max_length=250)
    other_info = models.TextField()
    added = models.BooleanField(default=False)

    #Updating Software Info
    def update_software_info(self, os_version, os_name, os_family, os_ui, other_info,added,*args, **kwargs):
        self.os_version = os_version
        self.os_name = os_name
        self.os_family = os_family
        self.os_ui = os_ui
        self.other_info = other_info
        self.added = added
        super(SoftwareInfo, self).save(update_fields=['screen',
                                              'battery'
                                              'camera',
                                              'ram'
                                              'rom',
                                              'processor',
                                              'added',], *args, **kwargs)

    class Meta:
        ordering = ('added',)

class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='devices/%Y/%m/%d',
                              blank=True)
    added = models.BooleanField(default=False)

    #Updating Software Info
    def update_image(self, photo, cover, added,*args, **kwargs):
        self.photo = photo
        self.cover = cover
        self.added = added
        super(Image, self).save(update_fields=['photo','cover','added',], *args, **kwargs)


    #Get List of Photos Excluding The Non Published Photos
    def product_images(self, product):
        photos = Image.objects.filter(product=product,
                                      added=True)
        photos = [i.photo for i in photos]
        return photos


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
        return f'Review by {self.author} on {self.product}'