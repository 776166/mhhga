import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class CandidateQuerySet(models.QuerySet):
    def for_owner(self, user):
        return self.filter(owner=user)

    def active(self):
        return self.filter(is_deleted=False)


class Candidate(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="candidates",
    )

    is_visible = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)

    objects = CandidateQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["owner", "is_deleted", "-created_at"],
                name="cand_owner_del_created_idx",
            ),
        ]

    def __str__(self):
        return self.name

    def soft_delete(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save(update_fields=["is_deleted", "deleted_at"])
