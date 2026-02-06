import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask, request
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    return render_template('index.html', message='Hello World!')

#Barra de pesquisa 
# Barra de pesquisa 
@APP.route('/search/')
def search():
    q = request.args.get("q")

    if not q:
        return render_template("search_results.html", query=q, results={})

    q_pattern = f"%{q}%"
    results = {}

    # Procurar vinhos (limpa nomes e evita duplicados)
    results["wines"] = db.execute("""
        SELECT DISTINCT
            w.WineID,
            REPLACE(
                REPLACE(
                    REPLACE(w.WineName, '''', ''), 
                '[', ''), 
            ']', '') AS WineName
        FROM Wine w
        WHERE REPLACE(
                REPLACE(
                    REPLACE(w.WineName, '''', ''), 
                '[', ''), 
            ']', '') LIKE ?
        ORDER BY WineName;
    """, (q_pattern,)).fetchall()

    # Procurar castas (apenas castas ligadas a vinhos, sem repetição)
    results["grapes"] = db.execute("""
        SELECT 
            MIN(g.GrapeID) AS GrapeID,
            REPLACE(
                REPLACE(
                    REPLACE(g.GrapeName, '''', ''), 
                '[', ''), 
            ']', '') AS GrapeName
        FROM Grape g
        JOIN WineGrape wg ON g.GrapeID = wg.GrapeID
        WHERE REPLACE(
                REPLACE(
                    REPLACE(g.GrapeName, '''', ''), 
                '[', ''), 
            ']', '') LIKE ?
        GROUP BY GrapeName
        ORDER BY GrapeName;
    """, (q_pattern,)).fetchall()

    # Procurar pratos (apenas pratos que realmente têm vinhos)
    results["dishes"] = db.execute("""
        SELECT DISTINCT
            d.DishID,
            REPLACE(
                REPLACE(
                    REPLACE(d.DishName, '''', ''), 
                '[', ''), 
            ']', '') AS DishName
        FROM Dish d
        JOIN WineDish wd ON d.DishID = wd.DishID
        WHERE REPLACE(
                REPLACE(
                    REPLACE(d.DishName, '''', ''), 
                '[', ''), 
            ']', '') LIKE ?
        ORDER BY DishName;
    """, (q_pattern,)).fetchall()

    # Procurar regiões
    results["regions"] = db.execute("""
        SELECT DISTINCT
            RegionID,
            RegionName
        FROM Region
        WHERE RegionName LIKE ?
        ORDER BY RegionName;
    """, (q_pattern,)).fetchall()

    # Procurar países
    results["countries"] = db.execute("""
        SELECT DISTINCT
            Code,
            CountryName
        FROM Country
        WHERE CountryName LIKE ?
        ORDER BY CountryName;
    """, (q_pattern,)).fetchall()

    # Procurar vinícolas
    results["wineries"] = db.execute("""
        SELECT DISTINCT
            WineryID,
            WineryName
        FROM Winery
        WHERE WineryName LIKE ?
        ORDER BY WineryName;
    """, (q_pattern,)).fetchall()

    # Procurar vintages (anos de colheita)
    results["vintages"] = db.execute("""
        SELECT DISTINCT
            v.VintageID,
            CASE 
                WHEN v.IsNonVintage = 1 THEN 'N.V.'
                ELSE CAST(v.Year AS TEXT)
            END AS VintageLabel
        FROM Vintage v
        WHERE v.IsNonVintage = 0
          AND CAST(v.Year AS TEXT) LIKE ?
        ORDER BY v.Year;
    """, (q_pattern,)).fetchall()

    return render_template("search_results.html", query=q, results=results)



# Lista de vinhos
@APP.route('/Wine/')
def list_wines():
    rows = db.execute("SELECT WineID, WineName, Type FROM Wine ORDER BY WineName COLLATE NOCASE;").fetchall()
    return render_template('wine_list.html', wines=rows)

