from app.models import Product,Category,User

user = User.objects.get(username='sthvry')

categorys = Category.objects.all(user=user)

testuser = User.objects.get(username='thuralinhtutsuper')
for category in categorys:
    # Category.objects.create('')
    print(category)