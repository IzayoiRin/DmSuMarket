from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class UserModel(AbstractUser):

    mobile = models.CharField(max_length=11, verbose_name='mobile')

    class Meta:

        db_table = 'tb_user'
        verbose_name = 'User'
