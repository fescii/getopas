from django.db import models
#from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField
from django.conf import settings
from django.contrib.auth import get_user_model


# Create your models here.

#User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name='profile')
    about = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    occupation = models.CharField(blank=True,max_length=250)
    website = models.CharField(blank=True,max_length=250)
    twitter = models.CharField(blank=True,max_length=250)
    linkedin = models.CharField(blank=True,max_length=250)
    location = models.CharField(blank=True,max_length=250)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                              blank=True)
    def __str__(self):
        return f'Profile for user {self.user.username}'

    def update_profile_picture(self, photo, *args, **kwargs):
        self.photo = photo
        super(Profile, self).save(update_fields=['photo'], *args, **kwargs)


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',related_name='rel_from_set',on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',related_name='rel_to_set',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


     # follow User
    def follow(self,user_from,user_to,*args, **kwargs):
        self.user_from = user_from
        self.user_to = user_to
        super(Contact, self).save(update_fields=['user_from','user_to'],*args, **kwargs)
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            ]
        ordering = ['-created']
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('following',models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))


#Preferences
class Theme(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name='user_themes')
    preferences = JSONField()
    theme_users = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    #Update users
    def update_users(self, *args, **kwargs):
        self.theme_users =self.theme_users+1
        super(Theme, self).save(*args, kwargs)

class UserTheme(models.Model):
    theme = models.ForeignKey(Theme,on_delete=models.CASCADE,related_name='current_theme')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name='user_current_theme')

    def __str__(self):
        return f'{self.creator} uses {self.theme}'

    #Set/Update Theme
    def update_user_theme(self,theme,user,*args, **kwargs):
        self.theme = theme
        self.user = user
        super(UserTheme, self).save(update_fields=['theme','user'],*args, **kwargs)