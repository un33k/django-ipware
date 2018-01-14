<<<<<<< HEAD
from django.apps import AppConfig as DjangoAppConfig
=======
from django.apps import AppConfig
>>>>>>> integration
from django.utils.translation import ugettext_lazy as _


class IPwareConfig(AppConfig):
    """
    Configuration entry point for the ipware app
    """
    label = name = 'ipware'
    verbose_name = _("ipware app")
