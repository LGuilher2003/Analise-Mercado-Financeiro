import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates

df = pd.read_sql('SELECT * FROM preco_acoes', sqlite3.connect('mercado_financeiro.db'))
def plotar_precos(df, ticker):
    df_ticker = df[df['Ticker'] == ticker].sort_values('Date')
    df_ticker['Date'] = pd.to_datetime(df_ticker['Date'])
    plt.figure(figsize=(14, 7))
    plt.plot(df_ticker['Date'], df_ticker['Price'], label='Preço', color='blue')
    plt.plot(df_ticker['Date'], df_ticker['Price'].cummax(), label='Alta (máximo até o momento)', color='green', linestyle='--')
    plt.plot(df_ticker['Date'], df_ticker['Price'].cummin(), label='Baixa (mínimo até o momento)', color='red', linestyle='--')
    plt.title(f'Evolução dos preços da ação - {ticker}')
    plt.xlabel('Data')
    plt.ylabel('Preço (USD)')
    plt.legend()
    plt.grid()
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.show()
def compararacoes(df, tickers):
    plt.figure(figsize=(14, 7))
    for ticker in tickers:
        df_ticker = df[df['Ticker'] == ticker].copy()
        df_ticker['Date'] = pd.to_datetime(df_ticker['Date'])
        df_ticker.set_index('Date', inplace=True)
        mensal = df_ticker.resample('M').last()
        plt.plot(mensal.index, mensal['Price'], label=ticker, marker='o')
        for x, y in zip(mensal.index, mensal['Price']):
            plt.text(x, y, f'{y:.2f}', fontsize=9, color='black', va='bottom', ha='center')
    plt.title('Comparação de preços das ações')
    plt.xlabel('Data')
    plt.ylabel('Preço (USD)')
    plt.legend()
    plt.grid()
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.show()
def preco_sma20(df, ticker):
    df_ticker = df[df['Ticker'] == ticker].sort_values('Date')
    df_ticker['Date'] = pd.to_datetime(df_ticker['Date'])
    plt.figure(figsize=(14, 7))
    plt.plot(df_ticker['Date'], df_ticker['Price'], label='Preço', color='blue')
    plt.plot(df_ticker['Date'], df_ticker['SMA_20'], label='SMA 20 dias', color='orange', linestyle='--')
    plt.title(f'Preço e SMA 20 dias - {ticker}')
    plt.xlabel('Data')
    plt.ylabel('Preço (USD)')
    plt.legend()
    plt.grid()
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.show()

preco_sma20(df,'META')
