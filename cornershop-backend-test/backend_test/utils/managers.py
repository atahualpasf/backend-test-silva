"""Django model managers utilities."""

# Django
from django.db import models


class SoftDeleteManager(models.Manager):
    """
    Manager that limits the queryset by default to show only not deleted
    instances of model.
    """

    def get_queryset(self):
        """
        Return queryset limited to not deleted entries.
        """
        query_set = super(SoftDeleteManager, self).get_queryset()
        return query_set.filter(is_deleted=False)
