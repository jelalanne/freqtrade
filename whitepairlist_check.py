import ccxt
import pandas as pd

# Configuration de l'échange
exchange = ccxt.binance()

# Liste des paires à évaluer
pairs = [
	"ADA/EUR", "ALPINE/EUR", "APE/EUR", "APT/EUR", "ARB/EUR", "ATOM/EUR", "AVAX/EUR", "BCH/EUR", "BNB/EUR", "BTC/EUR", "BTT/EUR", "CHZ/EUR", "DAR/EUR", "DOGE/EUR", "DOT/EUR", "EDU/EUR", "EGLD/EUR", "ENA/EUR", "ENJ/EUR", "EOS/EUR", "ETC/EUR", "ETH/EUR", "FTM/EUR", "GAL/EUR", "GALA/EUR", "GMT/EUR", "GRT/EUR", "HOT/EUR", "ICP/EUR", "ID/EUR", "JASMY/EUR", "LAZIO/EUR", "LINK/EUR", "LTC/EUR", "LUNA/EUR", "MATIC/EUR", "NEAR/EUR", "OP/EUR", "PEPE/EUR", "PORTO/EUR", "RENDER/EUR", "RNDR/EUR", "RUNE/EUR", "SHIB/EUR", "SOL/EUR", "SUI/EUR", "SXP/EUR", "THETA/EUR", "TRX/EUR", "UNI/EUR", "VET/EUR", "WAVES/EUR", "WIF/EUR", "WIN/EUR", "WRX/EUR", "XLM/EUR", "XRP/EUR", "YFI/EUR", "ZIL/EUR"
]

# Période d'évaluation (par exemple, 1 jour)
timeframe = '1d'

# Nombre de périodes à récupérer
limit = 100

# Fonction pour évaluer une paire
def evaluate_pair(pair):
    # Récupération des données OHLCV
    ohlcv = exchange.fetch_ohlcv(pair, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # Calcul des indicateurs
    df['atr'] = df['high'] - df['low']  # Simplifié pour l'exemple
    df['std'] = df['close'].rolling(window=14).std()  # Écart type
    volume_avg = df['volume'].mean()
    atr_avg = df['atr'].mean()
    std_avg = df['std'].mean()
    
    return {
        'pair': pair,
        'volume_avg': volume_avg,
        'atr_avg': atr_avg,
        'std_avg': std_avg
    }

# Évaluation des paires
results = [evaluate_pair(pair) for pair in pairs]

# Affichage des résultats
results_df = pd.DataFrame(results)
print(results_df)

