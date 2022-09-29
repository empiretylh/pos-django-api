import operator
import functools
import collections
from collections import OrderedDict
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model


from . import models, serializers

import json


class CreateUserApiView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = serializers.CreateUserSerializer

    def post(self, request):
        print('posteed')
        print(request.data)
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        self.perform_create(serializers)
        headers = self.get_success_headers(serializers.data)

        # Create a token than will be used for future auth
        token = Token.objects.create(user=serializers.instance)
        token_data = {'token': token.key}

        return Response(
            {**serializers.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers)


class Category(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        user = get_user_model().objects.get(username=request.user)
        data = models.Category.objects.filter(user=user)
        s = serializers.CategorySerializer(data, many=True)

        return Response(s.data)

    def post(self, request):
        user = get_user_model().objects.get(username=request.user)
        models.Category.objects.create(title=request.data['title'], user=user)
        return Response(status=status.HTTP_201_CREATED)


class Product(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        user = get_user_model().objects.get(username=request.user)
        data = models.Product.objects.filter(user=user)
        s = serializers.ProductSerializer(data, many=True)
        return Response(s.data)

    def post(self, request):
        name = request.data['name']
        price = request.data['price']
        qty = request.data['qty']

        description = request.data['description']
        category = models.Category.objects.get(id=request.data['category'])
        user = get_user_model().objects.get(username=request.user)
        pic = request.data['pic']
        models.Product.objects.create(
            name=name, user=user, pic=pic, price=price, qty=qty, description=description, category=category)
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request):
        id = request.data['id']
        user = get_user_model().objects.get(username=request.user)
        name = request.data['name']
        price = request.data['price']
        qty = request.data['qty']
        pic = request.data['pic']

        description = request.data['description']
        category = models.Category.objects.get(
            id=request.data['category'], user=user)

        PRODUCTS = models.Product.objects.get(user=user, id=id)
        PRODUCTS.name = name
        PRODUCTS.price = price
        PRODUCTS.qty = qty
        # PRODUCTS.date = date
        PRODUCTS.description = description
        PRODUCTS.category = category
        print(pic)

        if not pic == 'null':
            PRODUCTS.pic = pic

        PRODUCTS.save()

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        id = request.data['id']
        user = get_user_model().objects.get(username=request.user)

        PRODUCTS = models.Product.objects.get(user=user, id=id)
        PRODUCTS.delete()
        return Response(status=status.HTTP_201_CREATED)


def yearGenerator(self, data, strftime='%b'):
    result = {}
    # monthString = ['0','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    # 2022-09-06 18:50:44.169216+00:00

    for item in data:
        d = datetime.strptime(str(item.date)[0:19], "%Y-%m-%d %H:%M:%S")
        month_name = d.strftime(strftime)
        add_price = float(item.grandtotal) - float(item.tax)
        result[month_name] = result.get(month_name, 0) + int(add_price)

    return result


def monthGenerator(self, data):
    result = {}
    # monthString = ['0','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    # 2022-09-06 18:50:44.169216+00:00

    for item in data:
        d = datetime.strptime(str(item.date)[0:19], "%Y-%m-%d %H:%M:%S")
        name = d.strftime('%x')
        result[name] = result.get(name, 0) + int(float(item.grandtotal))

    return result


def todayGenerator(self, data):
    result = {}
    # monthString = ['0','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    # 2022-09-06 18:50:44.169216+00:00

    for item in data:
        d = datetime.strptime(str(item.date)[0:19], "%Y-%m-%d %H:%M:%S")
        name = d.strftime('%I:%M %p')
        result[name] = result.get(name, 0) + int(float(item.grandtotal))

    return result


class Sales(APIView):
    # permission_classes = [AllowAny]P

    def get(self, request):
        type = request.GET.get('type')
        time = request.GET.get('time')
        user = get_user_model().objects.get(username=request.user)
        d = datetime.now()
        chartdata = {}

        if time == 'today':
            data = models.Sales.objects.filter(user=user, date__year=str(
                d.year), date__month=str(d.month), date__day=str(d.day))
            chartdata = todayGenerator(self, data)
        elif time == 'month':
            data = models.Sales.objects.filter(
                user=user, date__year=str(d.year), date__month=str(d.month))
            chartdata = monthGenerator(self, data)
        elif time == 'year':
            data = models.Sales.objects.filter(
                user=user, date__year=str(d.year))
            chartdata = yearGenerator(self, data)
        elif time == 'custom':
            start_date = request.GET.get('startd')
            end_date = request.GET.get('endd')
            sd = datetime.strptime(start_date, "%m/%d/%y")
            ed = datetime.strptime(
                end_date, "%m/%d/%y").replace(hour=11, minute=59, second=59)
            data = models.Sales.objects.filter(user=user, date__range=(sd, ed))
            chartdata = monthGenerator(self, data)
        else:
            data = models.Sales.objects.filter(user=user)

        if type == 'DT':
            s = serializers.DTSalesSerializer(data, many=True)
        else:
            s = serializers.SalesSerializer(data, many=True)

        CombineData = {
            'DATA': s.data,
            'CHART_LABEL': chartdata.keys(),
            'CHART_DATA': chartdata.values(),
        }

        return Response(CombineData)

    def post(self, request):

        receiptNumber = request.data['receiptNumber']
        customerName = request.data['customerName']
        products = request.data['products']
        totalAmount = request.data['totalAmount']
        tax = request.data['tax']
        discount = request.data['discount']
        grandtotal = request.data['grandtotal']
        description = request.data['description']
        # date = request.data['date']
        user = get_user_model().objects.get(username=request.user)
        S = models.Sales.objects.create(user=user, receiptNumber=receiptNumber, customerName=customerName,
                                        totalAmount=totalAmount, tax=tax, discount=discount, grandtotal=grandtotal, description=description)

        print(products)
        p = json.loads(products)
        print(p)
        for b in p:
            print(b)
            product = models.Product.objects.get(id=b['name'], user=user)
            product.qty = int(product.qty) - int(b['qty'])
            product.save()

            a = models.SoldProduct.objects.create(
                name=product, price=b['price'], qty=b['qty'], sales=S)
            print(a)

        S.save()

        return Response(status=status.HTTP_201_CREATED)


class SoldProduct(APIView):

    def get(self, request):
        rn = request.GET.get['receiptNumber']

        user = get_user_model().objects.get(username=request.user)
        S = models.Sales.objects.get(user=user, receiptNumber=rn)
        seri = serializers.SoldProductSerializer(S.products.all(), many=True)
        return Response(seri.data)


class TopProductsView(APIView):

    def get(self, request):
        time = request.GET.get('time')
        user = get_user_model().objects.get(username=request.user)
        d = datetime.now()

        if time == 'today':
            data = models.SoldProduct.objects.filter(name__user=user, date__year=str(
                d.year), date__month=str(d.month), date__day=str(d.day))

        elif time == 'month':
            data = models.SoldProduct.filter(
                name__user=user, date__year=str(d.year), date__month=str(d.month))

        elif time == 'year':
            data = models.SoldProduct.objects.filter(
                name__user=user, date__year=str(d.year))

        elif time == 'custom':
            start_date = request.GET.get('startd')
            end_date = request.GET.get('endd')
            sd = datetime.strptime(start_date, "%m/%d/%y")
            ed = datetime.strptime(
                end_date, "%m/%d/%y").replace(hour=11, minute=59, second=59)
            data = models.SoldProduct.objects.filter(
                name__user=user, date__range=(sd, ed))

        else:
            data = models.SoldProduct.objects.filter(name__user=user)

        topmoneyproduct = {}
        topfreqsellproduct = {}

        for item in data:
            topmoneyproduct[item.name.name] = topmoneyproduct.get(
                item.name.name, 0) + int(float(item.price))
            topfreqsellproduct[item.name.name] = topfreqsellproduct.get(
                item.name.name, 0) + 1

        CombineData = {
            'T_Money': topmoneyproduct,
            'T_Freq': topfreqsellproduct,
        }

        return Response(CombineData)


def AyearGenerator(self, data, strftime='%b'):
    result = {}
    # monthString = ['0','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    # 2022-09-06 18:50:44.169216+00:00

    for item in data:
        d = datetime.strptime(str(item.date)[0:19], "%Y-%m-%d")
        month_name = d.strftime(strftime)
        result[month_name] = result.get(month_name, 0) + int(float(item.price))

    return result


def AmonthGenerator(self, data):
    result = {}
    # monthString = ['0','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    # 2022-09-06 18:50:44.169216+00:00

    for item in data:
        d = datetime.strptime(str(item.date)[0:19], "%Y-%m-%d")
        name = d.strftime('%x')
        result[name] = result.get(name, 0) + int(float(item.price))

    return result


def AtodayGenerator(self, data):
    result = {}
    # monthString = ['0','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    # 2022-09-06 18:50:44.169216+00:00

    for item in data:
        d = datetime.strptime(str(item.date)[0:19], "%Y-%m-%d")
        name = d.strftime('%I:%M %p')
        result[name] = result.get(name, 0) + int(float(item.price))

    return result


def ChartDataGenerator(self, data, time):
    if time == 'today':
        return AtodayGenerator(self, data)
    elif time == 'month':
        return AmonthGenerator(self, data)
    elif time == 'year':
        return AyearGenerator(self, data)
    else:
        return AmonthGenerator(self, data)


class Expense(APIView):
    def get(self, request):
        time = request.GET.get('time')
        d = datetime.now()
        user = get_user_model().objects.get(username=request.user)
        if time == 'today':
            data = models.Expense.objects.filter(user=user, date__year=str(
                d.year), date__month=str(d.month), date__day=str(d.day))
            chartdata = ChartDataGenerator(self, data, time)
        elif time == 'month':
            data = models.Expense.objects.filter(
                user=user, date__year=str(d.year), date__month=str(d.month))
            chartdata = ChartDataGenerator(self, data, time)
        elif time == 'year':
            data = models.Expense.objects.filter(
                user=user, date__year=str(d.year))
            chartdata = ChartDataGenerator(self, data, time)
        elif time == 'custom':
            start_date = request.GET.get('startd')
            end_date = request.GET.get('endd')
            sd = datetime.strptime(start_date, "%m/%d/%y")
            ed = datetime.strptime(
                end_date, "%m/%d/%y").replace(hour=11, minute=59, second=59)
            data = models.Expense.objects.filter(
                user=user, date__range=(sd, ed))
            chartdata = ChartDataGenerator(self, data, time)
        else:
            data = models.Expense.objects.filter(user=user)
            chartdata = ChartDataGenerator(self, data, time)

        s = serializers.ExpenseSerializer(data, many=True)
        CombineData = {
            'DATA': s.data,
            'CHART_LABEL': chartdata.keys(),
            'CHART_DATA': chartdata.values(),
        }

        return Response(CombineData)

    def post(self, request):
        user = get_user_model().objects.get(username=request.user)
        title = request.data['title']
        price = request.data['price']
        date = request.data['date']
        description = request.data['description']

        ex = models.Expense.objects.create(
            date=date, user=user, description=description, title=title, price=price)

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request):
        user = get_user_model().objects.get(username=request.user)
        id = request.data['id']
        title = request.data['title']
        price = request.data['price']
        date = request.data['date']
        description = request.data['description']

        ex = models.Expense.objects.get(user=user, id=id)
        ex.title = title
        ex.price = price
        ex.description = description
        ex.date = ex.date
        ex.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = get_user_model().objects.get(username=request.user)
        id = request.data['id']
        ex = models.Expense.objects.get(user=user, id=id)
        ex.delete()


class Purchase(APIView):
    def get(self, request):
        time = request.GET.get('time')
        d = datetime.now()
        user = get_user_model().objects.get(username=request.user)
        data = models.Purchase.objects.filter(user=user)
        if time == 'today':
            data = models.Purchase.objects.filter(user=user, date__year=str(
                d.year), date__month=str(d.month), date__day=str(d.day))
            chartdata = ChartDataGenerator(self, data, time)
        elif time == 'month':
            data = models.Purchase.objects.filter(
                user=user, date__year=str(d.year), date__month=str(d.month))
            chartdata = ChartDataGenerator(self, data, time)
        elif time == 'year':
            data = models.Purchase.objects.filter(
                user=user, date__year=str(d.year))
            chartdata = ChartDataGenerator(self, data, time)
        elif time == 'custom':
            start_date = request.GET.get('startd')
            end_date = request.GET.get('endd')
            sd = datetime.strptime(start_date, "%m/%d/%y")
            ed = datetime.strptime(
                end_date, "%m/%d/%y").replace(hour=11, minute=59, second=59)
            data = models.Purchase.objects.filter(
                user=user, date__range=(sd, ed))
            chartdata = ChartDataGenerator(self, data, time)
        else:
            data = models.Purchase.objects.filter(user=user)
            chartdata = ChartDataGenerator(self, data, time)
        s = serializers.PurchaseSerializer(data, many=True)
        CombineData = {
            'DATA': s.data,
            'CHART_LABEL': chartdata.keys(),
            'CHART_DATA': chartdata.values(),
        }

        return Response(CombineData)

    def post(self, request):
        user = get_user_model().objects.get(username=request.user)
        title = request.data['title']
        price = request.data['price']
        date = request.data['date']
        description = request.data['description']

        ex = models.Purchase.objects.create(
            date=date, user=user, description=description, title=title, price=price)

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request):
        user = get_user_model().objects.get(username=request.user)
        id = request.data['id']
        title = request.data['title']
        price = request.data['price']
        date = request.data['date']
        description = request.data['description']

        ex = models.Purchase.objects.get(user=user, id=id)
        ex.title = title
        ex.price = price
        ex.description = description
        ex.date = ex.date
        ex.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = get_user_model().objects.get(username=request.user)
        id = request.data['id']
        ex = models.Purchase.objects.get(user=user, id=id)
        ex.delete()


