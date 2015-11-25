import os
import redis
from rq import Worker, Queue, Connection



listen = ['default']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    from app import create_app

    app = create_app("config.DevConfig")
    app.app_context().push()

    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
