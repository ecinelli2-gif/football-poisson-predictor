# src/data_loader.py

import pandas as pd

def load_data_from_url(url: str) -> pd.DataFrame:
    """
    Scarica il file CSV da football-data.co.uk e restituisce un DataFrame pulito.
    
    Campi estratti:
    - Date: Data della partita
    - HomeTeam: Squadra giocante in casa
    - AwayTeam: Squadra giocante in trasferta
    - FTHG: Full Time Home Team Goals (Gol segnati in casa)
    - FTAG: Full Time Away Team Goals (Gol segnati in trasferta)
    """
    try:
        # Carica il dataset direttamente dal web, legge il file CSV e lo trasforma in un data frame, cioè in una tabella con tutti i dati, che all'inizio sarà vasta
        df = pd.read_csv(url)
        
        # Seleziona solo le colonne essenziali per il modello matematico
        columns_needed = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']
        
        # Verifica che tutte le colonne richieste siano presenti nel file CSV
        missing = [col for col in columns_needed if col not in df.columns]
        if missing:
            raise KeyError(f"Colonne mancanti nel dataset: {missing}")
            
        # Tiene solo le colonne interessanti    
        df = df[columns_needed].copy()
        
        # Rinomina le colonne per renderle più leggibili
        df.rename(columns={
            'HomeTeam': 'Home',
            'AwayTeam': 'Away',
            'FTHG': 'HomeGoals',
            'FTAG': 'AwayGoals'
        }, inplace=True)
        
        # Rimuove righe con valori mancanti (ad esempio partite rinviate o non ancora giocate)
        df.dropna(inplace=True)
        
        # Converte i gol in numeri interi, prima erano float
        df['HomeGoals'] = df['HomeGoals'].astype(int)
        df['AwayGoals'] = df['AwayGoals'].astype(int)
        
        return df

    except Exception as e:
        print(f"Errore durante il caricamento dei dati: {e}")
        return pd.DataFrame()
# Se qualcosa va storto la funzione stampa l'errore e restituisce un DataFrame vuoto invece di far crollare il programma 

def get_league_teams(df: pd.DataFrame) -> list:
    """Restituisce la lista ordinata e univoca delle squadre presenti nel dataset, guardando quelle che hanno giocato in casa e quelle che hanno giocato fuori casa."""
    if df.empty:
        return []
    teams = sorted(list(set(df['Home'].unique()).union(set(df['Away'].unique()))))
    return teams


if __name__ == "__main__":
    # URL di esempio: Serie A stagione recente (2025/2026 o 2024/2025) da football-data.co.uk
    SERIE_A_URL = "https://www.football-data.co.uk/mmz4281/2425/I1.csv"
    
    print("Download e pulizia dati in corso...")
    dataset = load_data_from_url(SERIE_A_URL)
    
    if not dataset.empty:
        print(f"\n✅ Dati caricati con successo! Numero di partite elaborate: {len(dataset)}")
        print("\nPrimi 5 incontri registrati:")
        print(dataset.head())
        
        squadre = get_league_teams(dataset)
        print(f"\n📊 Trovate {len(squadre)} squadre nel campionato:")
        print(squadre)