from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
    

class About(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)     
    miniTitle = models.CharField(max_length=200, blank=True, null=True) 
    content = models.TextField(null=True,blank=True)                  

    def __str__(self):
        return self.title or "About sehifesi melumatlari"
    

class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
    

class ContactInfo(models.Model):
    location = models.CharField(max_length=255, blank=True, null=True)
    location_url = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


    def __str__(self):
        return self.location or "No Location"
    

