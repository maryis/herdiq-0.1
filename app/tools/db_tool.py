import os, aiomysql
from app.tools.llm import call_llm

DB_HOST = os.getenv("DB_HOST")  # e.g. /cloudsql/your-connection-name
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

async def query_database(question: str):
    """Ask LLM to form safe SQL, then execute."""
    sql_prompt = f"""
    You are an expert SQL assistant.
    Write a concise MySQL query (read-only, SELECT only) that can help answer:
    "{question}"
    Respond with only the SQL query.
    """
    sql = (await call_llm(sql_prompt)).split(";")[0] + ";"

    try:
        conn = await aiomysql.connect(
            unix_socket=DB_HOST if DB_HOST.startswith("/") else None,
            host=None if DB_HOST.startswith("/") else DB_HOST,
            user=DB_USER, password=DB_PASS, db=DB_NAME)
        async with conn.cursor() as cur:
            await cur.execute(sql)
            result = await cur.fetchall()
        conn.close()
        return str(result)
    except Exception as e:
        return f"[DB error] {e}"
