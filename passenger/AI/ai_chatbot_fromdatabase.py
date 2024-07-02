from decouple import config
from sqlalchemy import create_engine
from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains  import sql_database
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from langchain_openai import ChatOpenAI
from query_generator import QueryGenerator


openai_api_key = config('OPENAI_API_KEY', default=None)
os.environ["OPENAI_API_KEY"] = openai_api_key

template = """
    Based on the table schema, the following SQL query can be used to retrieve the requested information:
    {schema}
    
    Question:{question}
    SQL Query: 
    
"""

prompt = ChatPromptTemplate.from_template(template)

pro =prompt.format(schema="my schema", question="How many vehicles are there in the database?")
db_uri = config('DATABASE_URL', default=None)
db = SQLDatabase.from_uri(db_uri)

data = db.run("select * from organization_vehicle")

def get_schema(_):
    return db.get_table_info()


template = """
    Based on the table schema, the following SQL query can be used to retrieve the requested information:
    {schema}
    
    Question:{question}
    SQL Query: {query}
    SQL Response : {response}
    """

prompt = ChatPromptTemplate.from_template(template)

def run_query(query):
    response = db.run(query)
    return response

# query = "select * from organization_vehicle"
query = QueryGenerator().generate_query("How many vehicle are there in the database?")

response = run_query(query)
print("Response: ", response)   