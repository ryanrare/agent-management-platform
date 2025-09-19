from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Agent
from agent_platform.serializers import AgentSerializer
from agents.services.orchestrator import Orchestrator
from agents.services.documents import DocumentRetriever


class AgentListCreateAPIView(APIView):
    def get(self, request):
        agents = Agent.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Agent.objects.get(pk=pk)
        except Agent.DoesNotExist:
            return None

    def get(self, request, pk):
        agent = self.get_object(pk)
        if not agent:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AgentSerializer(agent)
        return Response(serializer.data)

    def put(self, request, pk):
        agent = self.get_object(pk)
        if not agent:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AgentSerializer(agent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        agent = self.get_object(pk)
        if not agent:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgentExecuteAPIView(APIView):
    def post(self, request, pk):
        try:
            agent = Agent.objects.get(pk=pk)
        except Agent.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        input_text = request.data.get("input")
        if not input_text:
            return Response({"detail": "Missing input."}, status=400)

        # 🔍 Busca documentos relevantes
        retriever = DocumentRetriever(agent)
        docs = retriever.search(input_text, top_k=5)
        context = "\n\n".join([f"{doc.title}: {doc.content}" for doc in docs])

        # 📝 Insere contexto na entrada do agente
        full_input = f"Use os seguintes documentos para responder:\n{context}\n\nPergunta: {input_text}"

        run = Orchestrator().run_workflow(agent, full_input)

        return Response({
            "agent": agent.id,
            "input": input_text,
            "context_docs": [{"title": d.title, "url": d.url} for d in docs],
            "output": run.output_text,
            "status": run.status
        })
