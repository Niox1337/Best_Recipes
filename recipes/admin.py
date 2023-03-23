from django.contrib import admin
from recipes.models import UserProfile, Tag, Review, Rating, Recipe

admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Rating)


class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'recipe_name_slug': ('name',)}


admin.site.register(Recipe, RecipeAdmin)
