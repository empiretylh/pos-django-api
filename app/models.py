from django.db import models
from django.contrib.auth.models import AbstractUser,Group

from django.core.files.base import ContentFile
# Create your models here.

class User(AbstractUser):
    phoneno = models.CharField(max_length=11,null=False,blank=False)
    name = models.CharField(max_length=255)
    profileimage = models.ImageField(upload_to="img/profile/%y/%mm/%dd",null=True)
    email = models.CharField(max_length=255)
    
    address = models.TextField(blank=True,null=True)
    start_d = models.DateTimeField(null=True)
    end_d = models.DateTimeField(null=True)
    
    def uploadimage(self,profileimage:str):
        temp_file = ContentFile(profileimage)
        self.profileimage.save(f'{self.pk}'.jpeg,temp_file)

class Category(models.Model):
    title =  models.CharField(max_length=255,null=False,blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title +' '+ self.user.username

class Product(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False)
    price = models.CharField(max_length=30,null=False,blank=False)
    qty = models.CharField(max_length=30,null=False,blank=False)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="img/product/%y/%mm/%dd",null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class SoldProduct(models.Model):
    name = models.ForeignKey(Product,blank=True, null=True,on_delete=models.PROTECT,related_name='soldproduct_set')
    price = models.CharField(max_length=30,null=False,blank=False)
    qty = models.CharField(max_length=30,null=False,blank=False)
    date = models.DateTimeField(auto_now_add=True)    
    sales =  models.ForeignKey('Sales',related_name='sproduct',on_delete=models.CASCADE)
    def __str__(self):
        return self.name.name+' '+self.price

class Sales(models.Model):
    receiptNumber = models.CharField(max_length=50,null=False,blank=False,primary_key=True)
    customerName = models.CharField(max_length=30,null=False,blank=False)
    totalAmount = models.CharField(max_length=20,null=False,blank=False)
    tax = models.CharField(max_length=20,null=False,blank=False)
    discount = models.CharField(max_length=20,null=False,blank=False)
    grandtotal = models.CharField(max_length=20,null=False,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description =  models.TextField(blank=True,null=True)

    def __str__(self):
        return self.customerName + '  '+self.grandtotal + '  RN :'+self.receiptNumber




class OtherIncome(models.Model):
    title = models.CharField(max_length=255,null=False,blank=False)
    price = models.CharField(max_length=20,null=False,blank=False)
    date = models.DateField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
   

    def __str__(self):
        return self.title +' ' + self.description



class Expense(models.Model):
    title = models.CharField(max_length=255,null=False,blank=False)
    price = models.CharField(max_length=20,null=False,blank=False)
    date = models.DateField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
   

    def __str__(self):
        return self.title +' ' + self.description


class Purchase(models.Model):
    title = models.CharField(max_length=255,null=False,blank=False)
    price = models.CharField(max_length=20,null=False,blank=False)
    date = models.DateField()
    description = models.TextField(blank=True) 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
   


    def __str__(self):
        return self.title +' ' + self.description

class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True,null=False)

    def __str__(self):
        return self.user + ' '+ self.message

class AppVersion(models.Model):
    version = models.CharField(max_length=255,null=False)
    url = models.TextField(null=False)
    releaseNote = models.TextField()

    def __str__(self):
        return self.version

    
