from django.contrib import admin
from .models import Flashcard, FlashcardSets, PremiumAccount


admin.site.register(Flashcard)
admin.site.register(FlashcardSets)
admin.site.register(PremiumAccount)