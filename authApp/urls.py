from django.urls import path, include
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import UserPPUpdateAPIView,UserUpdateAPIView,ChangePasswordAPIView,CustomTokenObtainPairView, ContactCreateAPIView, ContactInfoAPIView, AboutAPIView, UserProfileView, PlanListView
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet
router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blog')
urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('change/password/', ChangePasswordAPIView.as_view(), name='token_refresh'),  
    path('user/update/', UserUpdateAPIView.as_view(), name='token_refresh'),  
    path('user/update/pp/', UserPPUpdateAPIView.as_view(), name='token_refresh'),  

    path('about-info/', AboutAPIView.as_view(), name='about-info'),
    path('contact/create/', ContactCreateAPIView.as_view(), name='contact-create'),
    path('contact-info/', ContactInfoAPIView.as_view(), name='contact-info'),

    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('plans/', PlanListView.as_view(), name='plan-list'),
       path('', include(router.urls)),
]

