import sqlite3
import ast

def parse_list(value):
    """
    Converte strings como:
    "['Cabernet Sauvignon', 'Merlot']"
    Em listas reais: ["Cabernet Sauvignon", "Merlot"]
    """
    if not value or value.strip() == "":
        return []

    value = value.strip()

    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed]
        else:
            return [str(parsed)]
    except Exception:
        cleaned = value.strip("[]")
        parts = [p.strip(" '\"") for p in cleaned.split(",")]
        return [p for p in parts if p]

def main():
    conn = sqlite3.connect("wines.db")
    cur = conn.cursor()

    # NON-VINTAGE
    cur.execute(
        "SELECT VintageID FROM Vintage WHERE IsNonVintage = 1 AND Year IS NULL"
    )
    row = cur.fetchone()
    if row:
        non_vintage_id = row[0]
    else:
        cur.execute(
            "INSERT INTO Vintage (Year, IsNonVintage) VALUES (?, ?)",
            (None, 1),
        )
        non_vintage_id = cur.lastrowid

    # RAW DATA
    cur.execute("SELECT WineID, Grapes, Harmonize, Vintages FROM RawWine")
    rows = cur.fetchall()

    for wine_id, grapes, harmonize, vintages in rows:

        # -----------------------------------------
        # GRAPES
        # -----------------------------------------
        grapes_list = parse_list(grapes)
        for grape_name in grapes_list:
            cur.execute(
                "INSERT OR IGNORE INTO Grape (GrapeName) VALUES (?)",
                (grape_name,),
            )
            cur.execute(
                "SELECT GrapeID FROM Grape WHERE GrapeName = ?",
                (grape_name,),
            )
            grape_id = cur.fetchone()[0]

            cur.execute(
                "INSERT OR IGNORE INTO WineGrape (WineID, GrapeID) VALUES (?, ?)",
                (wine_id, grape_id),
            )

        # -----------------------------------------
        # DISHES
        # -----------------------------------------
        dishes_list = parse_list(harmonize)
        for dish_name in dishes_list:
            cur.execute(
                "INSERT OR IGNORE INTO Dish (DishName) VALUES (?)",
                (dish_name,),
            )
            cur.execute(
                "SELECT DishID FROM Dish WHERE DishName = ?",
                (dish_name,),
            )
            dish_id = cur.fetchone()[0]

            cur.execute(
                "INSERT OR IGNORE INTO WineDish (WineID, DishID) VALUES (?, ?)",
                (wine_id, dish_id),
            )

        # -----------------------------------------
        # VINTAGES
        # -----------------------------------------
        if vintages:
            vintages_list = parse_list(vintages)

            for v in vintages_list:
                if v.lower() in ["nv", "n.v.", "non-vintage"]:
                    # Liga ao registro non-vintage
                    cur.execute(
                        "INSERT OR IGNORE INTO WineVintage (WineID, VintageID) VALUES (?, ?)",
                        (wine_id, non_vintage_id),
                    )
                    continue

                # Tenta converter para ano
                try:
                    year = int(v)
                except ValueError:
                    continue

                # Verifica se o ano já existe
                cur.execute(
                    "SELECT VintageID FROM Vintage WHERE Year = ? AND IsNonVintage = 0",
                    (year,),
                )
                row_v = cur.fetchone()

                if row_v:
                    vintage_id = row_v[0]
                else:
                    cur.execute(
                        "INSERT INTO Vintage (Year, IsNonVintage) VALUES (?, ?)",
                        (year, 0),
                    )
                    vintage_id = cur.lastrowid

                cur.execute(
                    "INSERT OR IGNORE INTO WineVintage (WineID, VintageID) VALUES (?, ?)",
                    (wine_id, vintage_id),
                )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
