import pandas as pd


# ============================================================
# 1. EXTRACT - LER OS DADOS
# ============================================================

# Lê o arquivo CSV
df = pd.read_csv("vendas.csv")

print("Dados originais:")
print(df.head())


# ============================================================
# 2. DIAGNÓSTICO
# ============================================================

# Mostra os tipos das colunas
print("\nTipos dos dados:")
print(df.dtypes)

# Mostra os valores vazios
print("\nValores vazios:")
print(df.isnull().sum())

# Mostra a quantidade de duplicatas
print("\nDuplicatas:", df.duplicated().sum())


# ============================================================
# 3. LIMPAR TEXTOS
# ============================================================

# Remove espaços desnecessários
df["produto"] = df["produto"].str.strip()
df["categoria"] = df["categoria"].str.strip()
df["regiao"] = df["regiao"].str.strip()
df["vendedor"] = df["vendedor"].str.strip()


# Corrige nomes escritos de formas diferentes
df["categoria"] = df["categoria"].replace(
    "informatica",
    "Informática"
)

df["regiao"] = df["regiao"].replace(
    "nordeste",
    "Nordeste"
)


# ============================================================
# 4. CORRIGIR TIPOS
# ============================================================

# Converte texto para data
df["data"] = pd.to_datetime(
    df["data"],
    dayfirst=True
)

# Garante que quantidade seja número
df["quantidade"] = pd.to_numeric(
    df["quantidade"],
    errors="coerce"
)

# Garante que valor seja número
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")


# ============================================================
# 5. REMOVER DUPLICATAS
# ============================================================

df = df.drop_duplicates()


# ============================================================
# 6. CALCULAR PREÇO UNITÁRIO
# ============================================================

# Divide o valor total pela quantidade
df["preco_unitario"] = (df["valor"] / df["quantidade"])


# ============================================================
# 7. PREENCHER VALORES VAZIOS
# ============================================================

# Calcula o preço médio de cada produto
preco_medio = df.groupby("produto")["preco_unitario"].median()


# Preenche os valores que estão vazios
for produto in df["produto"].unique():

    preco = preco_medio[produto]

    # Procura vendas desse produto que estão
    # sem valor, mas possuem quantidade
    filtro = ((df["produto"] == produto) &  (df["valor"].isna()))

    # Calcula:
    # quantidade × preço médio
    df.loc[filtro, "valor"] = (df.loc[filtro, "quantidade"] * preco  )


# ============================================================
# 8. PREENCHER QUANTIDADES VAZIAS
# ============================================================

for produto in df["produto"].unique():

    preco = preco_medio[produto]

    # Procura vendas desse produto que estão
    # sem quantidade, mas possuem valor
    filtro = (
        (df["produto"] == produto) &
        (df["quantidade"].isna())
    )

    # Calcula:
    # valor ÷ preço médio
    df.loc[filtro, "quantidade"] = (
        df.loc[filtro, "valor"] / preco
    ).round()


# ============================================================
# 9. ATUALIZAR PREÇO UNITÁRIO
# ============================================================

df["preco_unitario"] = (
    df["valor"] / df["quantidade"]
)


# ============================================================
# 10. ARREDONDAR VALORES
# ============================================================

df["valor"] = df["valor"].round(2)

df["preco_unitario"] = (
    df["preco_unitario"].round(2)
)

df["quantidade"] = (
    df["quantidade"].astype("Int64")
)


# ============================================================
# 11. LOAD - SALVAR OS DADOS
# ============================================================

df.to_csv(
    "vendas_tratadas.csv",
    index=False
)


# ============================================================
# 12. VERIFICAÇÃO FINAL
# ============================================================

print("\nETL concluído!")

print("\nValores vazios depois do tratamento:")
print(df.isnull().sum())

print("\nDados tratados:")
print(df.head())
