from django.db import models



class UserProfile(models.Model):

    FIRST_NAME_LEN = 50
    LAST_NAME_LEN = 50
    EMAIL_LEN = 320
    PASSWORD_LEN = 255
    USER_DESCRIPTION_LEN = 200
    USER_NAME_LEN = 50

    # TODO: do we need a minimum length for user_name, password, etc?
    user_name = models.CharField(max_length=USER_NAME_LEN, unique=True)
    first_name = models.CharField(max_length=FIRST_NAME_LEN)
    last_name = models.CharField(max_length=LAST_NAME_LEN)
    email = models.EmailField(max_length=EMAIL_LEN)
    date_of_birth = models.DateField()
    # TODO: look at how rango handled user passwords etc.
    password = models.CharField(max_length=PASSWORD_LEN)
    user_description = models.TextField(max_length=USER_DESCRIPTION_LEN)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "User Profiles"

class Recipe(models.Model):

    NAME_LEN = 255
    TEXT_LEN = 3000
    INGREDIENTS_LEN = 1000

    name = models.CharField(max_length=NAME_LEN, unique=True)
    text = models.TextField(max_length=TEXT_LEN)
    ingredients = models.TextField(max_length=INGREDIENTS_LEN)
    views = models.IntegerField()
    noOfRatings = models.IntegerField()
    recipePicture = models.ImageField()
    savedBy = models.ManyToManyField(UserProfile)
    def __str__(self):
        return self.name

class Review(models.Model):

    TEXT_LEN = 2000

    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(TEXT_LEN)
    image = models.ImageField()
    noOfRatings = models.IntegerField()
    # TODO: minvaluevalidtor and maxvaluevalidtor?
    review_rating = models.IntegerField(max)

    def __str__(self):
        return self.name

class Rating(models.Model):

    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # True = recipe, False = review
    recipeOrReview = models.BooleanField()
    rating = models.IntegerField()

    def __str__(self):
        return self.name

class Tag(models.Model):

    TAG_MAX_LEN = 50

    tag = models.CharField(max_length=TAG_MAX_LEN)
    # TODO: we will probably need special logic to call when a recipe is deleted to handle tag
    recipe = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.name
