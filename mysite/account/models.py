from django.db import models
from django.conf import settings


# Create your models here.

#User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name='profile')
    about = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    occupation = models.TextField()
    website = models.CharField(blank=True,max_length=250)
    twitter = models.CharField(blank=True,max_length=250)
    linkedin = models.CharField(blank=True,max_length=250)
    location = models.CharField(blank=True,max_length=250)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                              blank=True)
    def __str__(self):
        return f'Profile for user {self.user.username}'