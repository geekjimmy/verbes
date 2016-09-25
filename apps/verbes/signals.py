from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in)
def login_notifier(sender, request, user, **kwargs):
    messages.add_message(request, messages.SUCCESS, 'Vous êtes maintenant connecté avec le compte {}'.format(user.email))

@receiver(user_logged_out)
def logout_notifier(sender, request, user, **kwargs):
    messages.add_message(request, messages.SUCCESS, 'Déconnexion réussie.')