class OtherIncome(APIView):
    def get(self, request):
        user = get_user_model().objects.get(username=request.user)
        time = request.GET.get('time')

        d = datetime.now()

        if time == 'today':
            data = models.OtherIncome.objects.filter(user=user, date__year=str(
                d.year), date__month=str(d.month), date__day=str(d.day))
            chartdata = ChartDataGenerator(self, data, time)
        elif time == 'month':
            data = models.OtherIncome.objects.filter(
                user=user, date__year=str(d.year), date__month=str(d.month))
            chartdata = ChartDataGenerator(self, data, time)
        elif time == 'year':
            data = models.OtherIncome.objects.filter(
                user=user, date__year=str(d.year))
            chartdata = ChartDataGenerator(self, data, time)
        elif time == 'custom':
            start_date = request.GET.get('startd')
            end_date = request.GET.get('endd')
            sd = datetime.strptime(start_date, "%m/%d/%y")
            ed = datetime.strptime(
                end_date, "%m/%d/%y").replace(hour=11, minute=59, second=59)
            data = models.OtherIncome.objects.filter(
                user=user, date__range=(sd, ed))
            chartdata = ChartDataGenerator(self, data, time)
        else:
            data = models.OtherIncome.objects.filter(user=user)
            chartdata = ChartDataGenerator(self, data, time)

        s = serializers.OtherIncomeSerializer(data, many=True)
        CombineData = {
            'DATA': s.data,
            'CHART_LABEL': chartdata.keys(),
            'CHART_DATA': chartdata.values(),
        }

        return Response(CombineData)

    def post(self, request):
        user = get_user_model().objects.get(username=request.user)
        title = request.data['title']
        price = request.data['price']
        date = request.data['date']
        description = request.data['description']

        ex = models.OtherIncome.objects.create(
            date=date, user=user, description=description, title=title, price=price)

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request):
        user = get_user_model().objects.get(username=request.user)
        id = request.data['id']
        title = request.data['title']
        price = request.data['price']
        date = request.data['date']
        description = request.data['description']

        ex = models.OtherIncome.objects.get(user=user, id=id)
        ex.title = title
        ex.price = price
        ex.description = description
        ex.date = ex.date
        ex.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = get_user_model().objects.get(username=request.user)
        id = request.data['id']
        ex = models.OtherIncome.objects.get(user=user, id=id)
        ex.delete()


