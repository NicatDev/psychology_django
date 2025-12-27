from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    active_test_count = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(null=True,blank=True)
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []       

    objects = CustomUserManager()
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Əgər username boşdursa və ya None-dırsa, email-i ona mənimsət
        if not self.username:
            self.username = self.email
        
        super().save(*args, **kwargs)
    

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
    

class Plan(models.Model):
    title = models.CharField(max_length=100)               # "Standard", "Medium", "Pro"
    tests_count = models.PositiveIntegerField(default=1)   # neçə test daxil olduğu
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    customerPrice = models.DecimalField(max_digits=10, decimal_places=2)  
    currency = models.CharField(max_length=10, default='$')
    short_description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.title} ({self.price} {self.currency})"
    


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="blogs")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.title
