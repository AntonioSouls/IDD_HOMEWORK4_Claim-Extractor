from bs4 import BeautifulSoup
from tqdm import tqdm
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import json

# Funzione per trasformare la lista ricevuta in ingresso in un'unica stringa
def sanitize_table(table):
    combined_string = "".join(table)
    return combined_string

# Funzione per rimuovere caratteri superflui dall'id di una tabella ricevuta in ingrsso
def sanitize_tableId(tableId):
    return tableId.replace("id_table_", "")

# Funzione per rimuovere caratteri superflui dal nome del file JSON ricevuto in ingresso
def sanitize_filename(filename):
    return filename[len("arXiv_"):-len(".json")]

# Funzione che rimuove comandi LaTeX come \textbf{}, \frac{}, ecc.
def clean_latex(text):
    text = re.sub(r'\$', '', text)
    return text


# Funzione che riceve in ingresso una tabella e la converte in un data-frame
def conversion_calculator(html_table):
    soup = BeautifulSoup(html_table, 'html.parser')

    # Trova tutti gli elementi <math> con classe "ltx_Math" e sostituisci il loro contenuto con il valore di "alttext"
    for math_element in soup.find_all("math", class_="ltx_Math"):
        alttext = math_element.get('alttext', '')  # Ottieni il valore dell'attributo alttext
        if alttext == "\\times" and math_element.string is None:
            math_element.replace_with("x")
        math_element.string = alttext  # Sostituisci il contenuto del tag con il valore di alttext
    

    # Trova la tabella
    table = soup.find("table")
    
    # Converte la tabella HTML in un DataFrame
    df: pd.DataFrame = pd.read_html(StringIO(str(table)))[0]
    
    # Pulisce il contenuto del DataFrame
    df = df.map(lambda x: clean_latex(str(x)))

    # Verifica se la prima riga può essere usata come intestazione
    first_row = df.iloc[0].apply(pd.to_numeric, errors='coerce')

    is_numeric_index = first_row.index.map(lambda x: isinstance(x, (int, float)))
    is_consecutive = False
    if is_numeric_index.all():
        is_consecutive = all(first_row.index[i] == first_row.index[i - 1] + 1 for i in range(1, len(first_row.index)))
    if is_consecutive:
        df.columns = df.iloc[0]
        df = df.drop(index=0).reset_index(drop=True)

    return df


# Funzione che trasforma il data-frame della tabella in un'immagine
# (Le immagini ci torneranno utili in fase di test)
def save_table_png(df, path):
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.axis('off')  

    df = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)


# Funzione che memorizza il data-frame in formato .json aggiungendo anche ulteriori informazioni rilevanti della tabella
def save_converted_table(df, caption, references, path):
    
    header = df.columns.tolist()

    df_as_json = [header]
    rows_as_lists = df.apply(lambda row: row.astype(str).tolist(), axis=1)

    for row_list in rows_as_lists:
        df_as_json.append(row_list)

    json_content = {
        "table": df_as_json,
        "caption": caption,
        "references": references
    }

    with open(path, "w") as file:
        json.dump(json_content, file, indent=4)


# Funzione che riceve in ingresso un elenco di file json contenenti varie tabelle ciascuno, estrae le singole tabelle una ad una e, per 
# ognuna, effettua una conversione in formato data-frame e salva il risultato di tale conversione in un apposito file json specifico per 
# quella tabella
def extract_tables(cartella_sorgente, cartella_destinazione_df, cartella_destinazione_png):
    for JSON_File in tqdm(os.listdir(cartella_sorgente), desc="Conversion of paper tables in .json format"):

        JSON_File_sanitized = sanitize_filename(JSON_File)
        JSON_file_path = os.path.join(cartella_sorgente, JSON_File)
        with open(JSON_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for table_id, table_content in data.items():
            table_id_sanitized = sanitize_tableId(table_id)
            html_table = sanitize_table(table_content.get("table"))
            if html_table:
                converted_table = conversion_calculator(html_table)
                converted_table_path = os.path.join(cartella_destinazione_df, f"{JSON_File_sanitized}_{table_id_sanitized}.json")
                table_png_path = os.path.join(cartella_destinazione_png, f"{JSON_File_sanitized}_{table_id_sanitized}.png")
                save_converted_table(converted_table, table_content.get("caption"), table_content.get("references"), converted_table_path)
                save_table_png(converted_table, table_png_path)
            
            
        
           