class ProfitAndLoss(APIView):
    def get(self, request, format=None):
        user = get_user_model().objects.get(username=request.user)

        d = datetime.now()

        otherincome_data = models.OtherIncome.objects.filter(
            user=user, date__year=str(d.year))
        sales_data = models.Sales.objects.filter(
            user=user, date__year=str(d.year))
        expense_data = models.Expense.objects.filter(
            user=user, date__year=str(d.year))
        purchase_data = models.Purchase.objects.filter(
            user=user, date__year=str(d.year))

        sales_ge = yearGenerator(self, sales_data, '%B')
        otherincome_ge = AyearGenerator(self, otherincome_data, '%B')
        expense_ge = AyearGenerator(self, expense_data, '%B')
        purchase_ge = AyearGenerator(self, purchase_data, '%B')

        addData = {k: sales_ge.get(k, 0) + otherincome_ge.get(k, 0)
                   for k in set(sales_ge) | set(otherincome_ge)}
        minusData = {k: expense_ge.get(k, 0) + purchase_ge.get(k, 0)
                     for k in set(expense_ge) | set(purchase_ge)}
        subtractData = {k: addData.get(k, 0) - minusData.get(k, 0)
                        for k in set(addData) | set(minusData)}

        print(sales_ge)

        # print(addData,minusData,subtractData)
        ordered_data = sorted(
            addData.items(), key=lambda x: datetime.strptime(x[0], '%B'))
        print(ordered_data)

        CombineData = {
            'addData':  OrderedDict(sorted(addData.items(), key=lambda x: datetime.strptime(x[0], '%B'))),
            'minusData': OrderedDict(sorted(minusData.items(), key=lambda x: datetime.strptime(x[0], '%B'))),
            'result': OrderedDict(sorted(subtractData.items(), key=lambda x: datetime.strptime(x[0], '%B'))),

        }
        return Response(CombineData)


