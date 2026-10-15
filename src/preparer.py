import os
import yaml
import pandas as pd

from sklearn.model_selection import train_test_split


# ============================================================
# 1. Chargement des paramètres
# ============================================================

with open("params.yaml", encoding="utf-8") as file:
    params = yaml.safe_load(file)

preparation_params = params["preparation"]


# ============================================================
# 2. Chargement des données
# ============================================================

df = pd.read_csv(
    "data/transactions.csv"
)


# ============================================================
# 3. Séparation des données
# ============================================================

train, test = train_test_split(
    df,
    test_size=preparation_params["test_size"],
    random_state=preparation_params["random_state"]
)


# ============================================================
# 4. Création du dossier de sortie
# ============================================================

os.makedirs(
    "data/prepare",
    exist_ok=True
)


# ============================================================
# 5. Sauvegarde des données
# ============================================================

# Sortie 1 : données d'entraînement
train.to_csv(
    "data/prepare/train.csv",
    index=False
)

# Sortie 2 : données de test
test.to_csv(
    "data/prepare/test.csv",
    index=False
)


# ============================================================
# 6. Affichage du résultat
# ============================================================

print(
    "Préparation :",
    len(train),
    "lignes train /",
    len(test),
    "lignes test"
)