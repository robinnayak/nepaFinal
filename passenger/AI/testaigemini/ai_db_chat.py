from decouple import config
from langchain_community.utilities import SQLDatabase
import os
import google.generativeai as genai
# from passenger.AI.query_generator import QueryGenerator
# from passenger.AI.ai_db_chatbot import DatabaseChatbot
class DatabaseChatbot:
    def __init__(self):
        openai_api_key = config('OPENAI_API_KEY', default=None)
        os.environ["OPENAI_API_KEY"] = openai_api_key

        google_api_key = config('GEMINI_API_KEY', default=None)
        os.environ["GOOGLE_API_KEY"] = google_api_key

        db_uri = config('DATABASE_URL', default=None)
        self.db = SQLDatabase.from_uri(db_uri)

        if google_api_key is None:
            raise ValueError("Please set the GEMINI_API_KEY environment variable")

        genai.configure(api_key=google_api_key)

    def get_schema(self):
        return self.db.get_table_info()

    def run_query(self, query):
        response = self.db.run(query)
        return response

    def generate_sql_query(self, question):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Generate an SQL query for the following question related to the database: '{question}'", stream=False)
        return response.text.strip()

    def generate_and_run_query(self, question):
        generated_query = self.generate_sql_query(question)
        response = self.run_query(generated_query)
        return response

# Usage example
if __name__ == "__main__":
    chatbot = DatabaseChatbot()
    question = "How many organization_trip are there in database?"
    response = chatbot.generate_and_run_query(question)
    print(response)
