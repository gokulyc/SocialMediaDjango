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

class Connections(models.Model):
    sender=models.ForeignKey(UserDataBase,related_name='sender',on_delete=models.CASCADE,null=True,blank=True)
    receiver=models.ForeignKey(UserDataBase,related_name='receiver',on_delete=models.CASCADE,null=True,blank=True)
    status=models.CharField(max_length=30,null=True,blank=True,default='Sent')
    date=models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.sender.name+'<->'+self.receiver.name

class Company_Model(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100, blank=True,null=True)
    logo=models.ImageField(null=True,blank=True)
    number=models.CharField(max_length=100, blank=True,null=True)
    email=models.CharField(max_length=100, blank=True,null=True)
    website=models.CharField(max_length=150, blank=True,null=True)
    address=models.CharField(max_length=150, blank=True,null=True)
    title=models.CharField(max_length=50, blank=True,null=True)

    def __str__(self):
        return self.name