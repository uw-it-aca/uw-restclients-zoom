from restclients_core import models
from dateutil.parser import parse


class ZoomUser(models.Model):
    TYPE_BASIC = 1
    TYPE_PRO = 2
    TYPE_CORP = 3
    TYPE_CHOICES = (
        (TYPE_BASIC, 'Basic'), (TYPE_PRO, 'Pro'), (TYPE_CORP, 'Corp')
    )

    id = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=500)
    type = models.IntegerField(choices=TYPE_CHOICES)
    status = models.CharField(max_length=64)
    pmi = models.IntegerField()
    timezone = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    last_login_time = models.DateTimeField()
    verified = models.IntegerField()

    @staticmethod
    def from_json(data):
        user = ZoomUser()
        user.id = data['id']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.type = data['type']
        user.status = data['status']
        user.pmi = data['pmi']
        user.timezone = data['timezone']
        user.dept = data['dept']
        user.verified = data['verified']
        user.created_at = parse(data['created_at'])
        user.last_login_time = parse(data['last_login_time'])
        return user