#Detalhes do vinho
@APP.route('/Wine/<int:wine_id>/')
def wine_detail(wine_id):
    wine = db.execute(
        "SELECT * FROM Wine WHERE WineID = ?",
        (wine_id,)
    ).fetchone()

    grapes = db.execute("""
        SELECT 
            g.GrapeID,
            REPLACE(
                REPLACE(
                    REPLACE(g.GrapeName, '''', ''), 
                '[', ''), 
            ']', '') AS GrapeName
        FROM Grape g
        JOIN WineGrape wg ON g.GrapeID = wg.GrapeID
        WHERE wg.WineID = ?
        ORDER BY GrapeName;
    """, (wine_id,)).fetchall()

    dishes = db.execute(
        """
        SELECT d.DishID, d.DishName
        FROM Dish d
        JOIN WineDish wd ON d.DishID = wd.DishID
        WHERE wd.WineID = ?
        ORDER BY d.DishName
        """,
        (wine_id,)
    ).fetchall()

    vintages = db.execute(
        """
        SELECT v.VintageID, v.Year, v.IsNonVintage
        FROM Vintage v
        JOIN WineVintage wv ON v.VintageID = wv.VintageID
        WHERE wv.WineID = ?
        ORDER BY v.IsNonVintage DESC, v.Year
        """,
        (wine_id,)
    ).fetchall()


    return render_template(
        'wine_detail.html',
        wine=wine,
        grapes=grapes,
        dishes=dishes,
        vintages=vintages
    )


# Lista de países
@APP.route('/Country/')
def list_countries():
    rows = db.execute("SELECT Code, CountryName FROM Country ORDER BY CountryName COLLATE NOCASE;").fetchall()
    return render_template('country_list.html', countries=rows)

# Detalhe de um país
@APP.route('/Country/<code>/')
def country_detail(code):
    row = db.execute(
        "SELECT * FROM Country WHERE Code = ?",
        (code,)
    ).fetchone()
    return render_template('country_detail.html', country=row)

# Lista de regiões
@APP.route('/Region/')
def list_regions():
    rows = db.execute("SELECT RegionID, RegionName FROM Region ORDER BY RegionName COLLATE NOCASE;").fetchall()
    return render_template('region_list.html', regions=rows)

# Detalhe de uma região
@APP.route('/Region/<int:region_id>/')
def region_detail(region_id):
    row = db.execute(
        "SELECT * FROM Region WHERE RegionID = ?",
        (region_id,)
    ).fetchone()
    return render_template('region_detail.html', region=row)

# Lista de produtoras (wineries)
@APP.route('/Winery/')
def list_wineries():
    rows = db.execute("SELECT WineryID, WineryName FROM Winery ORDER BY WineryName COLLATE NOCASE;").fetchall()
    return render_template('winery_list.html', wineries=rows)

# Detalhe de uma winery
@APP.route('/Winery/<int:winery_id>/')
def winery_detail(winery_id):
    row = db.execute(
        "SELECT * FROM Winery WHERE WineryID = ?",
        (winery_id,)
    ).fetchone()
    return render_template('winery_detail.html', winery=row)

# Grapes
@APP.route('/Grape/')
def list_grapes():
    rows = db.execute("""
        SELECT DISTINCT
            g.GrapeID,
            REPLACE(
                REPLACE(
                    REPLACE(g.GrapeName, '''', ''), 
                '[', ''), 
            ']', '') AS GrapeName
        FROM Grape g
        JOIN WineGrape wg ON g.GrapeID = wg.GrapeID
        ORDER BY GrapeName;
    """).fetchall()
    return render_template('grape_list.html', grapes=rows)


#Detalhes das uvas
@APP.route('/Grape/<int:grape_id>/')
def grape_detail(grape_id):
    grape = db.execute("""
        SELECT 
            GrapeID,
            REPLACE(
                REPLACE(
                    REPLACE(GrapeName, '''', ''), 
                '[', ''), 
            ']', '') AS GrapeName
        FROM Grape
        WHERE GrapeID = ?;
    """, (grape_id,)).fetchone()

    wines = db.execute("""
        SELECT w.WineID, w.WineName, w.Type
        FROM Wine w
        JOIN WineGrape wg ON w.WineID = wg.WineID
        WHERE wg.GrapeID = ?
        ORDER BY w.WineName;
    """, (grape_id,)).fetchall()

    from_wine = request.args.get('from_wine')
    return render_template(
        'grape_detail.html',
        grape=grape,
        wines=wines,
        from_wine=from_wine
    )


