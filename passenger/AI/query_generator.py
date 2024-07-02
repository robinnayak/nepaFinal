import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

nltk.download('punkt')
nltk.download('stopwords')

class QueryGenerator:
    def __init__(self):
        self.models = {
            'customuser': 'authentication_customuser',
            'driver': 'authentication_driver',
            'organization': 'authentication_organization',
            'vehicle': 'organization_vehicle',
            'trip': 'organization_trip',
            'tripprice': 'organization_tripprice',
            'booking': 'organization_booking',
            'ticket': 'organization_ticket',
            'passenger': 'passenger_passenger',
            'where':'where',
        }
        self.stop_words = set(stopwords.words('english'))

    def generate_query(self, question):
        words = word_tokenize(question.lower())
        filtered_words = [word for word in words if word.isalnum() and word not in self.stop_words]
        # Generate a simple query if just a table name is mentioned
        for word in filtered_words:
            if word in self.models:
                return f"SELECT * FROM {self.models[word]};"
        
        # Generate a query with filtering
        if "where" in words:
            return self.generate_filter_query(question, filtered_words)
        
        return "Sorry, I could not generate an SQL query for the given question."

    def generate_filter_query(self, question, filtered_words):
        table_name = ""
        condition = ""
        
        for word in filtered_words:
            if word in self.models:
                table_name = self.models[word]
                break
        
        if not table_name:
            return "Sorry, I could not find a relevant table for the given question."

        # Extract the condition from the question
        match = re.search(r'where\s+(.*)', question, re.IGNORECASE)
        if match:
            condition = match.group(1)
            condition = self.parse_condition(condition)

        if condition:
            return f"SELECT * FROM {table_name} WHERE {condition};"
        
        return f"SELECT * FROM {table_name};"

    def parse_condition(self, condition):
        # Handle common operators and patterns
        operators = ["=", ">", "<", ">=", "<=", "<>"]
        for op in operators:
            if op in condition:
                parts = condition.split(op)
                if len(parts) == 2:
                    left, right = parts[0].strip(), parts[1].strip()
                    return f"{left} {op} {right}"

        # Handle 'AND' and 'OR' conditions
        condition = condition.replace(" and ", " AND ").replace(" or ", " OR ")

        # Handle range conditions like "between"
        match = re.search(r'(\w+)\s+between\s+(\d+)\s+and\s+(\d+)', condition, re.IGNORECASE)
        if match:
            column, val1, val2 = match.groups()
            return f"{column} BETWEEN {val1} AND {val2}"
        
        return condition
