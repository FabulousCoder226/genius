
from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class AppInfo(models.Model):
   title = models.CharField(max_length=50)
   logo = models.ImageField(upload_to='logo')
   carousel1 = models.ImageField(upload_to='carousel')
   carousel2 = models.ImageField(upload_to='carousel')
   carousel3 = models.ImageField(upload_to='carousel')
   banner = models.ImageField(upload_to='banner')
   copyright = models.IntegerField()

   def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    pix = models.ImageField(upload_to='catpix')

    def __str__(self):
        return self.name

class Food(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    foodname = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    pix = models.ImageField(upload_to='pix') 
    price = models.IntegerField()
    promo_price = models.IntegerField(blank=True, null=True)
    special_gifts = models.BooleanField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.foodname

class Contact(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.full_name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    phone =  models.CharField(max_length=50)
    pix = models.ImageField(upload_to='customer', default='customer/avatar.png', blank=True, null=True) 

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    price = models.IntegerField()
    qty = models.IntegerField()
    paid = models.BooleanField()
    amount = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, default='b')
    amount = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    pay_code = models.CharField(max_length=50)
    additional_info = models.TextField()
    paid = models.BooleanField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username




























    # CRUD 
    # C =create (INSERT)
    # R = read(SELECT)
    # U = update (UPDATE)
    # D = delete (DELETE)