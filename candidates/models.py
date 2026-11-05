
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseEntry(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    title = models.CharField("Название", max_length=255)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class CandidateEntry(BaseEntry):
    candidate = models.ForeignKey(
        "candidates.Candidate",
        on_delete=models.CASCADE,
        related_name="%(class)s_entries",
        verbose_name="Кандидат",
    )

    class Meta:
        abstract = True


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


class Education(CandidateEntry):
    class Meta:
        verbose_name = "образование"
        verbose_name_plural = "образование"


class Employment(CandidateEntry):
    class Meta:
        verbose_name = "место работы"
        verbose_name_plural = "места работы"


class EmploymentDescription(BaseEntry):
    employment = models.ForeignKey(
        Employment,
        on_delete=models.CASCADE,
        related_name="descriptions",
        verbose_name="Место работы",
    )

    class Meta:
        verbose_name = "описание опыта работы"
        verbose_name_plural = "описания опыта работы"


class Skill(CandidateEntry):
    class Level(models.TextChoices):
        BASIC = "basic", "Базовый"
        INTERMEDIATE = "intermediate", "Средний"
        ADVANCED = "advanced", "Продвинутый"

    level = models.CharField(
        "Уровень владения",
        max_length=16,
        choices=Level.choices,
    )

    class Meta:
        verbose_name = "навык"
        verbose_name_plural = "навыки"


class About(CandidateEntry):
    class Meta:
        verbose_name = "блок «О себе»"
        verbose_name_plural = "блоки «О себе»"
