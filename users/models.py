from django.db import models
from django.contrib.auth.models import User
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class FlashcardSets(models.Model):
    setTitle = models.CharField(max_length=120)
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='setOwner')
    access = models.ManyToManyField(User, related_name='setAccess')
    shareKey = models.CharField(max_length=50, default=generate_uuid, null=False)


class Flashcard(models.Model):
    setTitle = models.ForeignKey(FlashcardSets, on_delete=models.CASCADE)
    question = models.CharField(max_length=120)
    answer = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class PremiumAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isPremium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.isPremium}"