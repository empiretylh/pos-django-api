from datetime import timedelta
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

from django.utils import timezone


from . import models, serializers

import json


def CHECK_IN_PLAN_AND_RESPONSE(user, data, **args):
    if user.is_plan:
        return Response('End Plan or No Purchase Plan')
    else:
        return Response(data=data, **args)

    print('User is in Plan')


# only For Sales Digits user
class CreateUserApiView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = serializers.CreateUser_SalesDigit_Serializer

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


class SalesTwoDigits(APIView):
    # permission_classes = [AllowAny]P

    def get(self, request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                            is_salesDigits=True)
      
        try:
            G = models.TwoDigitsGroup.objects.get(user=user, is_done=False)          
            print('Group M Exists')
        except ObjectDoesNotExist:
            print('Group M Not Exits')
            G = models.TwoDigitsGroup.objects.create(user=user)
            print('Group M Created')


        data = models.SalesTwoDigits.objects.filter(user=user,group=G)
        ser = serializers.SalesTwoDigitSerializer(data,many=True)

        return Response(ser.data)

    def post(self, request):
        name = request.data['customername']
        phoneno = request.data['phoneno']
        digits = request.data['digits']
        totalamount = request.data['totalamount']
        print(request.user)
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                            is_salesDigits=True)
                                
        try:
            G = models.TwoDigitsGroup.objects.get(user=user, is_done=False)          
            print('Group M Exists')
        except ObjectDoesNotExist:
            print('Group M Not Exits')
            G = models.TwoDigitsGroup.objects.create(user=user)
            print('Group M Created')


        # print(str(name) +'\n')
        # print(str(phoneno) + '\n')
        # print(digits)
        # print(int(totalamount))

        Sales = models.SalesTwoDigits.objects.create(customername=name,phoneno=phoneno,totalprice=totalamount,user=user,group=G)
        # Sales1 = models.SalesTwoDigits.objects.create(customername=name,phoneno=phoneno,totalprice=totalamount,user=user,group=G1)

        print('Sales Objects Created')


        ds = json.loads(digits)
        # print(p)
        for d in ds:
            print(d)
            d1 = models.TwoDigits.objects.create(number=d['digits'],amount=d['amount'],user=user,sales=Sales)
            print('D1 Create')
           

        print('Finished All')

        #     product = models.Product.objects.get(id=b['name'], user=user)
        #     product.qty = int(product.qty) - int(b['qty'])
        #     product.save()

        #     a = models.SoldProduct.objects.create(
        #         name=product, price=b['price'], qty=b['qty'], sales=S)
        #     print(a)

        # S.save()

        return Response(status=status.HTTP_201_CREATED)

class Check_MORE_TWODIGITS(APIView):
    def get(self,request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                     is_salesDigits=True)   
           
        dd = request.GET.get('datetime')
        print(dd)
        d = datetime.strptime(dd,"%a %b %d %Y")

        try:            
            G = models.TwoDigitsGroup.objects.filter(user=user,is_done=True,end_datetime__day=str(d.day))    
            S =  serializers.TwoDigitsGroupSerializer(G,many=True)
            return Response(S.data)
               
            print('M True Exist')
        except ObjectDoesNotExist:
            print('Data M Not Exit')
            return Response(0)
            #0 Means Data Does Not Exit

        
       

class FinishSalesTwoDigits(APIView):

    def get(self,request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                     is_salesDigits=True)   
           
        dd = request.GET.get('datetime')
      
        print(dd)
        d = datetime.fromisoformat(dd)      
      
        try:            
            G = models.TwoDigitsGroup.objects.get(user=user,is_done=True,end_datetime=d)    
           
        except ObjectDoesNotExist:
            print('Data Does Not Exit')
            #0 Means Data Does Not Exit
            return Response(0)

        st = models.SalesTwoDigits.objects.filter(group=G)
        ser = serializers.SalesTwoDigitSerializer(st,many=True)

        return Response(ser.data)

    def post(self,request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                            is_salesDigits=True)
       
        G = models.TwoDigitsGroup.objects.get(user=user, is_done=False)
        G.is_done=True
        G.luckyNumber= request.data['luckynumber']
        G.end_datetime = datetime.now()
        G.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self,request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                            is_salesDigits=True)
        dd = request.GET.get('datetime')
       
        d = datetime.fromisoformat(dd)  
        G = models.TwoDigitsGroup.objects.get(user=user, is_done=True,end_datetime=d)
        G.delete()
        print('Successfully Deleted Data')
        return Response(status=status.HTTP_201_CREATED)

class FinishAllSalesTwoDigits(APIView):

    def get(self,request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                     is_salesDigits=True)      
               
        S = ''
        try:            
            G = models.TwoDigitsGroup.objects.filter(user=user,is_done=True)
            S =  serializers.TwoDigitsGroupSerializer(G,many=True)
        except ObjectDoesNotExist:
            print('Data Does Not Exit')
            #0 Means Data Does Not Exit
            return Response(0)
      
    

        return Response(S.data)



