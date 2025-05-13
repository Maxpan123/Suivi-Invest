from sqlalchemy import create_engine, text

# Remplace ceci par ton URL Supabase complète
DATABASE_URL = "postgresql://DB_SUIFIN_owner:npg_tFPhX8frz0vi@ep-dawn-glade-ab96c3r5-pooler.eu-west-2.aws.neon.tech/DB_SUIFIN?sslmode=require"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Connexion réussie à Supabase ! Résultat :", result.scalar())
except Exception as e:
    print("❌ Connexion échouée :", e)