class ProfileAPIView(APIView):

    def get(self, request, format=None):
        user = models.User.objects.get(username=request.user)
        s = serializers.ProfileSerializer(user)
        print(s)
        return Response(s.data)

    def post(self, request, format=None):
        user = get_user_model().objects.get(username=request.user)

        if 'image' in request.data:
            user.profileimage = request.FILES['image']
            user.save()
            s = serializers.ProfileSerializer(user)
            return Response(s.data)
        s = serializers.ProfileSerializer(user)
        return Response(s.data)


class FeedBackAPIView(APIView):

    def post(self, request, format=None):
        message = request.data['message']

        models.FeedBack.objects.create(user=request.user, message=message)

        return Response(status=status.HTTP_201_CREATED)


class PricingAPIView(APIView):
    def get(self, request, format=None):
        data = models.Pricing.objects.all()
        pricing_ser = serializers.PricingSerializer(data, many=True)
        user = get_user_model().objects.get(username=request.user)
        pr_req_ser={data:{}}
        try:
            pricing_req = models.PricingRequest.objects.filter(user=user,done=False)
            pr_req_ser = serializers.PricingRequestSerializer(pricing_req,many=True)
        except ObjectDoesNotExist:
            print('Objects Does Not exist')
        CombineData = {
            'pricing':pricing_ser.data,
            'pr_request': pr_req_ser.data
        }

        return Response(CombineData)

    # It Is Main Buy SOftware not adding Pricing method check this code
    def post(self, request, format=None):
        price_time_type = request.data['type']
        user = get_user_model().objects.get(username=request.user)
        pricing = models.Pricing.objects.get(title=price_time_type)
        models.PricingRequest.objects.create(user=user, rq_price=pricing)
        
        return Response(status=status.HTTP_201_CREATED)

# Only Super User Can Be Use this View
class PricingRequestView(APIView):
    def get(self,request,format=None):
        pricing_req = models.PricingRequest.objects.all()
        ser_p_r = serializers.PricingRequestSerializer(pricing_req,many=True)

        return Response(ser_p_r.data)
    
    def post(self,request):
        username = request.data['username']
        user = get_user_model().objects.get(username=username)
        pr = models.PricingRequest.objects.get(user=user,done=False)
        # pr.done = True
        user.start_d = pr.date
        user.end_d = pr.date + pr.rq_price.days
        user.save()

        return Response(status=status.HTTP_201_CREATED)
        

class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class LoginWithFacebook(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.CreateUserSerializer

    def post(self, request):

        try:
            username = request.data['username']
            print(username)
            user = models.User.objects.get(username=username)
            print(user)
            token = Token.objects.get(user=user)
            token_data = {'token': token.key}
            return Response({**token_data}, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            serializers = self.get_serializer(data=request.data)
            serializers.is_valid(raise_exception=True)
            self.perform_create(serializers)

            token = Token.objects.create(user=serializers.instance)
            token_data = {'token': token.key}

            return Response({**token_data}, status=status.HTTP_201_CREATED)
