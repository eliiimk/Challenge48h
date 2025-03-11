import json
import pandas as pd
from mistralai import Mistral
import time
from tqdm import tqdm

# 🔹 Clé API et modèle
api_key = "L4eMZHtfQHjV9BTwjlfiDwrzHjrT5LhG"
model = "mistral-large-latest"
client = Mistral(api_key=api_key)


# 🔹 Fonction pour analyser un tweet
def analyser_tweet(tweet_text):
    try:
        prompt = f"""
        Analyse le tweet suivant concernant ENGIE :
        "{tweet_text}"

        1️⃣ **Sentiment** (Positif, Neutre, ou Négatif)
        2️⃣ **Score d'inconfort** (0 à 100% si Négatif, sinon 0)
        3️⃣ **Catégorie** parmi :
           - Problèmes de facturation
           - Pannes et urgences
           - Service client injoignable
           - Problèmes avec l’application
           - Délai d’intervention
           - Autre
        4️⃣ **Réponse automatique** : Génère une réponse adaptée au contexte.

        **Réponds uniquement avec un JSON au format strictement valide :**
        {{
            "sentiment": "Positif/Neutre/Négatif",
            "score_inconfort": 0-100,
            "categorie": "...",
            "reponse": "..."
        }}
        """
        stream_response = client.chat.stream(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        response = ""
        for chunk in stream_response:
            response += chunk.data.choices[0].delta.content

        response = response.strip().replace("```json", "").replace("```", "").strip()

        try:
            response_json = json.loads(response)
            return response_json
        except json.JSONDecodeError:
            return {"sentiment": "Erreur", "score_inconfort": 0, "categorie": "Erreur", "reponse": "Erreur"}

    except Exception as e:
        print(f"Erreur lors de l'analyse du tweet: {e}")
        return {"sentiment": "Erreur", "score_inconfort": 0, "categorie": "Erreur", "reponse": "Erreur"}


# 🔹 Chargement du fichier CSV
csv_path = "DataSet/Post_Treatment.csv"
df = pd.read_csv(csv_path, sep=';', quotechar='"', lineterminator='\n')
df.columns = df.columns.str.strip()


# 🔹 Application de l'analyse
def analyse_sequentielle(df):
    results = []
    for tweet_text in tqdm(df['text'], desc="Analyse des tweets"):
        result = analyser_tweet(tweet_text)
        results.append(result)
        time.sleep(2)
    return results


# 🔹 Analyse des 5 premières lignes
results = analyse_sequentielle(df)

# 🔹 Ajout des résultats au dataframe
df['sentiment'] = [res.get('sentiment', 'Erreur') for res in results]
df['score_inconfort'] = [res.get('score_inconfort', 0) for res in results]
df['categorie'] = [res.get('categorie', 'Erreur') for res in results]
df['reponse'] = [res.get('reponse', 'Erreur') for res in results]

# 🔹 Réorganisation des colonnes dans l'ordre demandé
df = df[['id', 'id_user', 'date', 'time', 'text', 'sentiment', 'score_inconfort', 'categorie', 'reponse']]

# 🔹 Sauvegarde des résultats (propre par colonne)
csv_output_path = "DataSet/Final.csv"
json_output_path = "DataSet/Final.json"

# ➡️ Sauvegarde CSV
df.to_csv(csv_output_path, index=False, sep=';', encoding='utf-8')

# ➡️ Sauvegarde JSON (formaté proprement)
df_json = df.to_dict(orient='records')
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(df_json, json_file, ensure_ascii=False, indent=4)

# 🔥 Résultat
print("\n✅ Analyse terminée ! Résultats enregistrés dans :", csv_output_path)
print("\n📊 Aperçu des résultats :")
print(df)