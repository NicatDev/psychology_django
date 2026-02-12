from modeltranslation.translator import translator, TranslationOptions
from .models import PersonalityType

class PersonalityTypeTranslationOptions(TranslationOptions):
    fields = (
        'name', 'summary', 'workplace_personality', 'working_with_team',
        'communicating_with_others', 'managing_conflict', 'taking_the_lead',
        'getting_things_done', 'growth_and_development', 'coping_with_stress',
        'achieving_success', 'making_decisions',
        
        # JSON Fields
        'key_motivators', 'ideal_work_environments', 'core_values',
        'preferred_work_tasks', 'contributions_to_organization',
        'team_helps', 'team_irritates', 'team_action_steps',
        'communication_strengths', 'communication_misunderstanding', 'communication_action_steps',
        'conflict_help', 'conflict_triggered_by', 'conflict_irritate', 'conflict_action_steps',
        'inspire_others', 'make_things_happen', 'leadership_development',
        'decision_strengths', 'decision_challenges', 'decision_action_steps',
        'tasks_help', 'tasks_irritate', 'tasks_action_steps',
        'learning_improved', 'learning_hindered', 'how_you_view_change', 'opportunities_for_growth',
        'stress_triggers', 'best_stress_response', 'others_help_stress', 'worst_stress_response', 'others_worsen_stress',
        'potential_problems', 'suggestions_do', 'suggestions_dont'
    )

translator.register(PersonalityType, PersonalityTypeTranslationOptions)
