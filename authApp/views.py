from .models import Contact, ContactInfo, About, Plan, Blog
from .serializers import UserUpdatePPSerializer,CustomTokenObtainPairSerializer, BlogListSerializer,PlanListSerializer ,ContactSerializer, ContactInfoSerializer, AboutSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserUpdateSerializer, ChangePasswordSerializer
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


class ContactInfoAPIView(APIView):
    permission_classes = [AllowAny]
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
    

class BlogPagination(PageNumberPagination):
    page_size = 6  # hər səhifədə 10 blog
    page_size_query_param = 'page_size'
    max_page_size = 50

class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogListSerializer
    pagination_class = BlogPagination


