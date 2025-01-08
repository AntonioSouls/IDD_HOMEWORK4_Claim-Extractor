from task1 import TableConverter, ClaimExtractor
import time

# Funzione principale che orchestra l'intera esecuzione del programma
def main():
    start_time = time.time()
    TableConverter.table_extractor("data/extraction","data/conversions", "data/images")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Conversion Completed in {execution_time:.6f} secondi")
    ClaimExtractor.claim_extractor("data/conversions")

# Funzione starter dello script che fa partire la funzione principale
if __name__ == "__main__":
    main()