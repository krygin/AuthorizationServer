# Create your views here.
from uuid import uuid4

import numpy
from AuthorizationServer.utils import generate_code

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views import generic
from oauth_endpoint.models import Client
from resources.models import ResourceAccessRequest, Resource


class AuthorizeView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        client_id = self.request.GET.get("client_id")
        resource_id = self.request.GET.get("resource_id")
        client = Client.objects.get(pk=client_id)
        resource = Resource.objects.get(pk=resource_id)

        access_request = ResourceAccessRequest.objects.create(resource=resource, client=client,
                                                              user_id=user.id, submitted=False)
        return reverse('resources:submit_access_request', kwargs={'pk': access_request.pk})


class CodeView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, pk=None, **kwargs):
        access_request = ResourceAccessRequest.objects.get(pk=pk)
        owners = access_request.resource.owners.all()
        criteria = access_request.resource.criteria.all()
        marks = access_request.marks.all()
        client = access_request.client
        # criteria = ResourceCriteria.objects.filter(resource=access_request.resource)
        # owners = ResourceOwner.objects.filter(resource=access_request.resource)

        # Приоритеты согласующих по отношению к цели

        owners_priorities = []
        sum = 0
        for owner in owners:
            sum += owner.weight

        for owner in owners:
            owners_priorities.append(owner.weight / sum)

        owners_priorities_matrix = numpy.array(owners_priorities)

        # Приоритеты критериев по отношению к согласующим

        owners_marks = []
        for owner in owners:
            owner_marks = []
            sum = 0
            for criterion in criteria:
                sum += marks.get(owner=owner, criteria=criterion).mark

            for criterion in criteria:
                owner_marks.append(marks.get(owner=owner, criteria=criterion).mark / sum)

            owners_marks.append(owner_marks)

        marks_matrix = numpy.array(owners_marks)

        # Приоритеты альтернатив по отношению к критериям

        criteria_priorities = []
        sum = 0
        for criterion in criteria:
            sum += criterion.weight

        criterion_properties = []
        for criterion in criteria:
            criterion_properties.append(criterion.weight / sum)

        criteria_priorities.append(criterion_properties)

        criterion_properties = []
        for criterion in criteria:
            base = 1 / (criterion.weight / sum)
            criterion_properties.append(base)

        sum = 0
        for criterion in criterion_properties:
            sum += criterion

        for i, criterion in enumerate(criterion_properties):
            criterion_properties[i] = criterion / sum

        criteria_priorities.append(criterion_properties)

        criteria_priorities = list(map(list, zip(*criteria_priorities)))

        for priority in criteria_priorities:
            sum = 0
            for i in priority:
                sum += i
            for i, p in enumerate(priority):
                priority[i] = p / sum

        criteria_priorities_matrix = numpy.array(criteria_priorities)

        print("Матрица приоритетов владельцев по отношению к фокусу")
        print(owners_priorities_matrix)
        print("Матрица приоритеов критериев по отношению к владельцам")
        print(marks_matrix)

        # print("Владельцы * Оценки")
        owners_dot_marks = numpy.dot(owners_priorities_matrix, marks_matrix)
        # print(owners_dot_marks)

        print("Матрица приоритетов альтернатив по отношению к критериям")
        print(criteria_priorities_matrix)

        result = numpy.dot(owners_dot_marks, criteria_priorities_matrix)

        print("Результат")
        print(result)
        if result.size == 2:
            if result[0] > result[1]:
                access_request.code = generate_code()
                access_request.save()
                return "{0}?{1}".format(client.redirect_uri, 'code={0}'.format(access_request.code))
            else:
                return "{0}?{1}".format(client.redirect_uri, 'error={0}'.format('access_denied'))
