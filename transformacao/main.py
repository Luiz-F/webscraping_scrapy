import pandas as pd
import datetime
import sqlite3

path = '../extracao/data1.json'
df = pd.read_json(path)

#Adicionar colunas ao DataFrame
df['Source'] = 'https://lista.mercadolivre.com.br/tenis-corrida-masculino'
df['Data Coleta'] = datetime.datetime.now()

#Converter os campos de prices para Float e preencher campos nulos com zero.
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

#Remover Parenteses no Reviews Amount
df['reviews_amount'] = df['reviews_amount'].str.replace("(","").str.replace(")","")
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Juntar as colunas de Preço com Centavos
df['old_price'] = df['old_price_reais'] + (df['old_price_centavos'] / 100)
df['new_price'] = df['new_price_reais'] + (df['new_price_centavos'] / 100)

#Remover colunas desnecessárias do DataFrame
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

# Criar e conectando no banco de dados.
conn = sqlite3.connect('../data/quotes.db')

# Inserir os dados no banco de dados.
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conn.close()
