from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    '''
    Date_Of_Birth = models.DateTimeField(auto_now_add=True,default=None)
    city = models.CharField(max_length=20,default='---')
    state = models.CharField(max_length=30,default='---')
    country = models.CharField(max_length=20,default='---')
    '''
    def __str__(self):
        return f' {self.user.username} Profile'

