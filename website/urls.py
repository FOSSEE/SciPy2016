from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = patterns('',
    url(r'^$', 'website.views.home', name='home'),
    url(r'^cfp/$', 'website.views.cfp', name='cfp'),
    url(r'^submit-cfp/$', 'website.views.submitcfp', name='submitcfp'),
    url(r'^submit-cfw/$', 'website.views.submitcfw', name='submitcfw'),
    url(r'^accounts/register/$', 'website.views.userregister', name='userregister'),
    # url(r'^view-abstracts/$', 'website.views.view_abstracts', name='view_abstracts'),
    url(r'^view-abstracts/$', 'website.views.view_abstracts', name='view_abstracts'),
    url(r'^abstract-details/(?P<proposal_id>\d+)$', 'website.views.abstract_details', name='abstract_details'),
    url(r'^view-abstracts/delete/$', 'website.views.delete', name='delete'),
    url(r'^comment-abstract/(?P<proposal_id>\d+)$', 'website.views.comment_abstract', name='comment_abstract'),
    url(r'^comment-abstract/status/(?P<proposal_id>\d+)$', 'website.views.status', name='status'),

  )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
