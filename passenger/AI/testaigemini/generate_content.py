import pathlib 
import textwrap3 
import os
import google.generativeai as genai 
from IPython.display import display, Markdown
from decouple import config


def to_markdown(text):
    text = text.replace('.',' *')
    return Markdown(textwrap3.indent(text, '>',predicate=lambda _:True))


GOOGLE_API_KEY = config('GEMINI_API_KEY',default=None)
print(GOOGLE_API_KEY)

if GOOGLE_API_KEY is None:
    raise ValueError('API key is not set. Please set the API key before continuing.')   

# Create a new instance of the Gemini API client
genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
        print(m.description)

        
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("what is the meaning of life? ")
print(response.text)

#print safety ratings

if hasattr(response, 'safety_ratings'):
    print("Safety ratings:")
    for rating in response.safety_ratings:
        print(f"{rating.category}: {rating.probability}")
else:
    print("No safety ratings available in the response.")

response = model.generate_content("What is the meaning of life",stream=True)

for chunk in response:
    print(chunk.text)
    print("_"*80)
