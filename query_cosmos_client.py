import certifi
import ssl
from gremlin_python.driver import client, serializer
from config import COSMOS_DB_ENDPOINT, COSMOS_DB_DATABASE, COSMOS_DB_GRAPH, COSMOS_DB_PRIMARY_KEY

# Initialize SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Initialize Gremlin Client
gremlin_client = client.Client(
    COSMOS_DB_ENDPOINT, 
    'g',
    username=f"/dbs/{COSMOS_DB_DATABASE}/colls/{COSMOS_DB_GRAPH}",
    password=COSMOS_DB_PRIMARY_KEY,
    message_serializer=serializer.GraphSONSerializersV2d0(),
    ssl_context=ssl_context
)

async def run_gremlin_query(query):
    """
    Executes a Gremlin query against Cosmos DB and returns the results.
    """
    try:
        callback = await gremlin_client.submitAsync(query)  # Make it async
        if callback.result():
            return callback.result().all().result()
        else:
            return []
    except Exception as e:
    