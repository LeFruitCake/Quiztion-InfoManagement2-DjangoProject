from django.db import models
from django.contrib.auth.models import User

class FlashcardSets(models.Model):
    setTitle = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Created by: {self.author} Titled: {self.setTitle}"


class Flashcard(models.Model):
    setTitle = models.ForeignKey(FlashcardSets, on_delete=models.CASCADE)
    question = models.CharField(max_length=120)
    answer = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.setTitle} - {self.question}"

class PremiumAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isPremium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.isPremium}"