# Dishes
@APP.route('/Dish/')
def list_dishes():
    rows = db.execute("""
        SELECT DISTINCT
            d.DishID,
            REPLACE(
                REPLACE(
                    REPLACE(d.DishName, '''', ''), 
                '[', ''), 
            ']', '') AS DishName
        FROM Dish d
        JOIN WineDish wd ON d.DishID = wd.DishID
        ORDER BY DishName;
    """).fetchall()
    return render_template('dish_list.html', dishes=rows)


# Detalhe dos dishes
@APP.route('/Dish/<int:dish_id>/')
def dish_detail(dish_id):
    dish = db.execute("""
        SELECT 
            DishID,
            REPLACE(
                REPLACE(
                    REPLACE(DishName, '''', ''), 
                '[', ''), 
            ']', '') AS DishName
        FROM Dish
        WHERE DishID = ?;
    """, (dish_id,)).fetchone()

    wines = db.execute("""
        SELECT w.WineID, w.WineName, w.Type
        FROM Wine w
        JOIN WineDish wd ON w.WineID = wd.WineID
        WHERE wd.DishID = ?
        ORDER BY w.WineName;
    """, (dish_id,)).fetchall()

    return render_template('dish_detail.html', dish=dish, wines=wines)


# VINTAGES
@APP.route('/Vintage/')
def list_vintages():
    rows = db.execute("""
        SELECT DISTINCT
            v.VintageID,
            CASE 
                WHEN v.IsNonVintage = 1 THEN 'N.V.'
                ELSE CAST(v.Year AS TEXT)
            END AS VintageName
        FROM Vintage v
        JOIN WineVintage wv ON v.VintageID = wv.VintageID
        ORDER BY v.IsNonVintage, v.Year;
    """).fetchall()
    
    return render_template('vintage_list.html', vintages=rows)

# Detalhes dos Vintages
@APP.route('/Vintage/<int:vintage_id>/')
def vintage_detail(vintage_id):
    vintage = db.execute("""
        SELECT 
            VintageID,
            CASE 
                WHEN IsNonVintage = 1 THEN 'N.V.'
                ELSE CAST(Year AS TEXT)
            END AS VintageName,
            Year,
            IsNonVintage
        FROM Vintage
        WHERE VintageID = ?;
    """, (vintage_id,)).fetchone()

    wines = db.execute("""
        SELECT w.WineID, w.WineName, w.Type
        FROM Wine w
        JOIN WineVintage wv ON w.WineID = wv.WineID
        WHERE wv.VintageID = ?
        ORDER BY w.WineName;
    """, (vintage_id,)).fetchall()

    return render_template('vintage_detail.html', vintage=vintage, wines=wines)


#---------------------- INTERROGAÇÕES -----------------------

#Q1 - Número de vinhos por país
@APP.route('/q1/')
def q1():
    sql = """
    SELECT c.CountryName AS Country,
           COUNT(w.WineID) AS NumWines
    FROM Wine w
    JOIN Region r ON w.RegionID = r.RegionID
    JOIN Country c ON r.CountryCode = c.Code
    GROUP BY c.CountryName
    ORDER BY NumWines DESC
    """
    rows = db.execute(sql).fetchall()
    return render_template('q1.html', rows=rows)

#Q2 - Número de vinhos por região
@APP.route('/q2/')
def q2():
    sql = """
    SELECT r.RegionName AS Region,
           c.CountryName AS Country,
           COUNT(w.WineID) AS NumWines
    FROM Wine w
    JOIN Region r ON w.RegionID = r.RegionID
    JOIN Country c ON r.CountryCode = c.Code
    GROUP BY r.RegionName, c.CountryName
    ORDER BY NumWines DESC
    """
    rows = db.execute(sql).fetchall()
    return render_template('q2.html', rows=rows)

#Q3 - Agregações sobre ABV
@APP.route('/q3/')
def q3():
    sql = """
    SELECT AVG(ABV)  AS MediaABV,
           COUNT(*)  AS NumWines,
           SUM(ABV)  AS TotalABV,
           MAX(ABV)  AS MaxABV,
           MIN(ABV)  AS MinABV
    FROM Wine
    WHERE ABV IS NOT NULL
    """
    rows = db.execute(sql).fetchall()
    return render_template('q3.html', rows=rows)

