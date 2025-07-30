import re

def anonymize_sql_procedure(input_file, output_file="output.sql", mapping_file="mapping.txt"):
    with open(input_file, "r", encoding="utf-8") as f:
        sql = f.read()

    table_map = {}
    column_map = {}
    alias_map = {}
    proc_map = {}
    variable_map = {}

    table_idx = column_idx = alias_idx = proc_idx = var_idx = 1

    # 1. Anonymiser la procédure stockée
    def replace_procedure(match):
        nonlocal proc_idx
        schema = match.group(1)
        proc = match.group(2)
        if schema not in proc_map:
            proc_map[schema] = f"schema{proc_idx}"
        if proc not in proc_map:
            proc_map[proc] = f"proc{proc_idx}"
        proc_idx += 1
        return f"CREATE PROCEDURE [{proc_map[schema]}].[{proc_map[proc]}]"

    sql = re.sub(r'\bCREATE\s+PROCEDURE\s+\[?(\w+)\]?\.\[?(\w+)\]?', replace_procedure, sql, flags=re.IGNORECASE)

    # 2. Anonymiser les variables (@XXX)
    def replace_variable(match):
        nonlocal var_idx
        var = match.group(0)
        if var not in variable_map:
            variable_map[var] = f"@var{var_idx}"
            var_idx += 1
        return variable_map[var]

    sql = re.sub(r'@\w+', replace_variable, sql)

    # 3. Identifier et anonymiser les alias (FROM/JOIN)
    def alias_mapper(match):
        nonlocal alias_idx
        alias = match.group(2)
        table = match.group(1).strip('[]')
        if alias not in alias_map:
            alias_map[alias] = f"alias{alias_idx}"
            alias_idx += 1
        if table not in table_map:
            table_map[table] = f"table{len(table_map)+1}"
        keyword = 'FROM' if 'FROM' in match.group(0).upper() else 'JOIN'
        return f"{keyword} {table_map[table]} {alias_map[alias]}"

    sql = re.sub(r'\bFROM\s+([\[\]\w\.]+)\s+(\w+)', alias_mapper, sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bJOIN\s+([\[\]\w\.]+)\s+(\w+)', alias_mapper, sql, flags=re.IGNORECASE)

    # 4. Remplacer alias.col par aliasX.colY
    def replace_alias_column(match):
        nonlocal column_idx
        alias = match.group(1)
        col = match.group(2)
        new_alias = alias_map.get(alias, alias)
        if col not in column_map:
            column_map[col] = f"col{column_idx}"
            column_idx += 1
        return f"{new_alias}.{column_map[col]}"

    sql = re.sub(r'\b(\w+)\.(\w+)', replace_alias_column, sql)

    # 5. Remplacer les alias seuls dans ORDER BY, etc.
    def replace_plain_aliases(match):
        alias = match.group(1)
        return alias_map.get(alias, alias)

    sql = re.sub(r'\b(\w+)\b(?=\s*[,;\n])', replace_plain_aliases, sql)

    # 6. Colonnes anonymisées dans AS 'xxx'
    def replace_column_alias(match):
        nonlocal column_idx
        name = match.group(1).strip("'\"[]")
        if name not in column_map:
            column_map[name] = f"col{column_idx}"
            column_idx += 1
        return f"AS '{column_map[name]}'"

    sql = re.sub(r"AS\s+'([^']+)'", replace_column_alias, sql, flags=re.IGNORECASE)

    # 7. Colonnes anonymisées dans AS alias (non quoté)
    def replace_select_alias(match):
        nonlocal column_idx
        alias = match.group(1).strip('"[]`')
        if alias not in column_map:
            column_map[alias] = f"col{column_idx}"
            column_idx += 1
        return f"AS {column_map[alias]}"

    sql = re.sub(r"AS\s+([\"`\[\]\w]+)", replace_select_alias, sql, flags=re.IGNORECASE)

    # 8. Sauvegarde du script anonymisé
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sql)

    # 9. Sauvegarde des mappages
    with open(mapping_file, "w", encoding="utf-8") as f:
        for d in (proc_map, variable_map, table_map, alias_map, column_map):
            for old, new in d.items():
                f.write(f"{old} > {new}\n")

    print(f"[✓] Script anonymisé dans {output_file}")
    print(f"[✓] Mapping généré dans {mapping_file}")

if __name__ == "__main__":
    anonymize_sql_procedure("input.sql")