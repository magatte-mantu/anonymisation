def load_mapping(mapping_file):
    """
    Charge le mapping inversé : {nouveau_nom: ancien_nom}
    """
    reverse_map = {}
    with open(mapping_file, "r", encoding="utf-8") as f:
        for line in f:
            if ">" in line:
                original, anonymized = map(str.strip, line.strip().split(">"))
                reverse_map[anonymized] = original
    return reverse_map


def desanonymize_sql(anonymized_file, mapping_file, output_file="restored.sql"):
    # Charger les mappings inversés
    reverse_map = load_mapping(mapping_file)

    # Trier par longueur descendante pour éviter les conflits ("col1" avant "col10")
    sorted_items = sorted(reverse_map.items(), key=lambda x: -len(x[0]))

    # Lire le SQL anonymisé
    with open(anonymized_file, "r", encoding="utf-8") as f:
        sql = f.read()

    # Remplacer chaque nom anonymisé par le nom d'origine
    for anon, original in sorted_items:
        # Remplacement exact (entre crochets, guillemets ou non)
        sql = sql.replace(f"[{anon}]", f"[{original}]")
        sql = sql.replace(f"'{anon}'", f"'{original}'")
        sql = sql.replace(f"{anon}", f"{original}")

    # Écrire le fichier désanonymisé
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sql)

    print(f"[✓] Script désanonymisé généré dans {output_file}")


# Utilisation
if __name__ == "__main__":
    desanonymize_sql("output.sql", "mapping.txt")
