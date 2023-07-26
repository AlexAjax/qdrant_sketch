import numpy as np
from qdrant_client.models import PointStruct
from qdrant_client.models import Filter, FieldCondition, Range
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


client = QdrantClient("[insertip]:6333") # Connect to existing Qdrant instance, for production
client.recreate_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=100, distance=Distance.DOT),
)

vectors = np.random.rand(100, 100)
client.upsert(
    collection_name="test_collection",
    points=[
        PointStruct(
            id=idx,
            vector=vector.tolist(),
            payload={"color": "red", "rand_number": idx % 10}
        )
        for idx, vector in enumerate(vectors)
    ]
)

query_vector = np.random.rand(100)
hits = client.search(
    collection_name="test_collection",
    query_vector=query_vector,
    limit=5  # Return 5 closest points
)
print(hits)

hits = client.search(
    collection_name="test_collection",
    query_vector=query_vector,
    query_filter=Filter(
        must=[  # These conditions are required for search results
            FieldCondition(
                key='rand_number',  # Condition based on values of `rand_number` field.
                range=Range(
                    gte=3  # Select only those results where `rand_number` >= 3
                )
            )
        ]
    ),
    limit=5  # Return 5 closest points
)

print(hits)
