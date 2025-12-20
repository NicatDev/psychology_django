from django.urls import path
from .views import BuyPlanAPIView, PaypalSuccessView, MyPaymentsView

urlpatterns = [
    path("buy-plan/", BuyPlanAPIView.as_view()),
    path("paypal/success/", PaypalSuccessView.as_view()),
    path('my-payments/', MyPaymentsView.as_view(), name='my-payments'),
]