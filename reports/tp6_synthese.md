# Orchestrateur ou intégration continue ? (TP06)

| Critère | Prefect (orchestrateur) | GitHub Actions (CI) |
| --- | --- | --- |
| Ce qui déclenche l’exécution | La planification hebdomadaire ou un lancement manuel depuis le tableau de bord. | Un `push` ou un lancement manuel depuis l’onglet Actions. |
| Où s’exécute le traitement | Sur le poste qui lance `serve` ou qui héberge le worker du pool `pool-tp`. | Sur une machine Linux fournie par GitHub, avec Python 3.12. |
| Qui surveille, et où | L’équipe MLOps consulte l’état, la durée et les journaux de chaque tâche dans l’interface Prefect. | L’équipe de développement consulte les étapes, les journaux et les rapports dans l’onglet Actions. |
| Ce qui se passe en cas d’échec | Prefect retente deux fois l’exécution de DVC si cette tâche échoue. Si le F1 est sous le seuil, la validation échoue immédiatement et la notification d’acceptation est sautée. | Le script de contrôle retourne le code 1 si le F1 est sous le seuil. Le job échoue et l’étape de conservation des rapports s’exécute quand même. |
| Type de tâche adapté | Réentraînement périodique ou à la demande et suivi opérationnel des traitements. | Vérification de la reproductibilité du pipeline et du seuil de qualité à chaque changement du projet. |
| Ce qui est versionné dans Git | Le flow Python, son script de planification et la configuration du déploiement dans `prefect.yaml`. | Le workflow YAML, les dépendances de CI et le script de vérification. |

## Conclusion

1. Prefect planifie le réentraînement et rend chaque tâche observable.
2. GitHub Actions rejoue le pipeline dans un environnement propre à chaque `push`.
3. Les deux contrôles lisent le même seuil F1 dans `params.yaml`.
4. Prefect interrompt la suite du traitement si le score est insuffisant, tandis que GitHub Actions signale l’échec sur le commit.
5. La CI contrôle les changements du projet et l’orchestrateur prend en charge ses traitements récurrents.
