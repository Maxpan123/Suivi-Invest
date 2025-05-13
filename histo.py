import pandas as pd

st.header("Historique des transactions")

session = Session()
transactions = session.query(Transaction).all()

# Convertir les objets SQLAlchemy en DataFrame
df = pd.DataFrame([{
    "Date": t.date,
    "ISIN": t.isin,
    "Libellé": t.libelle,
    "Type": t.type,
    "Quantité": t.quantite,
    "Prix unitaire": t.prix_unitaire,
    "Frais": t.frais,
    "Devise": t.devise
} for t in transactions])

# Affichage même si le DataFrame est vide
st.dataframe(df)