import openai
from django.conf import settings
from langchain_core.runnables.graph import Node, Graph
from agents.models import Agent


class RunResult:
    def __init__(self, input_text, output_text, status="success"):
        self.input_text = input_text
        self.output_text = output_text
        self.status = status


client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


def research_agent(input_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Pesquise sobre: {input_text}"}],
        max_tokens=300
    )
    return f"[Research] {response.choices[0].message.content}"


def analysis_agent(input_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Analise: {input_text}"}],
        max_tokens=300
    )
    return f"[Analysis] {response.choices[0].message.content}"


def code_agent(input_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Escreva código para: {input_text}"}],
        max_tokens=300
    )
    return f"[Code] {response.choices[0].message.content}"


class WorkflowMemory:
    def __init__(self):
        self.history = []

    def add(self, node_name: str, output: str):
        self.history.append({"node": node_name, "output": output})

    def get_context(self):
        # Concatena todos os outputs anteriores xd
        return "\n".join([f"{h['node']}: {h['output']}" for h in self.history])


class Orchestrator:
    def run_workflow(self, agent: Agent, input_text: str) -> RunResult:
        """
        Executa o workflow LangGraph com 3 agentes mockados e imprime o fluxo.
        """

        # Cria o grafo
        graph = Graph()
        print("📌 Grafo criado")

        # Adiciona nodes
        node_research = graph.add_node(research_agent, metadata={"role": "research"})
        print(f"✅ Node criado: {node_research.name} | ID: {node_research.id}")

        node_analysis = graph.add_node(analysis_agent, metadata={"role": "analysis"})
        print(f"✅ Node criado: {node_analysis.name} | ID: {node_analysis.id}")

        node_code = graph.add_node(code_agent, metadata={"role": "code"})
        print(f"✅ Node criado: {node_code.name} | ID: {node_code.id}")

        # Conecta nodes (fluxo: research -> analysis -> code)
        graph.add_edge(node_research, node_analysis)
        print(f"🔗 Conectado: {node_research.name} -> {node_analysis.name}")

        graph.add_edge(node_analysis, node_code)
        print(f"🔗 Conectado: {node_analysis.name} -> {node_code.name}")

        # Executa o grafo (simulação sequencial)
        memory = WorkflowMemory()
        current_output = input_text

        for node in [node_research, node_analysis, node_code]:
            # Passa contexto da memória para o agente
            context = memory.get_context()
            print(f"🏃 Executando node: {node.name} com input: {current_output} e contexto:\n{context}")
            current_output = node.data(f"{context}\n{current_output}")
            memory.add(node.name, current_output)
            print(f"📤 Output do node {node.name}: {current_output}")

        print("✅ Workflow finalizado")
        return RunResult(input_text, current_output)
