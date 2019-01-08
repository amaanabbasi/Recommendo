from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


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
    # interests =models.ForeignKey(

    # )

    def __str__(self):
        return self.user_id.username


class Interest(models.Model):
    # user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

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


class Interest2(models.Model):
    interest_name = models.ManyToManyField(Interest)
    # interest_level = models.DecimalField(
    #     default=0,
    #     validators=[MaxValueValidator(5.0), MinValueValidator(0.0)],
    #     decimal_places=1, max_digits=6,
    # )
    # bf=models.BooleanField()


class Interest3(models.Model):
    interest_x = models.OneToOneField(Interest2, on_delete=models.CASCADE)
    interest_level = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(5.0), MinValueValidator(0.0)],
        decimal_places=1, max_digits=6,
    )


class Event(models.Model):
    name = models.CharField(max_length=250, blank=True)
    event_id = models.BigAutoField(primary_key=True)  # unique
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True)
    # user_id of the user who created the event
    user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    lat = models.DecimalField(
        decimal_places=3, max_digits=6, blank=True, null=True)
    lng = models.DecimalField(
        decimal_places=3, max_digits=6, blank=True, null=True)

    # going to event: 4 conditions
    # yes = models.ManyToManyField(
    #     AppUser,
    #     related_name='events',
    #     default=1,
    #     blank=True,
    # )
    # maybe = models.ManyToManyField(
    #     AppUser,
    #     related_name='events',
    # )
    # invited = models.ManyToManyField(
    #     AppUser,
    #     related_name='events',
    # )
    # no = models.ManyToManyField(
    #     AppUser,
    #     related_name='events',
    # )

    def __str__(self):
        return str(self.event_id)
