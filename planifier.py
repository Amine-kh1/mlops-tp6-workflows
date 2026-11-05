from flow_mlops import reentrainement


if __name__ == "__main__":
    # Laisser ce processus ouvert pour exécuter les runs chaque lundi à 06 h UTC.
    reentrainement.serve(name="hebdomadaire", cron="0 6 * * 1")
