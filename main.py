import os

import psycopg
from dotenv import load_dotenv
from flask import Flask

load_dotenv(".env")

app = Flask(__name__)

driver = psycopg.connect(os.getenv("DB_URI"))


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/db/<tem>")
def read_database(tem: str):
    result = driver.execute("SELECT (value) FROM public.important_data WHERE name=%s", (item,)).fetchone()
    if result:
        return f"Found result: {result[0]}"
    else:
        return "Item not found"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
