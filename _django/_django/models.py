from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    inst = models.CharField(max_length=300)
    usr_type = models.CharField(max_length=20)
    global_rank = models.IntegerField(default=0)
    country_rank = models.IntegerField(default=0)
    ratings = models.IntegerField(default=0)
    objects = models.Manager()

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username
