
# 🤖 Agent Management Platform

Plataforma de **Gestão de Agentes de IA** com orquestração de workflows usando **LangGraph**, RAG e suporte a múltiplos agentes especializados.

---

## 📋 Descrição

Este projeto permite:

* Criar e gerenciar agentes de IA
* Configurar prompts customizados
* Executar workflows multi-agente
* Fazer **RAG (Retrieval-Augmented Generation)**, integrando documentos externos

---

## 🏗️ Arquitetura

* Django + DRF → API backend
* LangGraph → Orquestração de agentes
* PostgreSQL → Banco de dados principal
* Docker → Containerização

---

## ⚙️ Pré-requisitos

* Docker 20+
* Docker Compose 2+

---

## 📝 Configuração

1. Clone o repositório e entre na pasta:

```
git clone https://github.com/ryanrare/agent-management-platform.git && cd agent-management-platform
```

2. Crie o arquivo `.env` na raiz do projeto:

```
echo "DEBUG=1
SECRET_KEY=django-insecure-xyz
POSTGRES_DB=agentdb
POSTGRES_USER=agentusr
POSTGRES_PASSWORD=secret
POSTGRES_HOST=db
POSTGRES_PORT=5432
OPENAI_API_KEY=sk-xxxx" > .env
```

---

## 🚀 Rodando com Docker

Suba os containers:

```
sudo docker compose up --build -d
```

Se aparecer warning de containers órfãos:

```
sudo docker compose down --remove-orphans && docker compose up --build -d
```

### Rodar migrações

```
sudo docker compose exec web python manage.py migrate
```

### Importar documentos externos (RAG) via call comand do Django (apenas .html e .txt):

```
sudo docker compose exec web python manage.py crawl_docs --url "https://www.gutenberg.org/files/1342/1342-0.txt"
```

### Criar superusuário (opcional)

```
docker compose exec web python manage.py createsuperuser
```

---

## 📂 Estrutura de pastas resumida

```
agent_platform/
  ├── serializers.py         # Serializers geral para APIS
  ├── settings.py            # Configuracoes do projeto
  ├── urls.py                # Urls gerais do projeto(pode ser abstraido para cada pasta)
agents/
  ├── management/commands/   # call_command (ex: crawl_docs) Extracao via bot RAG
  ├── models.py              # Agent, Document, Execution
  ├── views.py               # APIs CRUD de Agents e Executions
  ├── services/orchestrator.py # LangGraph orchestrator
  ├── services/documents.py    # Busca semantica no RAG

prompts/
  ├── models.py              # Prompt, PromptVersion
  ├── views.py               # APIs CRUD de Prompts
docker-compose.yml
Dockerfile
requirements.txt
.env_example
```

---

## 🧪 Comandos úteis dentro do container web

### Banco de dados
```
python manage.py migrate
```

### Importar documentos externos (RAG)
```
python manage.py crawl_docs --url "https://www.gutenberg.org/files/1342/1342-0.txt"
```

### Criar superusuário
```
python manage.py createsuperuser
```

---

## 📡 Endpoints da API

### 🔹 Agents

**Listar todos os agentes**
```
GET /api/v1/agents/
```

**Criar agente**
```
POST /api/v1/agents/
{
  "name": "Research Assistant",
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "config": {},
  "prompt_id": "uuid-do-prompt"
}
```

**Obter detalhes de um agente**
```
GET /api/v1/agents/{id}/
```

**Atualizar agente**
```
PUT /api/v1/agents/{id}/
{
  "name": "Updated Assistant",
  "model": "gpt-4o-mini",
  "temperature": 0.9,
  "config": {},
  "prompt_id": "uuid-do-prompt"
}
```

**Deletar agente**
```
DELETE /api/v1/agents/{id}/
```

**Executar agente**
```
POST /api/v1/agents/{id}/execute/
{
  "input": "Qual a capital da França?"
}
```

---

### 🔹 Prompts

**Listar prompts**
```
GET /api/v1/prompts/
```

**Criar prompt**
```
POST /api/v1/prompts/
{
  "name": "Prompt Exemplo",
  "content": "Olá, responda conforme as instruções..."
}
```

**Obter detalhes de um prompt**
```
GET /api/v1/prompts/{id}/
```

**Atualizar prompt**
```
PUT /api/v1/prompts/{id}/
{
  "name": "Prompt Atualizado",
  "content": "Nova instrução..."
}
```

**Deletar prompt**
```
DELETE /api/v1/prompts/{id}/
```

---

### 🔹 Executions (Histórico de execuções)

**Listar execuções**
```
GET /api/v1/executions/
```

**Criar execução (manual)**
```
POST /api/v1/executions/
{
  "agent_id": "uuid-do-agente",
  "input": "Pergunta de teste"
}
```

**Obter detalhes de uma execução**
```
GET /api/v1/executions/{id}/
```

---
