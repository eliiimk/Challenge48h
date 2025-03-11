import pandas as pd

# Chargement des données
file_path = 'DataSet/filtered_tweets_engie.csv'
df = pd.read_csv(file_path, sep=';', quotechar='"', lineterminator='\n')

# Renommer les colonnes
df.columns = ['id', 'id_user', 'name', 'date', 'text']

# Supprimer les colonnes inutiles
df = df.drop(columns=['name'])

# Fonction pour enlever la notation scientifique et convertir les valeurs
def remove_scientific_notation(x):
    if isinstance(x, str):
        # Remplacer la virgule par un point si nécessaire
        x = x.replace(',', '.')
        if 'E' in x:  # Si la valeur est en notation scientifique
            base, exponent = x.split('E')
            return str(int(float(base) * (10 ** int(exponent))))  # Calcule nombre entier
    return x  # Si ce n'est pas en notation scientifique, on retourne la valeur de base

# Appliquer le calcul pour la colonne 'id'
df['id'] = df['id'].apply(remove_scientific_notation)

# Convertir la colonne 'date' en datetime tout en gardant le fuseau horaire
df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)

# Garder le fuseau horaire sans l'afficher
df['date'] = df['date'].dt.tz_convert('Europe/Paris')

# Créer une nouvelle colonne 'time' qui contient uniquement l'heure extraite de 'date'
df['time'] = df['date'].dt.time

# Formater la colonne 'date' pour ne conserver que le jour, le mois et l'année
df['date'] = df['date'].dt.strftime('%d/%m/%Y')

# Réorganiser les colonnes pour que 'time' soit la 4ème colonne
df = df[['id', 'id_user', 'date', 'time', 'text']]

# Supprimer les doublons en gardant uniquement la première occurrence pour chaque combinaison (id_user, text)
df = df.drop_duplicates(subset=['id_user', 'text'], keep='first')

# Sauvegarder le fichier modifié
df.to_csv('DataSet/PostTreatment.csv', sep=';', index=False)
