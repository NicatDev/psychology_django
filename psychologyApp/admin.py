from django.contrib import admin
from .models import *

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
    
class KeyMotivatorInline(admin.TabularInline):
    model = KeyMotivator
    extra = 1

class IdealWorkEnvironmentInline(admin.TabularInline):
    model = IdealWorkEnvironment
    extra = 1

class CoreValueInline(admin.TabularInline):
    model = CoreValue
    extra = 1

class PreferredWorkTaskInline(admin.TabularInline):
    model = PreferredWorkTask
    extra = 1

class ContributionToOrganizationInline(admin.TabularInline):
    model = ContributionToOrganization
    extra = 1

class TeamHelpInline(admin.TabularInline):
    model = TeamHelp
    extra = 1

class TeamIrritateInline(admin.TabularInline):
    model = TeamIrritate
    extra = 1

class TeamActionStepInline(admin.TabularInline):
    model = TeamActionStep
    extra = 1

# Main admin
@admin.register(PersonalityType)
class PersonalityTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    inlines = [
        KeyMotivatorInline,
        IdealWorkEnvironmentInline,
        CoreValueInline,
        PreferredWorkTaskInline,
        ContributionToOrganizationInline,
        TeamHelpInline,
        TeamIrritateInline,
        TeamActionStepInline,
    ]