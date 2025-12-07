from django.urls import path
from .views import QuestionListView, TestCreateView, UserTestListView, TestDetailView

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='questions-list'),
    path('test/create/', TestCreateView.as_view(), name='test-create'),
    path('tests/', UserTestListView.as_view(), name='user-tests'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test-detail'),
]