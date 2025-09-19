from django.core.management.base import BaseCommand
from django.conf import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from agents.models import Document

import requests


class Command(BaseCommand):
    help = "Crawl docs, gerar embeddings e salvar no banco"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            type=str,
            help="URL do documento a ser crawleado",
            default="https://meusite.com/docs.txt"
        )

    def handle(self, *args, **options):
        url = options["url"]
        self.stdout.write(f"📥 Baixando conteúdo de {url}...")

        # 1. Faz o download do documento
        resp = requests.get(url)
        if resp.status_code != 200:
            self.stderr.write(f"Erro ao baixar {url}: {resp.status_code}")
            return
        text = resp.text

        # 2. Split do texto
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(text)
        self.stdout.write(f"✂️ Texto dividido em {len(chunks)} chunks")

        # 3. Gerar embeddings
        embedder = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

        count = 0
        for chunk in chunks:
            vector = embedder.embed_query(chunk)

            # 4. Persistir no banco
            Document.objects.create(
                content=chunk,
                embedding=vector,
                url=url
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {count} chunks salvos no banco"))
