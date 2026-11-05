import json
from pathlib import Path

import yaml


RACINE = Path(__file__).resolve().parent


def lire_metriques():
    with (RACINE / 'reports' / 'metrics.json').open(encoding='utf-8') as fichier:
        return json.load(fichier)


def lire_seuil_f1():
    with (RACINE / 'params.yaml').open(encoding='utf-8') as fichier:
        return yaml.safe_load(fichier)['validation']['seuil_f1']


def modele_accepte(f1, seuil):
    return f1 >= seuil


def main():
    f1 = lire_metriques()['f1']
    seuil = lire_seuil_f1()
    print(f'F1 = {f1} | seuil = {seuil}')

    if not modele_accepte(f1, seuil):
        print('ECHEC : modele refuse')
        return 1

    print('OK : modele accepte')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
