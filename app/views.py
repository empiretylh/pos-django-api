from django.shortcuts import render

# Create your views here.
def hello(request):
    return render(request,'index.html')


def howtopaymoney(request):
    return render(request,'howtopaymoney.html') 