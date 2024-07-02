from decouple import config
from langchain_community.utilities import SQLDatabase
import os
from passenger.AI.query_generator import QueryGenerator

class DatabaseChatbot:
    def __init__(self):
        openai_api_key = config('OPENAI_API_KEY', default=None)
        os.environ["OPENAI_API_KEY"] = openai_api_key

        db_uri = config('DATABASE_URL', default=None)
        self.db = SQLDatabase.from_uri(db_uri)

    def get_schema(self):
        return self.db.get_table_info()

    def run_query(self, query):
        response = self.db.run(query)
        return response

    def generate_and_run_query(self, question):
        generated_query = QueryGenerator().generate_query(question)
        response = self.run_query(generated_query)
        return response
