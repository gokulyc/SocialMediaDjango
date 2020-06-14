from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserDataBase(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    dob=models.DateField(null=True,blank=True)
    location=models.CharField(max_length=100,null=True,blank=True)
    degree=models.CharField(max_length=100,null=True,blank=True)
    website=models.CharField(max_length=100,null=True,blank=True)
    experiance=models.CharField(max_length=100,null=True,blank=True)
    company=models.CharField(max_length=100,null=True,blank=True)
    profile_title = models.CharField(max_length=100, null=True, blank=True)

    # social Links

    facebook_url=models.CharField(max_length=150,null=True,blank=True)
    twitter_url=models.CharField(max_length=150,null=True,blank=True)
    google_url=models.CharField(max_length=150,null=True,blank=True)
    linkdin_url=models.CharField(max_length=150,null=True,blank=True)


    def __str__(self):
        return self.name