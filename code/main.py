from task1 import TableExtractor
from task1 import ClaimExtractor
from task2 import Profiling
import time

# Funzione principale che orchestra l'intera esecuzione del programma
def main():
    start_time = time.time()
    TableExtractor.extract_tables("data/papers","data/tables", "data/tables_images")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Conversion Completed in {execution_time:.6f} secondi")
    ClaimExtractor.claim_extractor("data/tables")
    Profiling.create_profiling_spreadsheet()
    

# Funzione starter dello script che fa partire la funzione principale
if __name__ == "__main__":
    main()