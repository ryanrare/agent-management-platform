from django.db import models


class Prompt(models.Model):
    key = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.key


class PromptVersion(models.Model):
    prompt = models.ForeignKey(Prompt, related_name="versions", on_delete=models.CASCADE)
    version = models.PositiveIntegerField()
    content = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("prompt", "version")
        ordering = ["-created_at"]
