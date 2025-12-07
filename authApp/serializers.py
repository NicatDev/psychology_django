from rest_framework import serializers
from .models import Contact, ContactInfo, About, Plan

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['id', 'title', 'miniTitle', 'content']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']  # id və tarix client tərəfindən doldurulmayacaq

    # Hamısını tələb olunan etmək
    def validate(self, data):
        for field in ['full_name', 'email', 'subject', 'message']:
            if not data.get(field):
                raise serializers.ValidationError({field: "This field is required."})
        return data
    
class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['id', 'location', 'location_url', 'phone', 'email']




from django.contrib.auth import get_user_model
from psychologyApp.models import Test, Answer, Option  # Test modeli testsApp-da olduğunu fərz edirəm

User = get_user_model()

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'value']

class AnswerSerializer(serializers.ModelSerializer):
    option = OptionSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'option']

class TestSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Test
        fields = ['id', 'created_at', 'answers']


class SimpleTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    tests = SimpleTestSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'tests']


class PlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
