import ccxt
import pandas as pd

# Configuration de l'échange
exchange = ccxt.binance()

# Liste des paires à évaluer
pairs = [
	"ADA/EUR", "APT/EUR", "ARB/EUR", "ATOM/EUR", "AVAX/EUR", "BCH/EUR", "BNB/EUR", "BTC/EUR", "DOGE/EUR", "DOT/EUR", "EGLD/EUR", "ETH/EUR", "FTM/EUR", "GALA/EUR", "GMT/EUR", "GRT/EUR", "ICP/EUR", "LINK/EUR", "LTC/EUR", "NEAR/EUR", "NOT/EUR", "OP/EUR", "PEPE/EUR", "POL/EUR", "RENDER/EUR", "SHIB/EUR", "SOL/EUR", "SUI/EUR", "TRX/EUR", "VET/EUR", "WIF/EUR", "WIN/EUR", "XLM/EUR", "XRP/EUR"
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
pd.options.display.float_format = '${:,.3f}'.format
results_df = pd.DataFrame(results)
print(results_df)

