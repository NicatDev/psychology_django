from .models import Contact, ContactInfo, About, Plan, Blog, SocialLink
from .serializers import UserUpdatePPSerializer,CustomTokenObtainPairSerializer, BlogListSerializer,PlanListSerializer ,ContactSerializer, ContactInfoSerializer, AboutSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserUpdateSerializer, ChangePasswordSerializer, SocialLinkSerializer
from rest_framework import generics, permissions
from rest_framework import status

class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user  # login olan user update edir
    
class UserPPUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdatePPSerializer

    def get_object(self):
        return self.request.user  # login olan user update edir

# Change password
class ChangePasswordAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class AboutAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request):
        obj = About.objects.first()
        if not obj:
            obj = About.objects.create(
                title=None,
                miniTitle=None,
                content=None
            )
        serializer = AboutSerializer(obj)
        return Response(serializer.data)


class ContactCreateAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]  
    authentication_classes = []


class ContactInfoAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request):
        obj = ContactInfo.objects.first()
        if not obj:
            obj = ContactInfo.objects.create(
                location=None,
                location_url=None,
                phone=None,
                email=None
            )
        serializer = ContactInfoSerializer(obj)
        return Response(serializer.data)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, context={'request': request}) 
        return Response(serializer.data)
    
class PlanListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Plan.objects.filter(is_active=True).order_by('price')
    serializer_class = PlanListSerializer
    authentication_classes = []

class BlogPagination(PageNumberPagination):
    page_size = 6  # hər səhifədə 10 blog
    page_size_query_param = 'page_size'
    max_page_size = 50

class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogListSerializer
    pagination_class = BlogPagination

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import random
User = get_user_model()
from .serializers import RegisterSerializer, VerifyEmailSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .models import VerificationCode

class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # 6 rəqəmli kod yaradırıq
            code = str(random.randint(100000, 999999))
            
            # Kodu bazada yadda saxlayırıq (Köhnə kodlar varsa silə bilərsiniz, sadəlik üçün birbaşa yaradırıq)
            VerificationCode.objects.create(user=user, code=code)
            
            # Emaili göndəririk
            subject = 'Hesab Təsdiqləmə Kodu'
            message = f'Salam, Sizin təsdiq kodunuz: {code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return Response({'error': 'Email göndərilə bilmədi, amma qeydiyyat uğurludur.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'message': 'Qeydiyyat uğurla tamamlandı. Zəhmət olmasa emailinizi yoxlayın və kodu daxil edin.',
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'İstifadəçi tapılmadı'}, status=status.HTTP_404_NOT_FOUND)
            
            # Əgər artıq aktivdirsə
            if user.is_active:
                return Response({'message': 'Hesab artıq təsdiqlənib'}, status=status.HTTP_200_OK)

            # Kodu yoxlayırıq (Sonuncu göndərilən kod əsas götürülür)
            verification = VerificationCode.objects.filter(user=user, code=code).last()
            
            if verification and verification.is_valid():
                user.is_active = True
                user.save()
                
                # İstifadə olunan kodu silirik (təhlükəsizlik üçün)
                verification.delete()
                
                return Response({'message': 'Hesab uğurla aktivləşdirildi!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Kod yanlışdır və ya vaxtı bitib'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendCodeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data, partial=True) # Sadəcə email lazımdır
        if request.data.get('email'):
            email = request.data.get('email')
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'İstifadəçi tapılmadı'}, status=status.HTTP_404_NOT_FOUND)
            
            if user.is_active:
                return Response({'message': 'Hesab artıq aktivdir.'}, status=status.HTTP_200_OK)

            # Yeni kod yaradırıq
            code = str(random.randint(100000, 999999))
            
            # Köhnə kodu silib yenisini yarada bilərik və ya sadəcə yeni birini yaradarıq
            # VerificationCode.objects.filter(user=user).delete() 
            VerificationCode.objects.create(user=user, code=code)
            
            # Emaili göndəririk
            subject = 'Hesab Təsdiqləmə Kodu (Yenidən)'
            message = f'Salam, Sizin yeni təsdiq kodunuz: {code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return Response({'error': 'Email göndərilə bilmədi'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Yeni kod email ünvanınıza göndərildi.'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Email daxil edilməyib'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # Kod yaradılması
            code = str(random.randint(100000, 999999))
            VerificationCode.objects.create(user=user, code=code)

            # Email göndərilməsi
            subject = 'Octopus - Reset password'
            message = f'Salam, Sizin şifrə yeniləmə kodunuz: {code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return Response({'error': 'Email göndərilə bilmədi.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Təsdiq kodu email ünvanınıza göndərildi.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            
            user = User.objects.get(email=email) # Serializer artıq yoxlayıb ki user var
            
            user.set_password(new_password)
            user.save()
            
            # Kodu silirik
            VerificationCode.objects.filter(user=user, code=serializer.validated_data['code']).delete()
            
            return Response({'message': 'Şifrəniz uğurla yeniləndi.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialLinksAPIView(generics.ListAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [AllowAny]  
    authentication_classes = []