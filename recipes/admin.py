from django.contrib import admin
from recipes.models import UserProfile, Tag, Review, Rating, Recipe

admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Recipe)