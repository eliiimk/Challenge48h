import os
import json
import pandas as pd
from mistralai import Mistral
import time  # Pour gérer les pauses entre les requêtes
from tqdm import tqdm  # Pour afficher la barre de progression

# 🔹 Clé API et modèle
api_key = "L4eMZHtfQHjV9BTwjlfiDwrzHjrT5LhG"  # Remplace par ta clé API
model = "mistral-large-latest"

# 🔹 Crée une instance du client Mistral
client = Mistral(api_key=api_key)

# 🔹 Fonction pour analyser un tweet avec gestion des erreurs et respect de la limite de requêtes
def analyser_tweet(tweet_text):
    try:
        # Reformulation du prompt avec JSON structuré et ajout de la réponse automatique
        prompt = f"""
        Analyse le tweet suivant concernant ENGIE :
        "{tweet_text}"

        1️⃣ **Sentiment** (Positif, Neutre, ou Négatif)
        2️⃣ **Score d'inconfort** (0 à 100% si Négatif, sinon 0)
        3️⃣ **Catégorie** parmi :
           - Problèmes de facturation : erreurs de montant, prélèvements injustifiés.
           - Pannes et urgences : absence de gaz, d’électricité, problème d’eau chaude.
           - Service client injoignable : absence de réponse, relances infructueuses.
           - Problèmes avec l’application : bugs, indisponibilité du service.
           - Délai d’intervention : retards dans la gestion des dossiers ou des réparations.
           - Autre

        4️⃣ **Réponse automatique** : Génère une réponse pour ce client en fonction de la catégorie détectée et du problème soulevé.

        **Réponds uniquement avec un JSON au format strictement valide :**
        {{
            "sentiment": "Positif/Neutre/Négatif",
            "score_inconfort": 0-100,
            "categorie": "...",
            "reponse": "..."
        }}
        """

        # Envoi de la requête en streaming
        stream_response = client.chat.stream(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        # Récupération et construction de la réponse
        response = ""
        for chunk in stream_response:
            response += chunk.data.choices[0].delta.content

        # Nettoyage du JSON généré
        response = response.strip().replace("```json", "").replace("```", "").strip()

        # Vérification et conversion en JSON
        try:
            response_json = json.loads(response)  # Parsing sécurisé
            return response_json
        except json.JSONDecodeError:
            # En cas d'erreur JSON, on retourne un résultat par défaut
            return {"sentiment": "Erreur", "score_inconfort": 0, "categorie": "Erreur", "reponse": "Erreur"}

    except Exception as e:
        # Gestion des erreurs
        print(f"Erreur lors de l'analyse du tweet: {e}")
        return {"sentiment": "Erreur", "score_inconfort": 0, "categorie": "Erreur", "reponse": "Erreur"}

# 🔹 Chargement du fichier CSV
csv_path = r"C:\Users\senth\OneDrive\Desktop\Challenge\save.csv"
df = pd.read_csv(csv_path, sep=';')

# 🔹 Fusion date et heure pour créer une colonne datetime
df['datetime'] = df['date'] + ' ' + df['time']
df.drop(columns=['date', 'time'], inplace=True)  # Suppression des colonnes inutiles

# 🔹 Application de l'analyse sur chaque tweet de manière séquentielle
def analyse_sequentielle(df):
    results = []
    for tweet_text in tqdm(df['text'], desc="Analyse des tweets"):
        result = analyser_tweet(tweet_text)
        results.append(result)
        time.sleep(2)  # Délai de 2 secondes entre chaque requête pour éviter de dépasser la limite de l'API
    return results

# Analyse des tweets de manière séquentielle
results = analyse_sequentielle(df)

# 🔹 Ajout des résultats dans le DataFrame
df['sentiment'] = [res.get('sentiment', 'Erreur') for res in results]
df['score_inconfort'] = [res.get('score_inconfort', 0) for res in results]
df['categorie'] = [res.get('categorie', 'Erreur') for res in results]
df['reponse'] = [res.get('reponse', 'Erreur') for res in results]

# 🔹 Création du format souhaité pour chaque ligne
df['formatted'] = df.apply(lambda row: f"date : {row['datetime']} , id : {row['id']} , id_user : {row['id_user']} , text : {row['text']} , sentiment : {row['sentiment']} , score_inconfort : {row['score_inconfort']} , categorie : {row['categorie']} , reponse : {row['reponse']}", axis=1)

# 🔹 Sauvegarde des résultats sous forme de texte dans un fichier CSV
csv_output_path = r"C:\Users\senth\OneDrive\Desktop\Challenge\tweets_analyzes_mistral.csv"
df[['formatted']].to_csv(csv_output_path, index=False, header=False)

# 🔹 Sauvegarde des résultats en JSON
json_output_path = r"C:\Users\senth\OneDrive\Desktop\Challenge\tweets_analyzes_mistral.json"
df_json = df.to_dict(orient='records')  # Convertit le DataFrame en liste de dictionnaires
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(df_json, json_file, ensure_ascii=False, indent=4)

print("\n✅ Analyse terminée ! Résultats enregistrés dans :", csv_output_path)
print("\n📊 Aperçu des résultats :")
print(df[['formatted']].head())  # Affiche un aperçu des résultats formatés
