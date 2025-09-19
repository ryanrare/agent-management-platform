"""
URL configuration for agent_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from agents.views import (
    AgentListCreateAPIView,
    AgentDetailAPIView,
    AgentExecuteAPIView
)
from prompts.views import (
    PromptListCreateAPIView,
    PromptDetailAPIView
)

urlpatterns = [
    # Agents
    path("api/v1/agents/", AgentListCreateAPIView.as_view(), name="agent-list"),
    path("api/v1/agents/<int:pk>/", AgentDetailAPIView.as_view(), name="agent-detail"),
    path("api/v1/agents/<int:pk>/execute/", AgentExecuteAPIView.as_view(), name="agent-execute"),

    # Prompts
    path("api/v1/prompts/", PromptListCreateAPIView.as_view(), name="prompt-list"),
    path("api/v1/prompts/<int:pk>/", PromptDetailAPIView.as_view(), name="prompt-detail"),
]
