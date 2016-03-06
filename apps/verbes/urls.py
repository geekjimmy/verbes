from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.AttempView.as_view(), name='attempt'),
    url(r'^resultat$', views.FeedbackView.as_view(), name='attempt-feedback'),
    url(r'^resultats$', views.ResultsView.as_view(), name='results'),
]
