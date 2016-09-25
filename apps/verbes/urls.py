from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.AttempView.as_view(), name='attempt'),
    url(r'^resultat$', views.FeedbackView.as_view(), name='attempt-feedback'),
    url(r'^resultats$', views.ResultsView.as_view(), name='results'),
    url(r'^mode-temps$', views.UserMoodTenseView.as_view(), name='user-mood-tense'),

    url('^inscription$', views.RegistrationView.as_view(), name='registration'),
    url('^connexion$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url('^deconnexion$', auth_views.logout, name='logout'),
    url('^mot-de-passe/reinitialisation$', auth_views.password_reset, name='password_reset'),
    url('^mot-de-passe/reinitialisation-envoyee$', auth_views.password_reset_done, name='password_reset_done'),
    url('^mot-de-passe/modifie$', auth_views.password_reset_complete, name='password_reset_complete'),
    url('^mot-de-passe/changer/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', auth_views.password_reset_confirm, name='password_reset_confirm'),

]
