from restclients_core import models


class ZoomUser(models.Model):
    id = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=500)
    type = models.IntegerField()
    status = models.CharField(max_length=64)
    pmi = models.IntegerField()
    timezone = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    last_login_time = models.DateTimeField()
    verified = models.IntegerField()
