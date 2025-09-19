# src/serializers.py
from rest_framework import serializers

from agents.models import Agent, Execution
from prompts.models import Prompt


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = [
            "id",
            "name",
            "content",
            "version",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AgentSerializer(serializers.ModelSerializer):
    prompt = PromptSerializer(read_only=True)
    prompt_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Agent
        fields = [
            "id",
            "name",
            "model",
            "temperature",
            "config",
            "prompt",
            "prompt_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ExecutionSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    agent_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Execution
        fields = [
            "id",
            "agent",
            "agent_id",
            "input",
            "output",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "output", "status", "created_at", "updated_at"]
