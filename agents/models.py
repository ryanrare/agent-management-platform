from django.db import models
from prompts.models import Prompt
import uuid
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Agent(models.Model):
    TYPES = [
        ("research", "Research"),
        ("code", "Code"),
        ("analysis", "Analysis"),
    ]
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=50, choices=TYPES)
    model = models.CharField(max_length=50, default="gpt-4o")
    temperature = models.FloatField(default=0.7)
    prompt = models.ForeignKey(Prompt, on_delete=models.SET_NULL, null=True, blank=True)
    config = models.JSONField(default=dict)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Execution(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE, related_name="executions")
    input = models.TextField()
    output = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Execution {self.id} - {self.agent.name} ({self.status})"


class Document(models.Model):
    url = models.URLField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    embedding = ArrayField(models.FloatField(), blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title or f"Doc {self.id}"
