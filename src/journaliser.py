
import json
import subprocess
import yaml
import pandas as pd
import mlflow

# Configuration de MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("tp3-dvc")

# Chargement des paramètres
with open("params.yaml", encoding="utf-8") as f:
    P = yaml.safe_load(f)

# Récupération de l'identifiant MD5 des données
with open("data/transactions.csv.dvc", encoding="utf-8") as f:
    ticket = yaml.safe_load(f)["outs"][0]

# Chargement des métriques
with open("reports/metrics.json", encoding="utf-8") as f:
    mets = json.load(f)

# Récupération du commit Git
commit = subprocess.getoutput("git rev-parse --short HEAD")

# Calcul du nombre de lignes du dataset
n = len(pd.read_csv("data/transactions.csv"))

# Création du run MLflow
with mlflow.start_run(
    run_name=f"donnees-{ticket['md5'][:8]}"
):
    # Enregistrement des paramètres
    mlflow.log_params(P["entrainement"])

    # Enregistrement des métriques
    mlflow.log_metrics(mets)

    # Enregistrement des tags
    mlflow.set_tags({
        "commit": commit,              # Quel code ?
        "donnees_md5": ticket["md5"],  # Quelles données ?
        "donnees_lignes": n            # Combien de lignes ?
    })

    # Enregistrement du fichier DVC
    mlflow.log_artifact("dvc.lock")

# Affichage du résultat
print(
    "Run MLflow créé : données",
    ticket["md5"][:8],
    "-",
    n,
    "lignes"
)
