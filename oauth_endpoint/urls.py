from django.conf.urls import url
from oauth_endpoint.views import AuthorizeView, CodeView

urlpatterns = [
    url(r'^authorize/$', AuthorizeView.as_view()),
    url(r'^code/(?P<pk>[0-9]+)/$', CodeView.as_view(), name='code')
]