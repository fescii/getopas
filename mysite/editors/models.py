from distutils.command.upload import upload
from tokenize import blank_re
from django.db import models
from django.conf import settings

# Create your models here.

#User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    about = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                              blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

