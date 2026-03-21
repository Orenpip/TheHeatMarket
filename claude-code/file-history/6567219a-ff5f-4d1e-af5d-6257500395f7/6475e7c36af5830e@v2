import voyageai
from app.config import get_settings


class EmbeddingService:
    def __init__(self):
        settings = get_settings()
        self.client = voyageai.Client(api_key=settings.voyage_api_key)
        self.model = "voyage-3"
        self.dimensions = 1024

    def embed_text(self, text: str) -> list[float]:
        """Embed a single text string."""
        result = self.client.embed([text], model=self.model)
        return result.embeddings[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts in a single API call."""
        if not texts:
            return []
        result = self.client.embed(texts, model=self.model)
        return result.embeddings


embedding_service = EmbeddingService()
