from rest_framework import generics
from .models import Contact, ContactInfo, About, Plan
from .serializers import PlanListSerializer ,ContactSerializer, ContactInfoSerializer, AboutSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.filter(is_active=True).order_by('price')
    serializer_class = PlanListSerializer