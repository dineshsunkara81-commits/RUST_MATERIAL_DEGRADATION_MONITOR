# logic/file_handler.py
import csv
import os

CSV_FILE = "assets.csv"

def read_assets():
    """Read all assets from CSV file"""
    assets = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            assets = list(reader)
    except FileNotFoundError:
        pass
    return assets

def write_assets(assets, header):
    """Write assets to CSV file"""
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(assets)

def add_asset(asset_data):
    """Add a single asset to CSV"""
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(asset_data)

def delete_asset(row_num):
    """Delete asset by row number"""
    assets = []
    header = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        assets = list(reader)
    
    if 1 <= row_num <= len(assets):
        deleted_asset = assets.pop(row_num - 1)
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(assets)
        return deleted_asset
    return None

def delete_bulk_assets(row_numbers):
    """Delete multiple assets by row numbers"""
    assets = []
    header = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        assets = list(reader)
    
    row_numbers = sorted([int(r) for r in row_numbers], reverse=True)
    deleted = []
    for idx in row_numbers:
        if 1 <= idx <= len(assets):
            deleted.append(assets.pop(idx - 1))
    
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(assets)
    
    return deleted