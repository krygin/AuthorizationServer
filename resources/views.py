import re

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.forms import HiddenInput, BooleanField, CharField
from django.http import HttpResponseRedirect
from django.views import generic

# Create your views here.
from resources.models import ResourceAccessRequest, ResourceCriteria, OwnersMark, ResourceOwner


class SubmitAccessRequestForm(forms.ModelForm):
    submitted = BooleanField(widget=HiddenInput)

    class Meta:
        model = ResourceAccessRequest
        fields = ('submitted',)


class SubmitAccessRequestView(LoginRequiredMixin, generic.UpdateView):
    form_class = SubmitAccessRequestForm
    model = ResourceAccessRequest
    template_name = 'resources/access_request_submit.html'

    def get_success_url(self):
        return reverse('resources:access_request', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        return SubmitAccessRequestForm

    def get_form(self, form_class=None):
        form = super(SubmitAccessRequestView, self).get_form(form_class=form_class)
        form.initial = {'submitted': True}
        return form

    def form_valid(self, form):
        self.object.submitted = form.fields['submitted']
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UserMarksForm(forms.ModelForm):
    class Meta:
        model = ResourceAccessRequest
        fields = []

    def set_marks(self, marks_queryset):
        for mark in marks_queryset:
            self.fields['criterion_{0}'.format(mark.criteria.pk)] = CharField(label=mark.criteria.criteria.name,
                                                                              initial=mark.mark)


class AccessRequestView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'resources/access_request.html'
    model = ResourceAccessRequest

    def get_form_class(self):
        return UserMarksForm

    def get_form(self, form_class=None):
        form = super(AccessRequestView, self).get_form(form_class=form_class)
        marks = self.object.marks.all()
        filtered_marks = marks.filter(owner__user=self.request.user)
        form.set_marks(filtered_marks)
        return form

    def form_valid(self, form):
        for field in form.fields:
            criterion_id = re.search(r'^criterion_(?P<id>[0-9]+)$', field).group('id')
            owner = ResourceOwner.objects.get(resource=self.object.resource, user=self.request.user)
            mark = form.cleaned_data[field]
            mark_object = OwnersMark.objects.get(owner=owner, request=self.object, criteria_id=criterion_id)
            mark_object.mark = mark
            mark_object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super(AccessRequestView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('resources:access_request', kwargs={'pk': self.object.pk})
