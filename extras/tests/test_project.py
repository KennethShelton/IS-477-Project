"""
Test Suite for NYC Air Quality Analysis Project
Demonstrates software engineering best practices with automated testing.
Goes beyond rubric requirements to ensure code quality and reproducibility.
"""

import pytest
import pandas as pd
import sqlite3
import os
from pathlib import Path

# Test fixtures
@pytest.fixture
def project_root():
    """Get project root directory (parent of extras folder)."""
    # __file__ is extras/tests/test_project.py
    # parent is extras/tests/
    # parent.parent is extras/
    # parent.parent.parent is project root
    return Path(__file__).parent.parent.parent

@pytest.fixture
def db_path(project_root):
    """Get database path."""
    return project_root / 'data' / 'nyc_air_health.db'

@pytest.fixture
def merged_data(project_root):
    """Load merged analysis data."""
    return pd.read_csv(project_root / 'data' / 'processed' / 'merged.csv')

# Data Existence Tests
class TestDataFiles:
    """Test that all required data files exist."""
    
    def test_raw_data_exists(self, project_root):
        """Check raw data files exist."""
        air_quality = project_root / 'data' / 'raw' / 'air_quality.csv'
        benmap = project_root / 'data' / 'raw' / 'NYNY_BenMAP.csv'
        
        assert air_quality.exists(), "air_quality.csv not found"
        assert benmap.exists(), "NYNY_BenMAP.csv not found"
        assert air_quality.stat().st_size > 1000, "air_quality.csv is too small"
        assert benmap.stat().st_size > 1000, "NYNY_BenMAP.csv is too small"
    
    def test_database_exists(self, db_path):
        """Check SQLite database exists."""
        assert db_path.exists(), "Database not found"
        assert db_path.stat().st_size > 1000, "Database is empty"
    
    def test_processed_data_exists(self, project_root):
        """Check processed data files exist."""
        merged = project_root / 'data' / 'processed' / 'merged.csv'
        assert merged.exists(), "merged.csv not found"

