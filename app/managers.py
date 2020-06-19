from django.db import models
from django.db.models import Sum

class LikesManager(models.Manager):
    use_for_related_fields = True

    def rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

