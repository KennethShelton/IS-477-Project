# Schema design (brief)

This file documents the initial schema design for the project database.

Tables planned:

- `air_quality`
  - unique_id INTEGER
  - indicator_id INTEGER
  - name TEXT
  - measure TEXT
  - measure_info TEXT
  - geo_type_name TEXT
  - geo_join_id TEXT
  - geo_place_name TEXT
  - time_period TEXT
  - start_date TEXT
  - data_value REAL
  - message TEXT

- `benmap`
  - bgrp TEXT PRIMARY KEY
  - many additional numeric columns (health impact estimates) present in the CSV

Notes:
- For convenience and reproducibility we will import the CSVs directly with `pandas.to_sql`.
- If a hand-defined schema is required later, extend `sql/schema.sql` with the full column list.