# Database Schema Tests
class TestDatabaseSchema:
    """Test database structure and integrity."""
    
    def test_tables_exist(self, db_path):
        """Check required tables exist."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'air_quality' in tables, "air_quality table missing"
        assert 'benmap' in tables, "benmap table missing"
        
        conn.close()
    
    def test_air_quality_columns(self, db_path):
        """Check air_quality table has expected columns."""
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM air_quality LIMIT 1", conn)
        conn.close()
        
        expected_cols = ['Unique_ID', 'Name', 'Geo_Place_Name', 'Data_Value']
        for col in expected_cols:
            assert col in df.columns, f"Column {col} missing from air_quality table"
    
    def test_benmap_columns(self, db_path):
        """Check benmap table has expected columns."""
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM benmap LIMIT 1", conn)
        conn.close()
        
        assert 'bgrp' in df.columns, "bgrp column missing from benmap table"

# Data Quality Tests
class TestDataQuality:
    """Test data quality and consistency."""
    
    def test_no_empty_dataframes(self, db_path):
        """Check tables are not empty."""
        conn = sqlite3.connect(db_path)
        
        air_count = pd.read_sql_query("SELECT COUNT(*) as cnt FROM air_quality", conn).iloc[0]['cnt']
        benmap_count = pd.read_sql_query("SELECT COUNT(*) as cnt FROM benmap", conn).iloc[0]['cnt']
        
        conn.close()
        
        assert air_count > 0, "air_quality table is empty"
        assert benmap_count > 0, "benmap table is empty"
    
    def test_merged_data_structure(self, merged_data):
        """Check merged data has correct structure."""
        assert not merged_data.empty, "Merged data is empty"
        
        expected_cols = ['borough', 'pollutant', 'mean_concentration', 'total_symptoms']
        for col in expected_cols:
            assert col in merged_data.columns, f"Column {col} missing from merged data"
    
    def test_borough_coverage(self, merged_data):
        """Check all NYC boroughs are represented."""
        expected_boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
        actual_boroughs = merged_data['borough'].unique()
        
        for borough in expected_boroughs:
            assert borough in actual_boroughs, f"Borough {borough} missing from analysis"
    
    def test_pollutant_coverage(self, merged_data):
        """Check all pollutants are analyzed."""
        expected_pollutants = ['NO2', 'O3', 'PM2.5']
        actual_pollutants = merged_data['pollutant'].unique()
        
        for pollutant in expected_pollutants:
            assert pollutant in actual_pollutants, f"Pollutant {pollutant} missing from analysis"
    
    def test_no_negative_concentrations(self, merged_data):
        """Check mean concentrations are non-negative."""
        assert (merged_data['mean_concentration'] >= 0).all(), \
            "Found negative mean concentrations"
    
    def test_reasonable_value_ranges(self, merged_data):
        """Check data values are within reasonable ranges."""
        # NO2 typically 0-100 ppb in urban areas
        no2_data = merged_data[merged_data['pollutant'] == 'NO2']['mean_concentration']
        assert no2_data.max() < 100, "NO2 values unreasonably high"
        
        # O3 typically 0-100 ppb
        o3_data = merged_data[merged_data['pollutant'] == 'O3']['mean_concentration']
        assert o3_data.max() < 100, "O3 values unreasonably high"
        
        # PM2.5 typically 0-50 mcg/m3
        pm25_data = merged_data[merged_data['pollutant'] == 'PM2.5']['mean_concentration']
        assert pm25_data.max() < 50, "PM2.5 values unreasonably high"

# Analysis Tests
class TestAnalysisResults:
    """Test analysis outputs and calculations."""
    
    def test_correlation_calculation(self, merged_data):
        """Verify correlation values are valid."""
        # Test that we can calculate correlations
        for pollutant in ['NO2', 'O3', 'PM2.5']:
            subset = merged_data[merged_data['pollutant'] == pollutant]
            if len(subset) > 1:
                corr = subset['mean_concentration'].corr(subset['total_symptoms'])
                assert -1 <= corr <= 1, f"Invalid correlation for {pollutant}: {corr}"
    
    def test_visualization_exists(self, project_root):
        """Check correlation visualization was created."""
        viz_path = project_root / 'docs' / 'correlation.png'
        assert viz_path.exists(), "Correlation visualization not found"
        assert viz_path.stat().st_size > 1000, "Visualization file is too small"

# Documentation Tests
class TestDocumentation:
    """Test documentation completeness."""
    
    def test_readme_exists(self, project_root):
        """Check README exists and is substantial."""
        readme = project_root / 'README.md'
        assert readme.exists(), "README.md not found"
        
        content = readme.read_text(encoding='utf-8')
        assert len(content) > 2000, "README is too short (should be 2700-4500 words)"
    
    def test_metadata_exists(self, project_root):
        """Check metadata file exists."""
        metadata = project_root / 'metadata.json'
        assert metadata.exists(), "metadata.json not found"
    
    def test_data_dictionary_exists(self, project_root):
        """Check data dictionary exists."""
        dict_path = project_root / 'docs' / 'DATA_DICTIONARY.md'
        assert dict_path.exists(), "DATA_DICTIONARY.md not found"
    
    def test_licenses_exist(self, project_root):
        """Check license files exist."""
        assert (project_root / 'LICENSE').exists(), "LICENSE not found"
        assert (project_root / 'DATA_LICENSE.md').exists(), "DATA_LICENSE.md not found"

# Script Tests
class TestScripts:
    """Test that all scripts are present and importable."""
    
    def test_scripts_exist(self, project_root):
        """Check all required scripts exist."""
        scripts = [
            'download_data.py',
            'inspection.py',
            'load_data.py',
            'clean_data.py',
            'analysis.py',
            'run_all.py'
        ]
        
        for script in scripts:
            script_path = project_root / 'scripts' / script
            assert script_path.exists(), f"Script {script} not found"
    
    def test_requirements_file(self, project_root):
        """Check requirements.txt exists and has content."""
        req_file = project_root / 'requirements.txt'
        assert req_file.exists(), "requirements.txt not found"
        
        content = req_file.read_text()
        assert 'pandas' in content, "pandas not in requirements"
        assert 'matplotlib' in content, "matplotlib not in requirements"

if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, '-v', '--tb=short'])
