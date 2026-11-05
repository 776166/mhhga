from django.db import models

import uuid


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

    title = models.CharField(
        "Название",
        max_length=255,
    )

    content = models.TextField(
        "Текст резюме",
        blank=True,
    )

    created_at = models.DateTimeField(
        "Создано",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Обновлено",
        auto_now=True,
    )

    class Meta:
        verbose_name = "резюме"
        verbose_name_plural = "резюме"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

