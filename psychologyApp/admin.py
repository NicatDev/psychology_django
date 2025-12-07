from django.contrib import admin
from .models import Question, Option, Test, Answer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'dimension', 'type']
    inlines = [OptionInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # Yeni cavab əlavə etmək üçün
    # readonly_fields = ('option',)  # bunu silirik, yoxsa option seçmək mümkün deyil

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [AnswerInline]  # Test içində cavablar görünəcək və seçilə biləcək

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['test', 'option']