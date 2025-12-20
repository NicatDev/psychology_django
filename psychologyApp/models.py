from django.db import models
from django.conf import settings

class Test(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tests')
    created_at = models.DateTimeField(auto_now=True)
    result_values = models.JSONField(null=True,blank=True)
    result = models.TextField(null=True,blank=True)

class Question(models.Model):
    text = models.TextField()
    dimension = models.CharField(max_length=10) 
    type = models.CharField(max_length=50, default='likert')  

    def __str__(self):
        return f"{self.text} - {self.text[:50]}"


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    value = models.JSONField()  # E.g. {"E": 5, "I":1}

    def __str__(self):
        return f"{self.question.text[:20]} - {self.text}"


class Answer(models.Model):
    test = models.ForeignKey(Test, related_name='answers', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.option.question.text}"
    

class PersonalityType(models.Model):
    code = models.CharField(max_length=10, unique=True)  # INTJ, INTP
    name = models.CharField(max_length=100)
    summary = models.TextField()
    workplace_personality = models.TextField()
    working_with_team = models.TextField()
    communicating_with_others = models.TextField()
    managing_conflict = models.TextField()
    taking_the_lead = models.TextField()
    getting_things_done = models.TextField()
    growth_and_development = models.TextField()
    coping_with_stress = models.TextField()
    achieving_success = models.TextField()

    def __str__(self):
        return self.code

class KeyMotivator(models.Model):
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, related_name="key_motivators")
    name = models.CharField(max_length=255)

class IdealWorkEnvironment(models.Model):
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, related_name="ideal_work_environments")
    name = models.CharField(max_length=255)

class CoreValue(models.Model):
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, related_name="core_values")
    name = models.CharField(max_length=255)

class PreferredWorkTask(models.Model):
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, related_name="preferred_work_tasks")
    name = models.CharField(max_length=255)

class ContributionToOrganization(models.Model):
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, related_name="contributions_to_organization")
    name = models.CharField(max_length=255)

class TeamHelp(models.Model):
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, related_name="team_helps")
    name = models.CharField(max_length=255)

class TeamIrritate(models.Model):
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, related_name="team_irritates")
    name = models.CharField(max_length=255)

class TeamActionStep(models.Model):
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, related_name="team_action_steps")
    name = models.CharField(max_length=255)

