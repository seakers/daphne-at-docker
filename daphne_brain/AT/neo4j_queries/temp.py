from neo4j import GraphDatabase

uri = "bolt://13.58.54.49:7687"
user = "neo4j"
password = "goSEAKers!"

print(f"Connecting to {uri} with user {user}")

driver = GraphDatabase.driver(
    uri, 
    auth=(user, password),
    encrypted=False,  # Try without encryption
    connection_timeout=60,  # Increased connection timeout to 60 seconds
    max_transaction_retry_time=30,
    max_connection_lifetime=3600  # Keep connections alive for longer
)

try:
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        print(result.single())
except Exception as e:
    print(f"Error: {type(e).__name__}")
    print(f"Error details: {e}")
finally:
    driver.close()