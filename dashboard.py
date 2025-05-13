# dashboard.py
import os
import streamlit as st
import pandas as pd
from datetime import date
from main import Session, Transaction, Valorisation

st.set_page_config(page_title="Dashboard PEA", layout="wide")
st.title("📊 Dashboard PEA - Bénéfices et valorisation")

# Connexion à la base
session = Session()

# Récupérer toutes les transactions
transactions = session.query(Transaction).all()
if not transactions:
    st.warning("Aucune transaction enregistrée.")
    st.stop()

# Transformer en DataFrame
df_tx = pd.DataFrame([{
    "isin": t.isin,
    "ticker": t.ticker,
    "type": t.type,
    "quantite": t.quantite,
    "prix_unitaire": t.prix_unitaire,
    "frais": t.frais,
    "date": t.date
} for t in transactions])

# Séparer achats et ventes
df_tx["quantite_signée"] = df_tx.apply(lambda row: row["quantite"] if row["type"] == "achat" else -row["quantite"], axis=1)

# Calculs par ISIN
grouped = df_tx.groupby(["isin", "ticker"]).agg(
    quantite_totale=("quantite_signée", "sum"),
    montant_total=("prix_unitaire", lambda x: (x * df_tx.loc[x.index, "quantite_signée"]).sum())
).reset_index()

grouped = grouped[grouped["quantite_totale"] > 0]
grouped["prix_moyen_achat"] = grouped["montant_total"] / grouped["quantite_totale"]

# Récupérer les valorisations du jour
today = date.today()
valorisations = session.query(Valorisation).filter_by(date=today).all()
df_valo = pd.DataFrame([{
    "isin": v.isin,
    "ticker": v.ticker,
    "cours": v.prix_unitaire
} for v in valorisations])

# Fusion et calcul des plus-values
df = pd.merge(grouped, df_valo, on=["isin", "ticker"], how="left")
df["valeur_actuelle"] = df["cours"] * df["quantite_totale"]
df["plus_value (€)"] = (df["cours"] - df["prix_moyen_achat"]) * df["quantite_totale"]
df["performance (%)"] = ((df["cours"] / df["prix_moyen_achat"]) - 1) * 100

# Affichage
st.subheader("💼 Positions actuelles")
st.dataframe(df[[
    "isin", "ticker", "quantite_totale", "prix_moyen_achat", "cours", "valeur_actuelle", "plus_value (€)", "performance (%)"
]])

session.close()
