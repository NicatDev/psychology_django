from modeltranslation.translator import translator, TranslationOptions
from .models import (
    PersonalityType, KeyMotivator, IdealWorkEnvironment, CoreValue, 
    PreferredWorkTask, ContributionToOrganization, TeamHelp, 
    TeamIrritate, TeamActionStep
)

class PersonalityTypeTranslationOptions(TranslationOptions):
    fields = (
        'name', 'summary', 'workplace_personality', 'working_with_team',
        'communicating_with_others', 'managing_conflict', 'taking_the_lead',
        'getting_things_done', 'growth_and_development', 'coping_with_stress',
        'achieving_success'
    )

class ChildModelTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(PersonalityType, PersonalityTypeTranslationOptions)
translator.register(KeyMotivator, ChildModelTranslationOptions)
translator.register(IdealWorkEnvironment, ChildModelTranslationOptions)
translator.register(CoreValue, ChildModelTranslationOptions)
translator.register(PreferredWorkTask, ChildModelTranslationOptions)
translator.register(ContributionToOrganization, ChildModelTranslationOptions)
translator.register(TeamHelp, ChildModelTranslationOptions)
translator.register(TeamIrritate, ChildModelTranslationOptions)
translator.register(TeamActionStep, ChildModelTranslationOptions)
