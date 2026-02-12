from rest_framework import serializers
from .models import PersonalityType, Question, Option, Test, Answer

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
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'created_at', 'answers', 'result', 'result_values']

    def get_answers(self, obj):
        return [answer.option.id for answer in obj.answers.all()]

class TestCreateAnswerSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()

class TestCreateSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.IntegerField(),  # Option id-ləri
        allow_empty=False,
    )
    result = serializers.CharField(required=False, allow_blank=True)  # TextField üçün
    result_values = serializers.JSONField(required=False) 
 # JSONField üçün

    def create(self, validated_data):
        user = self.context['request'].user
        print(validated_data)
        result = validated_data.get('result', "")
        result_values = validated_data.get('result_values', {})
        test = Test.objects.create(
            user=user,
            result=result,
            result_values=result_values
        )
        for option_id in validated_data['answers']:
            option = Option.objects.get(id=option_id)
            Answer.objects.create(test=test, option=option)
        return test
    


# Main serializer with nested relations
class PersonalityTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityType
        fields = '__all__'



class OptionSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'value']

class QuestionSaveSerializer(serializers.ModelSerializer):
    options = OptionSaveSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'dimension', 'type', 'options']