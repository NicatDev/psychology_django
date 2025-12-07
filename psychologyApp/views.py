

# Create your views here.
from rest_framework import generics, permissions
from .models import Question, Test
from .serializers import QuestionSerializer, TestSerializer, TestCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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