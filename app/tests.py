from django.test import TestCase

# Create your tests here.
from . models import Product,Category,User

user = User.objects.get(username='sthvry')

categorys = Category.objects.filter(user=user)
products = Product.objects.filter(user=user)
testuser = User.objects.get(username='thuralinhtutsuper')

for category in categorys:
    Category.objects.create(user=testuser,title=category)
    print(category.title)

for pd in products:
    Product.objects.create(
            name=pd.name, user=testuser,price=pd.price, qty=pd.qty, description=pd.description, category=pd.category)
    print(pd.name)