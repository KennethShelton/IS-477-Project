-- air_quality: key fields from data.gov Air Quality CSV
DROP TABLE IF EXISTS air_quality;
CREATE TABLE air_quality (
  unique_id INTEGER,
  indicator_id INTEGER,
  name TEXT,
  measure TEXT,
  measure_info TEXT,
  geo_type_name TEXT,
  geo_join_id TEXT,
  geo_place_name TEXT,
  time_period TEXT,
  start_date TEXT,
  data_value REAL,
  message TEXT
);

-- benmap (EnviroAtlas BenMAP results) minimal table; many more columns exist in the CSV.
DROP TABLE IF EXISTS benmap;
CREATE TABLE benmap (
  bgrp TEXT PRIMARY KEY
  -- other columns are numerous (health impact estimates). The load script will import
  -- the full CSV into a table automatically when using pandas.to_sql.
);

-- Notes:
-- The import script (scripts/load_data.py) will attempt to use pandas to load the
-- full CSVs into the database. If you prefer a hand-crafted schema for benmap,
-- extend this file with the full column list.