# ///////////////////////////////////////////////////Three Digits Data ................................................

class SalesThreeDigits(APIView):
    # permission_classes = [AllowAny]P

    def get(self, request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                            is_salesDigits=True)
                                            
      
        try:
            G = models.ThreeDigitsGroup.objects.get(user=user, is_done=False)
        except ObjectDoesNotExist:
            print('Three Digits Not exists')
            G = models.ThreeDigitsGroup.objects.create(user=user)
            print('Three Digits Gruop Created')

        data = models.SalesThreeDigits.objects.filter(user=user,group=G)
        ser = serializers.SalesThreeDigitSerializer(data,many=True)

        return Response(ser.data)

    def post(self, request):
        name = request.data['customername']
        phoneno = request.data['phoneno']
        digits = request.data['digits']
        totalamount = request.data['totalamount']
        print(request.user)
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                            is_salesDigits=True)
                                
        try:
            G = models.ThreeDigitsGroup.objects.get(user=user, is_done=False)
            print('Group Exists')
        except ObjectDoesNotExist:
            print('Group Not Exits')
            G = models.ThreeDigitsGroup.objects.create(user=user)
            print('Group Created')
        # print(str(name) +'\n')
        # print(str(phoneno) + '\n')
        # print(digits)
        # print(int(totalamount))

        Sales = models.SalesThreeDigits.objects.create(customername=name,phoneno=phoneno,totalprice=totalamount,user=user,group=G)

        print('Sales Objects Created')


        ds = json.loads(digits)
        # print(p)
        for d in ds:
            print(d)
            d = models.ThreeDigits.objects.create(number=d['digits'],amount=d['amount'],user=user,sales=Sales)
        
        print('Finished All')

        #     product = models.Product.objects.get(id=b['name'], user=user)
        #     product.qty = int(product.qty) - int(b['qty'])
        #     product.save()

        #     a = models.SoldProduct.objects.create(
        #         name=product, price=b['price'], qty=b['qty'], sales=S)
        #     print(a)

        # S.save()

        return Response(status=status.HTTP_201_CREATED)

class FinishSalesThreeDigits(APIView):

    def get(self,request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                     is_salesDigits=True)      
        dd = request.GET.get('datetime')
       
        print(dd) 
        d = datetime.strptime(dd,"%a %b %d %Y")
        try:            
            G = models.ThreeDigitsGroup.objects.get(user=user,is_done=True,end_datetime__day=str(d.day))        
        except ObjectDoesNotExist:
            print('Data Does Not Exit')
            #0 Means Data Does Not Exit
            return Response(0)
      
        st = models.SalesThreeDigits.objects.filter(group=G)
        ser = serializers.SalesThreeDigitSerializer(st,many=True)

        return Response(ser.data)

    def post(self,request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                            is_salesDigits=True)
       
        G = models.ThreeDigitsGroup.objects.get(user=user, is_done=False)
        G.is_done=True
        G.luckyNumber= request.data['luckynumber']
        G.end_datetime = request.data['enddate']
        G.save()
        return Response(status=status.HTTP_201_CREATED)
     
    def delete(self,request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                            is_salesDigits=True)

        dd = request.GET.get('datetime')
       
        print(dd) 
        d = datetime.strptime(dd,"%a %b %d %Y")
      
        G = models.ThreeDigitsGroup.objects.get(user=user, is_done=True,end_datetime__day=str(d.day))
        G.delete()
        print('Successfully Deleted Data')
        return Response(status=status.HTTP_201_CREATED)


class FinishAllSalesThreeDigits(APIView):

    def get(self,request):
        user = get_user_model().objects.get(username=request.user,is_plan=True,
                                     is_salesDigits=True)      
               
        S = ''
        try:            
            G = models.ThreeDigitsGroup.objects.filter(user=user,is_done=True)
            S =  serializers.ThreeDigitsGroupSerializer(G,many=True)
        except ObjectDoesNotExist:
            print('Data Does Not Exit')
            #0 Means Data Does Not Exit
            return Response(0)
      
    

        return Response(S.data)




class PricingAPIView(APIView):
    def get(self, request, format=None):
        data = models.Pricing.objects.filter(is_digits=True)
        pricing_ser = serializers.PricingSerializer(data, many=True)
        user = get_user_model().objects.get(username=request.user)
        print(user.is_superuser)
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
        pricing = models.Pricing.objects.get(id=price_time_type,is_digits=True)
        models.PricingRequest.objects.create(user=user, rq_price=pricing)
        
        return Response(status=status.HTTP_201_CREATED)

    def delete(self,request,format=None):
        price_time_type = request.GET.get('type')
        user = get_user_model().objects.get(username=request.user)
        pricing = models.Pricing.objects.get(id=price_time_type,is_digits=True)
        pr_req=  models.PricingRequest.objects.get(user=user,done=False)
        pr_req.delete()

        return Response(status=status.HTTP_201_CREATED)