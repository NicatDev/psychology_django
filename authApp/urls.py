from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ContactCreateAPIView, ContactInfoAPIView, AboutAPIView, UserProfileView, PlanListView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  

    path('about-info/', AboutAPIView.as_view(), name='about-info'),
    path('contact/create/', ContactCreateAPIView.as_view(), name='contact-create'),
    path('contact-info/', ContactInfoAPIView.as_view(), name='contact-info'),

    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('plans/', PlanListView.as_view(), name='plan-list'),
]

