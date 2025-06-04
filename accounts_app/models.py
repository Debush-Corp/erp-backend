from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserActivity(models.Model):
    """
    Modelo para registrar actividades de los usuarios en el sistema.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=100, verbose_name=_("Action"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Timestamp"))
    module = models.CharField(max_length=50, blank=True, verbose_name=_("Module"))

    class Meta:
        verbose_name = _("User Activity")
        verbose_name_plural = _("User Activities")
        db_table = 'auth_user_activity'

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"