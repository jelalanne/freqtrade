import requests

# Endpoint de l'API Binance pour obtenir les informations d'échange
url = "https://api.binance.com/api/v3/exchangeInfo"

# Récupération des données de l'API
response = requests.get(url)
data = response.json()

print(data)
# Filtrer les paires se terminant par 'EUR'
eur_pairs = [symbol['symbol'] for symbol in data['symbols'] if symbol['quoteAsset'] == 'EUR' and symbol['status'] == 'TRADING']

print(eur_pairs)
# Formater les paires sous la forme 'BASE/EUR'
formatted_pairs = [f"{pair[:-3]}/EUR" for pair in eur_pairs]

# Trier les paires par ordre alphabétique
sorted_pairs = sorted(formatted_pairs)

# Affichage des paires disponibles
print('[' + ', '.join(f'"{pair}"' for pair in sorted_pairs) + ']')
