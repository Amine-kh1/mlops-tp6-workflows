import os
import subprocess
import sys
from pathlib import Path

from prefect import flow, get_run_logger, task

from verifier_qualite import lire_metriques as charger_metriques
from verifier_qualite import lire_seuil_f1, modele_accepte


RACINE_PROJET = Path(__file__).resolve().parent


@task(retries=2, retry_delay_seconds=10)
def rejouer_pipeline():
    # Les étapes DVC appellent elles-mêmes python. Elles utilisent ainsi le même environnement.
    env = os.environ.copy()
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    resultat = subprocess.run(
        [sys.executable, "-m", "dvc", "repro"],
        cwd=RACINE_PROJET,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    logger = get_run_logger()
    if resultat.stdout:
        logger.info("%s", resultat.stdout.rstrip())
    if resultat.returncode:
        detail = resultat.stderr.strip() or resultat.stdout.strip()
        raise RuntimeError(f"dvc repro a échoué (code {resultat.returncode}) : {detail}")


@task
def lire_metriques():
    return charger_metriques()


@task(retries=0)
def valider(metriques):
    f1 = metriques["f1"]
    seuil = lire_seuil_f1()
    if not modele_accepte(f1, seuil):
        raise ValueError(f"F1 {f1} < seuil {seuil} : modèle refusé")
    get_run_logger().info("F1 %s >= seuil %s : modèle accepté", f1, seuil)


@task
def notifier(metriques):
    get_run_logger().info("NOTIFICATION équipe : nouveau modèle validé, F1 = %s", metriques["f1"])


@flow(name="reentrainement-fraude", log_prints=True)
def reentrainement():
    rejouer_pipeline()
    metriques = lire_metriques()
    valider(metriques)
    notifier(metriques)


if __name__ == "__main__":
    reentrainement()
