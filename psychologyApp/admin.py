from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from .models import PersonalityType, Question, Option, Test, Answer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'dimension', 'type']
    inlines = [OptionInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    # readonly_fields = ('option',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['test', 'option']
    
# Main admin
@admin.register(PersonalityType)
class PersonalityTypeAdmin(TabbedTranslationAdmin):
    list_display = ['code', 'name']
