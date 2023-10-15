from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

from django.utils import timezone
from datetime import datetime, timedelta


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'email',
                  'phoneno', 'password', 'address']
        write_only_fields = ('password')

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.start_d = timezone.now()
        user.end_d = timezone.now() + timedelta(days=10*365)
        user.save()

        return user


class CreateUser_SalesDigit_Serializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'phoneno', 'password']
        write_only_fields = ('password')

    def create(self, validated_data):
        user = super(CreateUser_SalesDigit_Serializer,
                     self).create(validated_data)
        user.set_password(validated_data['password'])
        user.start_d = timezone.now()
        user.end_d = timezone.now()
        user.is_salesDigits = True
        user.save()

        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category()
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product()
        fields = ['id', 'name', 'price', 'cost', 'qty',
                  'date', 'description', 'category', 'pic']


class SoldProductSerializer(serializers.ModelSerializer):
    # product_name = serializers.CharField(source='name.name')

    class Meta:
        model = models.SoldProduct()
        fields = ['id', 'name', 'price', 'profit', 'qty', 'date']


class SalesSerializer(serializers.ModelSerializer):
    sproduct = SoldProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.Sales()
        fields = ['receiptNumber','voucherNumber', 'customerName', 'sproduct', 'totalAmount', 'totalProfit', 
                  'tax', 'discount', 'grandtotal', 'deliveryCharges', 'date', 'description']


class DTSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sales()
        fields = ['grandtotal', 'date']


class OtherIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OtherIncome()
        fields = ['id', 'title', 'price', 'date', 'description']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expense()
        fields = ['id', 'title', 'price', 'date', 'description']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Purchase()
        fields = ['id', 'title', 'price', 'date', 'description']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'phoneno', 'username', 'name',
                  'profileimage', 'email', 'address', 'start_d', 'end_d', 'is_superuser', 'is_plan']


class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedBack
        fields = ['id', 'message']


class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppVersion
        fields = ['version', 'url', 'releaseNote']


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pricing
        fields = ['id', 'title', 'price', 'days', 'discount', 'is_digits']


class PricingRequestSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    rq_price = PricingSerializer(read_only=True)

    class Meta:
        model = models.PricingRequest
        fields = ['id', 'user', 'rq_price', 'date', 'done']


class TwoDigitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TwoDigits
        fields = ['id', 'number', 'amount']


class TwoDigitsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TwoDigitsGroup
        fields = ['id', 'start_datetime',
                  'luckyNumber', 'end_datetime', 'title']


class SalesTwoDigitSerializer(serializers.ModelSerializer):

    two_sales_digits = TwoDigitsSerializer(many=True, read_only=True)
    # sales_two_group = TwoDigitsGroupSerializer(many=True,read_only=True)
    luckyNumber_two = serializers.CharField(source='group.luckyNumber')
    # time    = serializers.CharField(source='group.time')

    class Meta:
        model = models.SalesTwoDigits
        fields = ['id', 'customername', 'phoneno', 'datetime',
                  'totalprice', 'two_sales_digits', 'luckyNumber_two']


class ThreeDigitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ThreeDigits
        fields = ['id', 'number', 'amount']


class ThreeDigitsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ThreeDigitsGroup
        fields = ['id', 'start_datetime',
                  'luckyNumber', 'end_datetime', 'title']


class SalesThreeDigitSerializer(serializers.ModelSerializer):

    three_sales_digits = ThreeDigitsSerializer(many=True, read_only=True)
    # sales_two_group = TwoDigitsGroupSerializer(many=True,read_only=True)
    luckyNumber_three = serializers.CharField(source='group.luckyNumber')

    class Meta:
        model = models.SalesThreeDigits
        fields = ['id', 'customername', 'phoneno', 'datetime',
                  'totalprice', 'three_sales_digits', 'luckyNumber_three']
