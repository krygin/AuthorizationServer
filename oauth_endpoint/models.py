from AuthorizationServer.utils import generate_client_secret
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=127, verbose_name="Имя")
    secret = models.CharField(max_length=32, default=generate_client_secret, verbose_name="Секрет")
    owner = models.ForeignKey(to=User, verbose_name="Владелец клиента")
    redirect_uri = models.CharField(max_length=127, null=True, blank=True, verbose_name="Redirect URI")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.name
