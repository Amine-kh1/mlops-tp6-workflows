import os
import json
import joblib
import pandas as pd

import matplotlib
matplotlib.use("Agg")  # Pas de fenêtre graphique

import matplotlib.pyplot as plt

from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    ConfusionMatrixDisplay
)


# ============================================================
# 1. Chargement des données de test
# ============================================================

test = pd.read_csv(
    "data/prepare/test.csv"
)


# ============================================================
# 2. Séparation des variables
# ============================================================

X = test.drop(
    columns="fraude"
)

y = test["fraude"]


# ============================================================
# 3. Chargement du modèle
# ============================================================

modele = joblib.load(
    "models/model.pkl"
)


# ============================================================
# 4. Prédictions
# ============================================================

pred = modele.predict(
    X
)


# ============================================================
# 5. Calcul des métriques
# ============================================================

mets = {
    "f1": round(
        f1_score(y, pred),
        4
    ),
    "precision": round(
        precision_score(y, pred),
        4
    ),
    "recall": round(
        recall_score(y, pred),
        4
    )
}


# ============================================================
# 6. Création du dossier de rapports
# ============================================================

os.makedirs(
    "reports",
    exist_ok=True
)


# ============================================================
# 7. Sauvegarde des métriques
# ============================================================

with open(
    "reports/metrics.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        mets,
        file,
        indent=2
    )


# ============================================================
# 8. Génération de la matrice de confusion
# ============================================================

ConfusionMatrixDisplay.from_predictions(
    y,
    pred
)

plt.savefig(
    "reports/confusion.png",
    dpi=110,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 9. Affichage des résultats
# ============================================================

print(
    "Évaluation :",
    mets
)