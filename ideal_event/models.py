from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


def upload_location(instance, filename):
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (instance.id, filename)


class AppUser(models.Model):
    name = models.CharField(max_length=250, blank=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    locale = models.CharField(default='en_IN', max_length=10)
    birthyear = models.IntegerField(default=1970)
    gender = models.CharField(default='Male', max_length=10)
    # joinedAt = models.DateTimeField(auto_now_add=True)
    location = models.CharField(default='Delhi', max_length=250)
    timezone = models.IntegerField(default=0)
    # friends = models.ManyToManyField('self')
    interests = models.ManyToManyField('KeyVal')

    def __str__(self):
        return self.user_id.username


class Interest(models.Model):
    # user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")

    height_field = models.IntegerField(default=400)
    width_field = models.IntegerField(default=500)

    def __str__(self):
        return self.name


class KeyVal(models.Model):
    container = models.ForeignKey(
        Interest, db_index=True, on_delete=models.CASCADE)
    # key:name
    name = models.CharField(max_length=250, db_index=True)
    # value:interest_level
    interest_level = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(5.0), MinValueValidator(0.0)],
        decimal_places=1, max_digits=6,
        db_index=True
    )

    def __str__(self):
        return self.container.name + ": " + str(self.interest_level)


class Grp(models.Model):
    name = models.CharField(max_length=30)
    appUsers = models.ManyToManyField(AppUser)
