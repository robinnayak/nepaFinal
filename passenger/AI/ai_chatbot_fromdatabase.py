from decouple import config
from sqlalchemy import create_engine
import requests
import os

# Load database URL from environment variables
db_uri = config('DATABASE_URL', default=None)

# Connect to the database using SQLAlchemy
engine = create_engine(db_uri)

class QueryGenerator:
  def __init__(self, api_key):
    self.api_key = api_key

  def generate_query(self, question):
    headers = {
      "Authorization": f"Bearer {self.api_key}",  # Replace with actual authorization format
      "Content-Type": "application/json"
    }
    payload = {
      "prompt": question,
      "max_tokens": 150  # Adjust max tokens as needed
    }
    # Replace with actual Gemini AI API endpoint URL
    url = "https://<your_gemini_ai_endpoint>/v1/generate_query"  # Placeholder for actual URL
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
      query = response.json().get("query", "")
      return query
    else:
      print("Error:", response.json())
      return None

def run_query(engine, query):
  with engine.connect() as connection:
    result = connection.execute(query)
    return result.fetchall()

# Example usage (replace with actual API key)
query_generator = QueryGenerator(api_key="<your_gemini_ai_api_key>")
question = "How many vehicles are there in the database?"
query = query_generator.generate_query(question)

if query:
  response = run_query(engine, query)
  print("Response:", response)
else:
  print("Failed to generate query.")
