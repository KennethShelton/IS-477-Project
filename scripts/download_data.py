"""
Data Acquisition Script for NYC Air Quality and Health Project

This script downloads the raw datasets and verifies their integrity using SHA-256 checksums.
Run this script before executing the analysis pipeline if the data is not already present.
"""

import os
import hashlib
import urllib.request
import sys

AIR_QUALITY_URL = "https://data.cityofnewyork.us/api/views/c3uy-2p5r/rows.csv?accessType=DOWNLOAD"
BENMAP_URL = "https://edg.epa.gov/data/Public/ORD/EnviroAtlas/NYNY_BenMAP.csv"

EXPECTED_CHECKSUMS = {
    "air_quality.csv": "",
    "NYNY_BenMAP.csv": ""
}

def calculate_sha256(filepath):
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_file(url, destination):
    """Download a file from URL to destination with progress indication."""
    print(f"Downloading {os.path.basename(destination)}...")
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"✓ Downloaded to {destination}")
        return True
    except Exception as e:
        print(f"✗ Error downloading {url}: {e}")
        return False

def verify_checksum(filepath, expected_checksum):
    """Verify file checksum against expected value."""
    if not expected_checksum:
        print(f"⚠ No expected checksum provided for {os.path.basename(filepath)}. Skipping verification.")
        actual_checksum = calculate_sha256(filepath)
        print(f"  Calculated checksum: {actual_checksum}")
        print(f"  Please add this to EXPECTED_CHECKSUMS in the script for future verification.")
        return True
    
    actual_checksum = calculate_sha256(filepath)
    if actual_checksum == expected_checksum:
        print(f"✓ Checksum verified for {os.path.basename(filepath)}")
        return True
    else:
        print(f"✗ Checksum mismatch for {os.path.basename(filepath)}!")
        print(f"  Expected: {expected_checksum}")
        print(f"  Actual:   {actual_checksum}")
        return False

def main():
    # Create data directory if it doesn't exist
    raw_dir = os.path.join(".", "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    
    print("=" * 60)
    print("NYC Air Quality and Health Project - Data Acquisition")
    print("=" * 60)
    
    # Download Air Quality data
    air_quality_path = os.path.join(raw_dir, "air_quality.csv")
    if os.path.exists(air_quality_path):
        print(f"\n{os.path.basename(air_quality_path)} already exists.")
        overwrite = input("Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Skipping download.")
        else:
            if not download_file(AIR_QUALITY_URL, air_quality_path):
                sys.exit(1)
    else:
        if not download_file(AIR_QUALITY_URL, air_quality_path):
            sys.exit(1)
    
    # Verify Air Quality checksum
    if not verify_checksum(air_quality_path, EXPECTED_CHECKSUMS["air_quality.csv"]):
        print("\n⚠ Warning: Checksum verification failed. The file may be corrupted or updated.")
        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            sys.exit(1)
    
    # Download BenMAP data
    benmap_path = os.path.join(raw_dir, "NYNY_BenMAP.csv")
    if os.path.exists(benmap_path):
        print(f"\n{os.path.basename(benmap_path)} already exists.")
        overwrite = input("Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Skipping download.")
        else:
            if not download_file(BENMAP_URL, benmap_path):
                sys.exit(1)
    else:
        if not download_file(BENMAP_URL, benmap_path):
            sys.exit(1)
    
    # Verify BenMAP checksum
    if not verify_checksum(benmap_path, EXPECTED_CHECKSUMS["NYNY_BenMAP.csv"]):
        print("\n⚠ Warning: Checksum verification failed. The file may be corrupted or updated.")
        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            sys.exit(1)
    
    # Write checksums to file
    checksums_path = os.path.join(raw_dir, "checksums.txt")
    with open(checksums_path, "w") as f:
        f.write(f"air_quality.csv: {calculate_sha256(air_quality_path)}\n")
        f.write(f"NYNY_BenMAP.csv: {calculate_sha256(benmap_path)}\n")
    print(f"\n✓ Checksums written to {checksums_path}")
    
    print("\n" + "=" * 60)
    print("Data acquisition complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the downloaded files in data/raw/")
    print("2. Run the analysis pipeline: python scripts/run_all.py")

if __name__ == "__main__":
    main()
