from django.conf.urls import url
from resources.views import SubmitAccessRequestView, AccessRequestView

urlpatterns = [
    url(r'^access_request/(?P<pk>[0-9]+)/$', AccessRequestView.as_view(), name='access_request'),
    url(r'^access_request/(?P<pk>[0-9]+)/submit/$', SubmitAccessRequestView.as_view(), name='submit_access_request'),
]