from crum import get_current_user
from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name="user_creation_%(app_label)s_%(class)s",
                                      null=True, blank=True, editable=False)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name="user_updated_%(app_label)s_%(class)s",
                                     null=True, blank=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super().save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        abstract = True
