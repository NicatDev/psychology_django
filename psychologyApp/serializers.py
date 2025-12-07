from rest_framework import serializers
from .models import Question, Option, Test, Answer

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'value']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'dimension', 'type', 'options']

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

class TestCreateAnswerSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()

class TestCreateSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.IntegerField(),  # Option id-ləri
        allow_empty=False,
        
    )

    def create(self, validated_data):
        user = self.context['request'].user
        test = Test.objects.create(user=user)
        for option_id in validated_data['answers']:
            option = Option.objects.get(id=option_id)
            Answer.objects.create(test=test, option=option)
        return test