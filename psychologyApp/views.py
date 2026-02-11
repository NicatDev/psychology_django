

# Create your views here.
from rest_framework import generics, permissions
from .models import Question, Test, Option
from .serializers import QuestionSerializer, TestSerializer, TestCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import json
from django.conf import settings
import os
# 1) Questions GET
class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.prefetch_related('options').all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

# 2) Test Create
class TestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TestCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.active_test_count > 0:
            user.active_test_count -= 1
            user.save() 
        else:
            return Response({'message': 'İstifadəçinin hesabında test cəhdi sayı 0-dır'}, status=status.HTTP_201_CREATED)
        test = serializer.save()
        
        return Response({'test_id': test.id}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        # Browser açanda text olaraq nümunəni göstəririk
        example = {
            "answers": [1, 2, 3]
        }
        return Response(
            {
                "message": "POST üçün nümunə JSON",
                "example": example
            },
            status=status.HTTP_200_OK
        )

# 3) List tests for user
class UserTestListView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Test.objects.filter(user=self.request.user).order_by('-created_at')
    

# 4) Test detail with answers
class TestDetailView(generics.RetrieveAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Test.objects.all()


from .models import PersonalityType
from .serializers import PersonalityTypeDetailSerializer

# List API (sadəcə id və name də ola bilər)
class PersonalityTypeListView(generics.ListAPIView):
    queryset = PersonalityType.objects.all()
    serializer_class = PersonalityTypeDetailSerializer  # nested info ilə

# Detail API (lookup by code)
class PersonalityTypeDetailView(generics.RetrieveAPIView):
    queryset = PersonalityType.objects.all()
    serializer_class = PersonalityTypeDetailSerializer
    lookup_field = 'code'

class LoadQuestionsAPIView(APIView):
    """
    API çağırıldıqda mövcud sualları sil və questions.json-dan DB-yə doldur.
    """

    def post(self, request):
        # 1️⃣ Mövcud datanı sil
        Option.objects.all().delete()
        Question.objects.all().delete()

        # 2️⃣ JSON faylını oxu
        file_path = os.path.join(settings.BASE_DIR, "data", "questions.json")
        with open(file_path, "r", encoding="utf-8") as f:
            questions_data = json.load(f)

        # 3️⃣ DB-yə yaz
        for q in questions_data:
            # Question obyektini əvvəl save et
            question = Question(
                text=q["question"],
                dimension=q.get("dimension", ""),
                type=q.get("type", "likert")
            )
            question.save()  # FK üçün commit

            # Option-ları bulk_create ilə əlavə et
            options_to_create = [
                Option(
                    question=question,
                    text=opt["text"],
                    value=opt["value"]
                )
                for opt in q.get("options", [])
            ]
            Option.objects.bulk_create(options_to_create)

        return Response(
            {"message": "Questions loaded successfully"},
            status=status.HTTP_201_CREATED
        )
    


from .models import (
    PersonalityType, KeyMotivator, IdealWorkEnvironment, CoreValue, PreferredWorkTask,
    ContributionToOrganization, TeamHelp, TeamIrritate, TeamActionStep
)
class LoadPersonalityTypesAPIView(APIView):
    """
    API çağırıldıqda mövcud personality types datalarını sil və
    personalityTypes.json-dan DB-yə doldur.
    """

    def post(self, request):
        # 1️⃣ Mövcud datanı sil
        PersonalityType.objects.all().delete()

        # 2️⃣ JSON faylını oxu
        file_path = os.path.join(settings.BASE_DIR, "data", "personalityTypes.json")
        with open(file_path, "r", encoding="utf-8") as f:
            types_data = json.load(f)

        # 3️⃣ DB-yə yaz
        for code, details in types_data.items():
            # PersonalityType yaradılır
            pt, created = PersonalityType.objects.update_or_create(
                code=code,
                defaults={
                    "name": details.get("name", ""),
                    "summary": details.get("summary", ""),
                    "workplace_personality": details.get("workplacePersonality", ""),
                    "working_with_team": details.get("workingWithTeam", ""),
                    "communicating_with_others": details.get("communicatingWithOthers", ""),
                    "managing_conflict": details.get("managingConflict", ""),
                    "taking_the_lead": details.get("takingTheLead", ""),
                    "getting_things_done": details.get("gettingThingsDone", ""),
                    "growth_and_development": details.get("growthAndDevelopment", ""),
                    "coping_with_stress": details.get("copingWithStress", ""),
                    "achieving_success": details.get("achievingSuccess", "")
                }
            )

            # 4️⃣ List tipli field-ləri əlavə et
            def add_list_items(model_class, related_name, key):
                for item in details.get(key, []):
                    model_class.objects.create(personality_type=pt, name=item)

            add_list_items(KeyMotivator, "key_motivators", "keyMotivators")
            add_list_items(IdealWorkEnvironment, "ideal_work_environments", "idealWorkEnvironment")
            add_list_items(CoreValue, "core_values", "coreValues")
            add_list_items(PreferredWorkTask, "preferred_work_tasks", "preferredWorkTasks")
            add_list_items(ContributionToOrganization, "contributions_to_organization", "contributionsToOrganization")
            add_list_items(TeamHelp, "team_helps", "teamHelp")
            add_list_items(TeamIrritate, "team_irritates", "teamIrritate")
            add_list_items(TeamActionStep, "team_action_steps", "teamActionSteps")

        return Response({"message": "Personality types loaded successfully"}, status=status.HTTP_201_CREATED)