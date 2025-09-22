import yfinance as yf
import numpy as np
import sqlite3
from db import criar_banco

def coletar_dados():
    tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "BRK-B", "NVDA", "JPM", "V"]
    data = yf.download(tickers, period="1y", interval="1d")
    data = data['Close']
    data = data.round(2)
    data = data.reset_index().melt(id_vars="Date", var_name="Ticker", value_name="Price")
    def rsi(series, period=14):
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    data['SMA_20'] = data.groupby("Ticker")['Price'].transform(lambda x: x.rolling(20).mean())
    data['RSI_14'] = data.groupby("Ticker")['Price'].transform(rsi)
    data['Signal'] = np.where(data['RSI_14'] < 30, "COMPRA",
                      np.where(data['RSI_14'] > 70, "VENDA", "NEUTRO"))
    data['Price'] = data['Price'].round(2)
    data['SMA_20'] = data['SMA_20'].round(2)
    data['RSI_14'] = data['RSI_14'].round(2)
    return data
def salvar_no_banco(data):
    conn = sqlite3.connect('mercado_financeiro.db')
    data.to_sql('preco_acoes', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    print("Dados salvos no banco com sucesso!")

if __name__ == "__main__":
    criar_banco()
    dados_processados = coletar_dados()
    salvar_no_banco(dados_processados)
    print("\n Banco atualizado com sucesso!")