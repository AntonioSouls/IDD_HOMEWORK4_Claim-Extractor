from task1 import TableConverter, ClaimExtractor
import time

# Funzione principale che orchestra l'intera esecuzione del programma
def main():
    #TableConverter.table_extractor("data/extraction","data/conversions", "data/images")
    ClaimExtractor.claim_extractor("data/conversions")

# Funzione starter dello script che fa partire la funzione principale
if __name__ == "__main__":
    main()