import django
from django.db import models
from datetime import date
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class UserProfile(models.Model):
    FIRST_NAME_LEN = 50
    LAST_NAME_LEN = 50
    USER_DESCRIPTION_LEN = 200

<<<<<<< HEAD
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
=======
    user = models.OneToOneField(User, on_delete=models.CASCADE)
>>>>>>> Zebedee
    # TODO: do we need a minimum length for user_name, password, etc?
    first_name = models.CharField(max_length=FIRST_NAME_LEN, blank=True)
    last_name = models.CharField(max_length=LAST_NAME_LEN, blank=True)
    date_of_birth = models.DateField(default=django.utils.timezone.now, blank=True)
    # TODO: look at how rango handled user passwords etc.
    user_description = models.TextField(max_length=USER_DESCRIPTION_LEN, blank=True)
<<<<<<< HEAD
    profile_picture = models.ImageField(upload_to='profile_images/', null=True, blank=True)
=======
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
>>>>>>> Zebedee
    user_name_slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.user_name_slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Profiles"


class Recipe(models.Model):
    NAME_LEN = 255
    TEXT_LEN = 3000
    INGREDIENTS_LEN = 1000

    creator = models.ForeignKey(UserProfile, related_name="creator", on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_LEN, unique=True)
    text = models.TextField(max_length=TEXT_LEN)
    ingredients = models.TextField(max_length=INGREDIENTS_LEN)
    views = models.IntegerField(default=0)
    no_of_ratings = models.IntegerField(default=0)
    # TODO: add recipe_picture upload to form and poplation script
    recipe_picture = models.ImageField()
    saved_by = models.ManyToManyField(UserProfile)

    recipe_name_slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.recipe_name_slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

    western = models.BooleanField(default=False)
    asian = models.BooleanField(default=False)
    indian = models.BooleanField(default=False)
    chinese = models.BooleanField(default=False)
    african = models.BooleanField(default=False)
    american = models.BooleanField(default=False)
    other = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Review(models.Model):
    TEXT_LEN = 2000

    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.TextField(TEXT_LEN)
    image = models.ImageField()
    no_of_ratings = models.IntegerField(default=0)
    # TODO: minvaluevalidtor and maxvaluevalidtor?
    review_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.creator.user_name + " review " + str(self.id)


class Rating(models.Model):
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    # True = recipe, False = review
    recipe_or_review = models.BooleanField(default=True)
    # 5 star scale on 1-10 scale e.g 1 = 0.5 stars
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.creator.user_name + " rating " + str(self.id)


class Tag(models.Model):
    TAG_MAX_LEN = 50#

    WESTERN_TAG = "Western"
    ASIAN_TAG = "Asian"
    INDIAN_TAG = "Indian"
    CHINESE_TAG = "Chinese"
    AFRICAN_TAG = "African"
    AMERICAN_TAG = "American"
    OTHER_TAG = "Other"

    tag = models.CharField(max_length=TAG_MAX_LEN)
    # TODO: we will probably need special logic to call when a recipe is deleted to handle tag
    recipe = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.tag