#Q4 — Castas usadas em mais de 40 vinhos
@APP.route('/q4/')
def q4():
    sql = """
    SELECT g.GrapeName,
           COUNT(wg.WineID) AS NumWines
    FROM Grape g
    JOIN WineGrape wg ON g.GrapeID = wg.GrapeID
    GROUP BY g.GrapeName
    HAVING COUNT(wg.WineID) > 40
    ORDER BY NumWines DESC, g.GrapeName
    """
    rows = db.execute(sql).fetchall()
    return render_template('q4.html', rows=rows)

#Q5 — Vinhos que harmonizam com pratos contendo “Beef”
@APP.route('/q5/')
def q5():
    sql = """
    SELECT d.DishName,
           w.WineName,
           wy.WineryName,
           c.CountryName
    FROM Wine w
    JOIN WineDish wd ON w.WineID = wd.WineID
    JOIN Dish d ON wd.DishID = d.DishID
    JOIN Winery wy ON w.WineryID = wy.WineryID
    JOIN Region r ON w.RegionID = r.RegionID
    JOIN Country c ON r.CountryCode = c.Code
    WHERE d.DishName LIKE '%Beef%'
    ORDER BY w.WineName
    """
    rows = db.execute(sql).fetchall()
    return render_template('q5.html', rows=rows)

#Q6 — Segunda maior graduação alcoólica
@APP.route('/q6/')
def q6():
    sql = """
    SELECT WineName,
           ABV
    FROM Wine
    WHERE ABV = (
        SELECT MAX(ABV)
        FROM Wine
        WHERE ABV < (SELECT MAX(ABV) FROM Wine)
    )
    """
    rows = db.execute(sql).fetchall()
    return render_template('q6.html', rows=rows)

#Q7 — Vinhos que nao tem website
@APP.route('/q7/')
def q7():
    sql = """
    SELECT 
            w.WineID,
            w.WineName,
            wy.WineryName
        FROM Wine w
        JOIN Winery wy ON wy.WineryID = w.WineryID
        WHERE w.WineryID NOT IN (
            SELECT WineryID
            FROM Winery
            WHERE Website IS NOT NULL AND Website <> ''
        );
    """
    rows = db.execute(sql).fetchall()
    return render_template('q7.html', rows=rows)

#Q8 — Castas usadas em vinhos Red e White
@APP.route('/q8/')
def q8():
    sql = """
    SELECT DISTINCT g.GrapeName
    FROM Grape g
    JOIN WineGrape wg ON g.GrapeID = wg.GrapeID
    JOIN Wine w       ON w.WineID = wg.WineID
    WHERE w.Type = 'Red'
    INTERSECT
    SELECT DISTINCT g.GrapeName
    FROM Grape g
    JOIN WineGrape wg ON g.GrapeID = wg.GrapeID
    JOIN Wine w       ON w.WineID = wg.WineID
    WHERE w.Type = 'White'
    """
    rows = db.execute(sql).fetchall()
    return render_template('q8.html', rows=rows)

#Q9 — Castas exclusivas de um único vinho
@APP.route('/q9/')
def q9():
    sql = """
    SELECT g.GrapeName
    FROM Grape g
    JOIN WineGrape wg ON g.GrapeID = wg.GrapeID
    GROUP BY g.GrapeName
    HAVING COUNT(DISTINCT wg.WineID) = 1
    ORDER BY g.GrapeName
    """
    rows = db.execute(sql).fetchall()
    return render_template('q9.html', rows=rows)

#Q10 — Produtores com mais de 5 vinhos
@APP.route('/q10/')
def q10():
    sql = """
    SELECT wy.WineryName,
           COUNT(w.WineID) AS NumWines
    FROM Winery wy
    JOIN Wine w ON w.WineryID = wy.WineryID
    GROUP BY wy.WineryName
    HAVING COUNT(w.WineID) > 5
    ORDER BY NumWines DESC, wy.WineryName
    """
    rows = db.execute(sql).fetchall()
    return render_template('q10.html', rows=rows)
