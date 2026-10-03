# Lê o arquivo CSV
import pandas as pd


df = pd.read_csv("vendas_tratadas.csv")


print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
print(df.head())