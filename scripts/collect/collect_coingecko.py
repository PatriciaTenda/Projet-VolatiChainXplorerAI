from pycoingecko import CoinGeckoAPI
import pandas as pd


cg = CoinGeckoAPI()

data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days='365', interval='daily')

df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
df = df[['date', 'price']].sort_values('date')

df.to_csv("data/raw/btc_prices_coingecko.csv", index=False)
print("Données enregistrées avec pycoingecko")