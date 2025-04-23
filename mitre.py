# ----------------------------------------
# Name        : Michael Trenker
# Datum       : 23.04.2025
# Projekt     : Masterarbeit
# Beschreibung: Generierung von Beispiel-Daten für MITRE ATT&CK-Techniken und Mitigations
# Version     : 1.0
# Python-Version: 3.11.9
# Packages   : mitreattack-python(4.0.0), pandas(2.2.3)
# ----------------------------------------

import argparse
from mitreattack.stix20 import MitreAttackData
import random
import pandas as pd
import json

# ============================================
# Argumente parsen
# ============================================
parser = argparse.ArgumentParser(description="Generate MITRE ATT&CK technique-mitigation sample data.")
parser.add_argument("--samples", type=int, default=20, help="Number of total samples to generate (half true, half false).")
parser.add_argument("--seed", type=int, default=None, help="Optional random seed for reproducibility.")
parser.add_argument("--output", type=str, default=None, help="Optional output JSON file path (e.g. output.json).")
args = parser.parse_args()

NUMBER_OF_ITERATIONS = args.samples
RANDOM_SEED = args.seed
OUTPUT_PATH = args.output

# ============================================
# Initialisierung
# ============================================
if RANDOM_SEED is not None:
    random.seed(RANDOM_SEED)

# Lade MITRE ATT&CK Daten (STIX 2.0 Format)
mitre_attack_data = MitreAttackData("enterprise-attack.json")

# Mapping von Technik-ID zu Mitigationsbeziehungen
techniques_with_mitigations = mitre_attack_data.get_all_techniques_mitigated_by_all_mitigations()

# ============================================
# Wahre Kombinationen (Technik ↔ passende Mitigation)
# ============================================
data_rows_true = []

true_technique_ids = random.sample(list(techniques_with_mitigations.keys()), NUMBER_OF_ITERATIONS // 2)

for tech_id in true_technique_ids:
    data = techniques_with_mitigations[tech_id]
    technique = data[0]["object"]
    relationships = data[0]["relationships"]

    mitigation_description = None
    for relationship in relationships:
        if relationship.relationship_type == "mitigates":
            mitigation_description = relationship.description
            break

    if mitigation_description:
        data_rows_true.append({
            "Technique Name": technique.name,
            "Description": technique.description,
            "Mitigation": mitigation_description,
            "Valid": "true"
        })

# Falsche Kombinationen (Technik ↔ zufällige falsche Mitigation)
data_rows_false = []

false_technique_ids = random.sample(list(techniques_with_mitigations.keys()), NUMBER_OF_ITERATIONS // 2)

for tech_id in false_technique_ids:
    data = techniques_with_mitigations[tech_id]
    technique = data[0]["object"]

    # Set aus echten Mitigations-IDs für diese Technik sammeln
    true_mitigations = {
        rel.target_ref
        for rel in data[0]["relationships"]
        if rel.relationship_type == "mitigates"
    }

    # Mit Versuchslimit, um Endlosschleife zu vermeiden
    max_attempts = 10
    attempts = 0
    mitigation_description = None

    while attempts < max_attempts:
        random_mitigation_id = random.sample(list(techniques_with_mitigations.keys()), 1)[0]

        # Prüfen, ob Mitigation-ID *nicht* in den echten Mitigations ist
        if random_mitigation_id not in true_mitigations:
            random_mitigation = techniques_with_mitigations[random_mitigation_id]
            relationships = random_mitigation[0]["relationships"]

            for relationship in relationships:
                if relationship.relationship_type == "mitigates":
                    mitigation_description = relationship.description
                    break

            # Falls wir eine Beschreibung bekommen haben: Break aus while
            if mitigation_description:
                break

        attempts += 1

    # Falls gültige "falsche" Mitigation gefunden wurde
    if mitigation_description:
        data_rows_false.append({
            "Technique Name": technique.name,
            "Description": technique.description,
            "Mitigation": mitigation_description,
            "Valid": "false"
        })


# ============================================
# Zusammenführen und ausgeben/speichern
# ============================================
data_rows = data_rows_true + data_rows_false
random.shuffle(data_rows)  # Shuffle direkt auf der Liste

# Optional: Als JSON speichern
if OUTPUT_PATH:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data_rows, f, ensure_ascii=False, indent=2)
    print(f"✅ Daten als JSON gespeichert unter: {OUTPUT_PATH}")
else:
    # Vorschau: Zeige die ersten 3 Einträge schön formatiert
    print(json.dumps(data_rows[:3], indent=2, ensure_ascii=False))
