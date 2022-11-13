from django.urls import path, include

# from app.models import SalesTwoDigits
from . import views
from . import apiview
from django.conf.urls.static import static
from django.conf import settings

from . import salesDigit

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/categorys/', apiview.Category.as_view(), name='category'),
    path('api/products/', apiview.Product.as_view(), name='product'),
    path('api/soldproducts/', apiview.SoldProduct.as_view(), name='sold_product'),
    path('api/sales/', apiview.Sales.as_view(), name='sales'),
    path('api/expenses/', apiview.Expense.as_view(), name='expense'),
    path('api/purchases/', apiview.Purchase.as_view(), name='purchase'),
    path('api/otherincome/', apiview.OtherIncome.as_view(), name='otherincome'),
    path('api/profitnloss/', apiview.ProfitAndLoss.as_view(), name='profitnloss'),
    path('api/profile/', apiview.ProfileAPIView.as_view(), name='profile'),

    path('api/toproduct/', apiview.TopProductsView.as_view(), name='topproduct'),
    path('api/feedback/', apiview.FeedBackAPIView.as_view(), name='feedback'),
    path('api/pricing/', apiview.PricingAPIView.as_view(), name='pricing'),
    path('api/pricingrequest/', apiview.PricingRequestView.as_view(),
         name='pricing_request'),


    path('auth/login/', obtain_auth_token, name='auth_user_login'),
    path('auth/register/', apiview.CreateUserApiView.as_view(),
         name='auth_user_create'),
    path('auth/logout/', apiview.LogoutUserAPIView.as_view(),
         name='auth_user_logout'),


    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
