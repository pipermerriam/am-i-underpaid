from django.conf.urls import patterns, url

from disparity.apps.salary import views


urlpatterns = patterns(
    '',
    # Survey Creation
    url(r'^survey/create/$', views.SurveyCreateView.as_view(), name='survey-create'),
    url(
        r'^survey/(?P<token>[-a-zA-Z0-9_:]+)/$',
        views.SurveyDetailView.as_view(),
        name='survey-detail',
    ),
    url(
        r'^survey/(?P<token>[-a-zA-Z0-9_:]+)/finalize/$',
        views.SurveyFinalizeView.as_view(),
        name='survey-finalize',
    ),
)
