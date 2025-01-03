import os
import json

# Funzione per rimuovere caratteri superflui dall'id di una tabella ricevuta in ingrsso
def sanitize_tableId(tableId):
    return tableId.replace("id_table_", "")

# Funzione per rimuovere caratteri superflui dal nome del file JSON ricevuto in ingresso
def sanitize_filename(filename):
    return filename[len("arXiv_"):-len(".json")]


#########################################################################################################################################
def claim_extractor(table_content):
    return

def main():
    cartella_sorgente = "extraction"
    cartella_destinazione = "claims"

    for JSON_File in os.listdir(cartella_sorgente):
        JSON_File_sanitized = sanitize_filename(JSON_File)
        print(f"Processing: {JSON_File_sanitized}")

        JSON_file_path = os.path.join(cartella_sorgente, JSON_File)
        with open(JSON_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for table_id, table_content in data.items():
            #extracted_claims = claim_extractor(table_content)
            table_id_sanitized = sanitize_tableId(table_id)
            output_file_path = os.path.join(cartella_destinazione, f"{JSON_File_sanitized}_{table_id_sanitized}_claims.json")
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(table_content, output_file, indent=4, ensure_ascii=False)
            print(f"Table {table_id} saved to {output_file_path}")
        print(f"\n\n")
                
        


# Funzione starter dello script
if __name__ == "__main__":
    main()