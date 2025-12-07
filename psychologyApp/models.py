from django.db import models
from django.conf import settings

class Test(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tests')
    created_at = models.DateTimeField(auto_now=True)

class Question(models.Model):
    text = models.TextField()
    dimension = models.CharField(max_length=10)  # EI, TF, JP, SN
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
    
