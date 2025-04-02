from groq import Groq
import os

from dotenv import load_dotenv


load_dotenv()

key=os.getenv('GROQ_API_KEY')


#key="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"

def analyze_code_with_llm(file_content, file_name):
    prompt = f""" 
        Analyse the following code for:
        - Code style and formatting issues
        - Potential bugs or error
        - Performance improvemnets
        - Best practices

    File : {file_name}
    Content : {file_name}

    Provide a detailed JSON output with the structure
    {{
        "issues" : [
        {{
            "type" : <style|bugs|performance|best_practice>,
            "line" : <line_number>,
            "description" : <description>,
            "suggestion" : <suggestion>
        }}
        ]

    }}
    '''json
"""
    client = Groq(
        api_key=key
    )
    completion = client.chat.completions.create(
        model = "llama3-8b-8192",
        messages=[
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        temperature = 1,
        top_p = 1
    )
    
    return completion.choices[0].message.conten


