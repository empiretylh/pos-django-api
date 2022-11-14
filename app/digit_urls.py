from django.urls import path, include

from . import views
from . import apiview
from django.conf.urls.static import static
from django.conf import settings

from . import salesDigit

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    path('auth/salesdigit/register/',
         salesDigit.CreateUserApiView.as_view(), name='sales_digit_register'),
    path('sd/api/salestwodigit/', salesDigit.SalesTwoDigits.as_view(),
         name='sales_two_digit'),
           path('sd/api/finishtwodigit/', salesDigit.FinishSalesTwoDigits.as_view(),
         name='finish_two_digit'),
          path('sd/api/historytwodigit/', salesDigit.FinishAllSalesTwoDigits.as_view(),
         name='history_two_digit'),



             path('sd/api/salesthreedigit/', salesDigit.SalesThreeDigits.as_view(),
         name='sales_three_digit'),
           path('sd/api/finishthreedigit/', salesDigit.FinishSalesThreeDigits.as_view(),
         name='finish_three_digit'),
          path('sd/api/historythreedigit/', salesDigit.FinishAllSalesThreeDigits.as_view(),
         name='history_three_digit'),
         

#     path('salesthreedigit', salesDigit.SalesTwoDigits.as_view(),
#          name='sales_two_digit'),
#     path('reporttwodigit', salesDigit.SalesTwoDigits.as_view(),
#          name='sales_two_digit'),
#     path('reportthreedigit', salesDigit.SalesTwoDigits.as_view(),
#          name='sales_two_digit')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
