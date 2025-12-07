import redis
from rq import Worker, Queue, Connection
from app.core.config import settings

listen = ['default']

def start_worker():
    redis_url = settings.REDIS_URL
    conn = redis.from_url(redis_url)

    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()

if __name__ == '__main__':
    print(f"Starting worker listening on: {listen}")
    start_worker()
