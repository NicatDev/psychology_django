from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
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
    extra = 1
    # readonly_fields = ('option',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['test', 'option']
    
class KeyMotivatorInline(TranslationTabularInline):
    model = KeyMotivator
    extra = 1

class IdealWorkEnvironmentInline(TranslationTabularInline):
    model = IdealWorkEnvironment
    extra = 1

class CoreValueInline(TranslationTabularInline):
    model = CoreValue
    extra = 1

class PreferredWorkTaskInline(TranslationTabularInline):
    model = PreferredWorkTask
    extra = 1

class ContributionToOrganizationInline(TranslationTabularInline):
    model = ContributionToOrganization
    extra = 1

class TeamHelpInline(TranslationTabularInline):
    model = TeamHelp
    extra = 1

class TeamIrritateInline(TranslationTabularInline):
    model = TeamIrritate
    extra = 1

class TeamActionStepInline(TranslationTabularInline):
    model = TeamActionStep
    extra = 1

# Main admin
@admin.register(PersonalityType)
class PersonalityTypeAdmin(TabbedTranslationAdmin):
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
