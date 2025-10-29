from app.tools.db_tool import query_database
from app.tools.web_tool import fetch_context
from app.tools.llm import call_llm

class Agent:
    async def run(self, user_input: str):
        # Step 1: Ask LLM which sources to use
        planner_prompt = f"""
        You are an AI with access to:
        - a MySQL database (structured data)
        - cached website text (context)
        Decide: "db", "web", or "both" for this question.
        Question: {user_input}
        """

        decision = (await call_llm(planner_prompt)).lower()
        db_data = web_data = ""

        # Step 2: Use chosen tools
        if "db" in decision:
            db_data = await query_database(user_input)
        if "web" in decision:
            web_data = await fetch_context(user_input)

        # Step 3: Produce final answer
        answer_prompt = f"""
        Combine information and answer clearly.
        Question: {user_input}
        Database info: {db_data[:1500]}
        Website context: {web_data[:1500]}
        """

        return await call_llm(answer_prompt)
