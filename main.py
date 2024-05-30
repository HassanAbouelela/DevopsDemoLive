import os

import psycopg
import redis
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv(".env")

USE_CACHE = os.getenv("USE_CACHE", "true").lower() == "true"

app = Flask(__name__)


try:
    driver = psycopg.connect(os.getenv("DB_URI"))
except Exception as e:
    raise Exception("Could not connect to postgres!") from e

if USE_CACHE:
    cache = redis.Redis.from_url(os.getenv("REDIS_URI"))
    try:
        cache.ping()
    except Exception as e:
        raise Exception("Could not connect to redis!", e)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/db/<item>")
def read_database(item: str):
    result = src = None
    if USE_CACHE:
        result = cache.get(item)
        if result:
            result = result.decode("utf-8")
        src = "redis"

    if not result:
        result = driver.execute("SELECT (value) FROM public.important_data WHERE name=%s;", (item,)).fetchone()
        src = "database"

        if not result:
            return f"Item not found: {result}"

        result = result[0]
        if USE_CACHE:
            cache.set(item, result)

    return jsonify({"result": result, "src": src})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
