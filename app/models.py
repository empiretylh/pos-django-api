from email.policy import default
from socketserver import ThreadingUnixDatagramServer
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser, Group

from django.core.files.base import ContentFile
# Create your models here.


class User(AbstractUser):
    phoneno = models.CharField(max_length=11, null=True, blank=False)
    name = models.CharField(max_length=255,null=True)
    profileimage = models.ImageField(
        upload_to="img/profile/%y/%mm/%dd", null=True)
    email = models.CharField(max_length=255,null=True)

    address = models.TextField(blank=True, null=True)
    is_plan = models.BooleanField(default=False)

    # Sales Digits User
    is_salesDigits =models.BooleanField(default=False,null=True)
   
    start_d = models.DateTimeField(null=True)
    end_d = models.DateTimeField(null=True)

    def uploadimage(self, profileimage: str):
        temp_file = ContentFile(profileimage)
        self.profileimage.save(f'{self.pk}'.jpeg, temp_file)


class Category(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.user.username


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.CharField(max_length=30, null=False, blank=False)
    qty = models.CharField(max_length=30, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="img/product/%y/%mm/%dd", null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SoldProduct(models.Model):
    name = models.ForeignKey(Product, blank=True, null=True,
                             on_delete=models.PROTECT, related_name='soldproduct_set')
    price = models.CharField(max_length=30, null=False, blank=False)
    qty = models.CharField(max_length=30, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    sales = models.ForeignKey(
        'Sales', related_name='sproduct', on_delete=models.CASCADE)

    def __str__(self):
        return self.name.name+' '+self.price


class Sales(models.Model):
    receiptNumber = models.CharField(
        max_length=50, null=False, blank=False, primary_key=True)
    customerName = models.CharField(max_length=30, null=False, blank=False)
    totalAmount = models.CharField(max_length=20, null=False, blank=False)
    tax = models.CharField(max_length=20, null=False, blank=False)
    discount = models.CharField(max_length=20, null=False, blank=False)
    grandtotal = models.CharField(max_length=20, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.customerName + '  '+self.grandtotal + '  RN :'+self.receiptNumber


class OtherIncome(models.Model):
    title = models.CharField(max_length=255, null=True, blank=False)
    price = models.CharField(max_length=20, null=True, blank=False)
    date = models.DateField(null=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.description


class Expense(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    price = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateField(null=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.description


class Purchase(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    price = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.description


class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.user.username + ' ' + self.message


class AppVersion(models.Model):
    version = models.CharField(max_length=255, null=False)
    url = models.TextField(null=False)
    releaseNote = models.TextField()

    def __str__(self):
        return self.version


class Pricing(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=30)
    days = models.CharField(max_length=5, null=True)
    discount = models.CharField(max_length=255, null=True)
    is_digits = models.BooleanField(default=False)
    def __str__(self):
        return self.title + ' ' + self.price


class PricingRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    rq_price = models.ForeignKey(
        Pricing, on_delete=models.CASCADE, related_name='rq_price')
    date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + '-' + self.rq_price.price


def showdate(self):
    if self.is_done:
        return self.end_datetime.date().strftime("%d/%m/%Y, %H:%M:%S")
    return 'Not Done'


class ThreeDigitsGroup(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_threedigits')
    start_datetime = models.DateTimeField(auto_now_add=True)
    luckyNumber = models.CharField(max_length=3, null=True)
    is_done = models.BooleanField(default=False)
    end_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username +' ' + showdate(self)





class TwoDigitsGroup(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_twodigits')
    start_datetime = models.DateTimeField(auto_now_add=True)
    luckyNumber = models.CharField(max_length=2, null=True)
    is_done = models.BooleanField(default=False)
    end_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username + ' '+ showdate(self)



class SalesThreeDigits(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    customername = models.CharField(max_length=255, null=False)
    phoneno = models.CharField(max_length=11, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    totalprice = models.CharField(max_length=10,null=False)
     # In Group
    group = models.ForeignKey(
        ThreeDigitsGroup, on_delete=models.CASCADE, related_name='luckyNumber_three',null=True)
    
    def __str__(self):
        return self.customername 


class SalesTwoDigits(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    customername = models.CharField(max_length=255, null=False)
    phoneno = models.CharField(max_length=11, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    totalprice = models.CharField(max_length=10,null=False)
       # In Group
    group = models.ForeignKey(
        TwoDigitsGroup, on_delete=models.CASCADE, related_name='luckyNumber_two',null=True)

    def __str__(self):
      return self.customername 



class ThreeDigits(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    number = models.CharField(max_length=3, null=False)
    amount = models.CharField(max_length=255, null=False)
    sales = models.ForeignKey(SalesThreeDigits,on_delete=models.CASCADE,related_name='three_sales_digits',null=True)


    def __str__(self):
        return self.number +' ' + self.amount


class TwoDigits(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    number = models.CharField(max_length=3, null=False)
    amount = models.CharField(max_length=255, null=False)
    sales = models.ForeignKey(SalesTwoDigits,on_delete=models.CASCADE,related_name='two_sales_digits',null=True)

    def __str__(self):
        return self.number +' '+ self.amount