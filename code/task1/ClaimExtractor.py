from openai import OpenAI
from tqdm import tqdm
import os
import json
import re
import time


""" ..................... Parte che definisce l'interazione con il modello ..................................................................."""

# Definisce la posizione in cui è memorizzato il comando da dare al modello
prompt = "".join(open("data/messageForModel.txt","r").readlines())


# Definisce l'API da contattare, quindi il modello con cui si comunica
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)


# Funzione che invia messaggi all'LLM e riceve le risposte
def ask_chatbot(table_content, max_retries, wait_time):
    for attempt in range(max_retries):
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
        )
        
        # Verifica se la risposta è valida
        if completion.choices and completion.choices[0]:
            return completion.choices[0].message.content
            
        
        # Attendi prima di ritentare
        time.sleep(wait_time)
    
    # Se fallisce dopo tutti i tentativi, ritorna un valore predefinito o lancia un'eccezione
    print("Errore: Non è stata ottenuta una risposta valida dopo diversi tentativi.")
    return None

# Funzione che re-interroga LLM nel caso in cui questo restituisca messaggi incompleti e gli chiede di completare la risposta
# lasciata incompleta
def ask_chatbot_recovery(continuation_prompt, max_retries, wait_time):
    for attempt in range(max_retries):
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-thinking-exp:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{prompt}\n{continuation_prompt}"
                        }
                    ]
                }
            ],
        )
        
        # Verifica se la risposta è valida
        if completion.choices and completion.choices[0]:
            return completion.choices[0].message.content
            
        
        # Attendi prima di ritentare
        time.sleep(wait_time)
    
    # Se fallisce dopo tutti i tentativi, ritorna un valore predefinito o lancia un'eccezione
    print("Errore: Non è stata ottenuta una risposta valida dopo diversi tentativi.")
    return None

""" .......................... Parte che specifica il comportamento per estrarre i Claim ed interrogare il modello ..........................."""

# Funzione che controlla se una risposta JSON è completa.
def is_response_complete(response):
    try:
        # Utilizza una regex per estrarre il JSON dalla risposta
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            return False
        
        # Prova a fare il parsing del JSON
        json.loads(json_match.group(0))
        return True
    except json.JSONDecodeError as e:
        return False


# Funzione che recupera una risposta incompleta chiedendo al modello di continuare
def recover_incomplete_response(incomplete_response, table_content):
    
    continuation_prompt = f"Continua la risposta incompleta:\n{incomplete_response}\nDalla tabella:\n{table_content}"
    continuation = ask_chatbot_recovery(continuation_prompt, 10, 10)
    if continuation:
        return incomplete_response + continuation
    return "{\u007b\u007d}"


# Funzione che riformatta e pulisce la risposta del modello
def format_claims(raw_response):
    return


# Funzione principale che per ogni tabella chiede al modello di estrarne i claims
def claim_extractor(cartella_sorgente):
    """ Estraggo uno ad uno i file dalla directory sorgente e memorizzo le informazioni presenti nel file"""
    for JSON_File in tqdm(os.listdir(cartella_sorgente), desc="Extracting claims from tables"):
        input_JSON_File_path = os.path.join(cartella_sorgente, JSON_File)
        with open(input_JSON_File_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        """ In primis verifico di non aver già creato il file destinazione, in modo da non dover interrogare il modello più volte sugli
        stessi dati. Dopodiché, per tutti i dati nuovi, interrogo il modello e salvo la risposta in un apposito file testuale"""    
        JSON_File_sanitized = JSON_File.replace(".json",".txt")
        txt_path = os.path.join("data/claims/txt",JSON_File_sanitized)
        if not os.path.exists(txt_path):
            raw_response = ask_chatbot(data, 10, 10)
            if raw_response:
                if not is_response_complete(raw_response):
                    raw_response = recover_incomplete_response(raw_response, data)
            
                with open(f"data/claims/txt/{JSON_File_sanitized}", 'w', encoding='utf-8') as output_file:
                    output_file.write(raw_response)
            time.sleep(10)
        
    for txt_file in os.listdir("data/claims/txt"):
        txt_file_path = os.path.join("data/claims/txt", txt_file)
        with open(txt_file_path, 'r', encoding="utf-8") as file:
            content = file.read()
        file_claims = format_claims(content)

        Json_file_sanitized = txt_file.replace(".txt", "_claims.json")
        with open(f"data/claims/json/{Json_file_sanitized}", 'w', encoding='utf-8') as file:
            json.dump(file_claims, file, indent=4)
    return