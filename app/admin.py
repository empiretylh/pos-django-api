from django.contrib import admin
from . import models
# Register your models here.=
admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.SoldProduct)
admin.site.register(models.Sales)
admin.site.register(models.OtherIncome)
admin.site.register(models.Expense)
admin.site.register(models.Purchase)
admin.site.register(models.FeedBack)
admin.site.register(models.AppVersion)
admin.site.register(models.Pricing)
admin.site.register(models.PricingRequest)


#Sales Digits App

admin.site.register(models.ThreeDigits)
admin.site.register(models.TwoDigits)
admin.site.register(models.ThreeDigitsGroup)
admin.site.register(models.TwoDigitsGroup)

admin.site.register(models.SalesThreeDigits)
admin.site.register(models.SalesTwoDigits)