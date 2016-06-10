from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from oauth_endpoint.models import Client


class Criteria(models.Model):
    name = models.CharField(max_length=127, verbose_name="Критерий")

    class Meta:
        verbose_name = "Критерий"
        verbose_name_plural = "Критерии"

    def __str__(self):
        return self.name


class Resource(models.Model):
    path = models.FilePathField(verbose_name="Путь", path="resources_folder", recursive=True)

    class Meta:
        verbose_name = "Ресурс"
        verbose_name_plural = "Ресурсы"

    def __str__(self):
        return self.path


class ResourceOwner(models.Model):
    user = models.ForeignKey(to=User, verbose_name="Владелец")
    resource = models.ForeignKey(to=Resource, verbose_name="Ресурс", related_name='owners')
    weight = models.IntegerField(verbose_name="Приоритет")

    class Meta:
        verbose_name = "Владелец ресурса"
        verbose_name_plural = "Владельцы ресурса"

    def __str__(self):
        return self.user.__str__()


class ResourceCriteria(models.Model):
    criteria = models.ForeignKey(to=Criteria, verbose_name="Критерий")
    resource = models.ForeignKey(to=Resource, verbose_name="Ресурс", related_name='criteria')
    weight = models.IntegerField(verbose_name="Приоритет")

    class Meta:
        verbose_name = "Критерий ресурса"
        verbose_name_plural = "Критерии ресурса"

    def __str__(self):
        return self.criteria.name


class ResourceAccessRequest(models.Model):
    resource = models.ForeignKey(to=Resource, verbose_name="Ресурс")
    created_at = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    user = models.ForeignKey(to=User, verbose_name="Инициатор")
    client = models.ForeignKey(to=Client, verbose_name="Клиент")
    submitted = models.BooleanField(verbose_name="Подтвержден")
    code = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Запрос на получение доступа"
        verbose_name_plural = "Запросы на получение доступа"

    def __str__(self):
        return "{0} ({1})".format(self.resource, self.created_at)

    def get_absolute_url(self):
        return reverse('resources:access_request', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ResourceAccessRequest, self).save(force_insert, force_update, using, update_fields)

        owners = ResourceOwner.objects.filter(resource=self.resource).all()
        criteria = ResourceCriteria.objects.filter(resource=self.resource).all()

        for owner in owners:
            for criterion in criteria:
                OwnersMark.objects.update_or_create(owner=owner, criteria=criterion, request=self)


class OwnersMark(models.Model):
    owner = models.ForeignKey(to=ResourceOwner, verbose_name="Владелец")
    criteria = models.ForeignKey(to=ResourceCriteria, verbose_name="Критерий")
    mark = models.FloatField(verbose_name="Оценка", null=True, blank=True)
    request = models.ForeignKey(to=ResourceAccessRequest, verbose_name="Запрос", related_name='marks')

    def user_marks(self):
        return self.marks.filter(user=self.owner.user)

    class Meta:
        verbose_name = "Оценка владельца по критерию"
        verbose_name_plural = "Оценки владельца по критериям"

    def __str__(self):
        return "{0} - {1}".format(self.owner, self.criteria)
