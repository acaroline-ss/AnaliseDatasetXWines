-- COUNTRY
CREATE TABLE Country (
    Code        TEXT PRIMARY KEY,
    CountryName TEXT NOT NULL
);

-- REGION
CREATE TABLE Region (
    RegionID    INTEGER PRIMARY KEY,
    RegionName  TEXT NOT NULL,
    CountryCode TEXT NOT NULL,
    FOREIGN KEY (CountryCode) REFERENCES Country(Code)
);

-- WINERY
CREATE TABLE Winery (
    WineryID   INTEGER PRIMARY KEY,
    WineryName TEXT NOT NULL,
    Website    TEXT
);

-- WINE
CREATE TABLE Wine (
    WineID    INTEGER PRIMARY KEY,
    WineName  TEXT NOT NULL,
    Type      TEXT,
    Elaborate TEXT,
    ABV       REAL,       -- SQLite usa REAL para floats
    Body      INTEGER,
    Acidity   INTEGER,
    RegionID  INTEGER,
    WineryID  INTEGER,
    FOREIGN KEY (RegionID) REFERENCES Region(RegionID),
    FOREIGN KEY (WineryID) REFERENCES Winery(WineryID)
);

-- GRAPE
CREATE TABLE Grape (
    GrapeID   INTEGER PRIMARY KEY AUTOINCREMENT,
    GrapeName TEXT NOT NULL UNIQUE
);

CREATE TABLE WineGrape (
    WineID  INTEGER NOT NULL,
    GrapeID INTEGER NOT NULL,
    PRIMARY KEY (WineID, GrapeID),
    FOREIGN KEY (WineID)  REFERENCES Wine(WineID)   ON DELETE CASCADE,
    FOREIGN KEY (GrapeID) REFERENCES Grape(GrapeID) ON DELETE CASCADE
);

-- DISH
CREATE TABLE Dish (
    DishID   INTEGER PRIMARY KEY AUTOINCREMENT,
    DishName TEXT NOT NULL UNIQUE
);

CREATE TABLE WineDish (
    WineID INTEGER NOT NULL,
    DishID INTEGER NOT NULL,
    PRIMARY KEY (WineID, DishID),
    FOREIGN KEY (WineID) REFERENCES Wine(WineID)  ON DELETE CASCADE,
    FOREIGN KEY (DishID) REFERENCES Dish(DishID)  ON DELETE CASCADE
);

-- VINTAGE
CREATE TABLE Vintage (
    VintageID    INTEGER PRIMARY KEY AUTOINCREMENT,
    Year         INTEGER,
    IsNonVintage INTEGER NOT NULL CHECK (IsNonVintage IN (0,1)),
    CHECK (
        (IsNonVintage = 1 AND Year IS NULL) OR
        (IsNonVintage = 0 AND Year IS NOT NULL)
    )
);

CREATE TABLE WineVintage (
    WineID    INTEGER NOT NULL,
    VintageID INTEGER NOT NULL,
    PRIMARY KEY (WineID, VintageID),
    FOREIGN KEY (WineID)    REFERENCES Wine(WineID)    ON DELETE CASCADE,
    FOREIGN KEY (VintageID) REFERENCES Vintage(VintageID) ON DELETE CASCADE
);
