import redis
import time

SOURCE_HOST = "172.16.22.21"
SOURCE_PORT = 16887    

REPLICA_HOST = "172.16.22.23"
REPLICA_PORT = 18204  

# Connect to Source DB:
source_db = redis.Redis(host=SOURCE_HOST, port=SOURCE_PORT, decode_responses=True)

# Inserting 100 values:
for i in range(1, 101):
    key = f"num:{i}"
    source_db.set(key, i)

print("Inserted successfully.")

# Adding delay for changes to be replicated to replica-db
WAIT_TIME = 3   # seconds
time.sleep(WAIT_TIME)

# Connect to Replica DB:
replica_db = redis.Redis(host=REPLICA_HOST, port=REPLICA_PORT, decode_responses=True)

# Reading values in reverse order:
for i in range(100, 0, -1):
    key = f"num:{i}"
    value = replica_db.get(key)
    print(value)

