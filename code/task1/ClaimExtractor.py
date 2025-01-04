from openai import OpenAI
import os
import json
import re
import time

prompt = "".join(open("data/messageForModel.txt","r").readlines())

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)



def ask_chatbot (table_content):
    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-thinking-exp:free",
        messages=[
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": f"{prompt}\n{table_content}"
            }
            ]
        }
        ],
        max_tokens=30000
    )
    
    return completion.choices[0].message.content


def format_claims(raw_response):
    try:
        # Utilizza una regex per trovare il JSON nella raw_response
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON structure found in the raw response.")
        
        # Estrai il JSON e caricalo come dizionario
        claims_data = json.loads(json_match.group(0))
        
        # Verifica che il risultato sia strutturato come un dizionario
        if not isinstance(claims_data, dict):
            raise ValueError("Extracted data is not a dictionary.")
        
        return claims_data
    except Exception as e:
        print(f"Error processing claims: {e}")
        return {}
       

def claim_extractor(cartella_sorgente, cartella_destinazione):
    for JSON_File in os.listdir(cartella_sorgente):
        JSON_File_path = os.path.join(cartella_sorgente, JSON_File)
        with open(JSON_File_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        raw_response = ask_chatbot(data)
        JSON_File_sanitized = JSON_File.replace(".json",".txt")
        with open(f"data/claims/{JSON_File_sanitized}", 'w', encoding='utf-8') as output_file:
                output_file.write(raw_response)
        time.sleep(120)
        
        

        # file_claims = format_claims(raw_response)

        # Json_file_sanitized = JSON_File.replace(".json", "_claims.json")
        # claims_file_path = os.path.join(cartella_destinazione, Json_file_sanitized)
        # with open(claims_file_path, 'w', encoding='utf-8') as file:
        #     json.dump(file_claims, file, indent=4)
        # break
    return