
import uuid

from django.db import models
from django.utils import timezone


class ResumeQuerySet(models.QuerySet):
    def for_owner(self, user):
        return self.filter(candidate__owner=user)

    def active(self):
        return self.filter(
            is_deleted=False,
            candidate__is_deleted=False,
        )


class Resume(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    candidate = models.ForeignKey(
        "candidates.Candidate",
        on_delete=models.CASCADE,
        related_name="resumes",
        verbose_name="Кандидат",
    )

    title = models.CharField("Название", max_length=255)
    content = models.TextField("Текст резюме", blank=True)

    education = models.ManyToManyField(
        "candidates.Education",
        blank=True,
        related_name="resumes",
        verbose_name="Образование",
    )

    employment_descriptions = models.ManyToManyField(
        "candidates.EmploymentDescription",
        blank=True,
        related_name="resumes",
        verbose_name="Опыт работы",
    )

    skills = models.ManyToManyField(
        "candidates.Skill",
        blank=True,
        related_name="resumes",
        verbose_name="Навыки",
    )

    about = models.ManyToManyField(
        "candidates.About",
        blank=True,
        related_name="resumes",
        verbose_name="О себе",
    )

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    objects = ResumeQuerySet.as_manager()

    class Meta:
        verbose_name = "резюме"
        verbose_name_plural = "резюме"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def soft_delete(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save(update_fields=["is_deleted", "deleted_at"])
