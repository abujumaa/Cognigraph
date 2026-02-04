import time
from typing import List, Dict
from src.utils.logger import logger


class MockS3Fetcher:
    def fetch_documents(self, bucket: str, prefix: str):
        logger.info(f"Fetching from s3://{bucket}/{prefix}...")
        return ["Doc 1 content...", "Doc 2 content..."]


class TextChunker:
    def chunk(self, text: str):
        return [text[i : i + 100] for i in range(0, len(text), 100)]


class IngestionPipeline:
    def __init__(self):
        # Initialize clients for Neo4j and Qdrant here
        pass

    def run(self):
        logger.info("Starting ingestion pipeline...")
        fetcher = MockS3Fetcher()
        chunker = TextChunker()

        docs = fetcher.fetch_documents("enterprise-data", "raw")

        for doc in docs:
            chunks = chunker.chunk(doc)

            # 1. Embedding -> Qdrant
            # self.qdrant_client.upsert(...)
            logger.info(f"Ingested {len(chunks)} chunks to Qdrant.")

            # 2. Entity Extraction -> Neo4j
            # entities = extract_entities(doc)
            # self.neo4j_session.run(...)
            logger.info(f"Ingested entities/relations to Neo4j.")


if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run()
