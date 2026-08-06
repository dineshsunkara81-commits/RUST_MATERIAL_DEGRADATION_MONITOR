from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import csv
import os

# ========== CREATE APP INSTANCE ==========
app = Flask(__name__)
CSV_FILE = "assets.csv"

# ========== INITIALIZE CSV ==========
def init_csv():
    try:
        with open(CSV_FILE, 'r') as file:
            pass
    except FileNotFoundError:
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Asset", "Material", "Environment", 
                           "Age", "Length", "Width", "Risk"])

# ========== HOME ROUTE ==========
@app.route('/')
def home():
    return render_template("index.html")

# ========== DASHBOARD ROUTE ==========
@app.route('/dashboard')
def dashboard():
    assets = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            assets = list(reader)
    except FileNotFoundError:
        init_csv()
    
    total = len(assets)
    high = len([a for a in assets if a.get("Risk") == "High"])
    medium = len([a for a in assets if a.get("Risk") == "Medium"])
    low = len([a for a in assets if a.get("Risk") == "Low"])
    
    return render_template(
        "dashboard.html",
        assets=assets,
        total=total,
        high=high,
        medium=medium,
        low=low
    )

# ========== ADD ASSET ROUTE ==========
@app.route('/add', methods=["GET", "POST"])
def add_asset():
    if request.method == "POST":
        asset = request.form["asset"]
        material = request.form["material"]
        environment = request.form["environment"]
        age = int(request.form["age"])
        length = request.form["length"]
        width = request.form["width"]
        
        from logic.prediction import predict_risk
        risk = predict_risk(material, environment, age)
        
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([asset, material, environment, 
                           age, length, width, risk])
        
        return redirect(url_for("dashboard"))
    
    return render_template("add_asset.html")

# ========== VIEW ASSETS ROUTE ==========
@app.route('/assets')
def assets():
    data = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            data = list(reader)
    except FileNotFoundError:
        init_csv()
    
    return render_template("view_asset.html", assets=data)

# ========== PREDICTION ROUTE ==========
@app.route('/prediction')
def prediction():
    data = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            data = list(reader)
    except FileNotFoundError:
        init_csv()
    
    return render_template("prediction.html", assets=data)

# ========== REPORTS ROUTE ==========
@app.route('/reports')
def reports():
    return render_template("reports.html")

# ========== EXPORT CSV ROUTE ==========
@app.route('/export/csv')
def export_csv():
    try:
        return send_file(CSV_FILE, as_attachment=True, download_name='assets_export.csv')
    except Exception as e:
        return str(e), 500

# ========== DASHBOARD DATA API ==========
@app.route('/dashboard-data')
def dashboard_data():
    assets = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            assets = list(reader)
    except FileNotFoundError:
        init_csv()
    
    return {
        'total': len(assets),
        'high': len([a for a in assets if a.get('Risk') == 'High']),
        'medium': len([a for a in assets if a.get('Risk') == 'Medium']),
        'low': len([a for a in assets if a.get('Risk') == 'Low'])
    }

# ========== DELETE SINGLE ASSET (by row number) ==========
@app.route('/delete/<int:row_num>', methods=['POST'])
def delete_asset(row_num):
    try:
        # Read all assets
        assets = []
        header = []
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)
            assets = list(reader)
        
        # Check if row_num is valid (1-based index)
        if row_num < 1 or row_num > len(assets):
            return {'success': False, 'message': f'Asset at position {row_num} not found'}, 404
        
        # Get asset name for message
        asset_name = assets[row_num - 1][0] if len(assets[row_num - 1]) > 0 else f"Row {row_num}"
        
        # Remove the asset (subtract 1 because list is 0-indexed)
        del assets[row_num - 1]
        
        # Write back
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(assets)
        
        return {'success': True, 'message': f'"{asset_name}" deleted successfully'}, 200
            
    except Exception as e:
        print(f"Error: {e}")
        return {'success': False, 'message': str(e)}, 500

# ========== DELETE BULK ASSETS (by row numbers) ==========
@app.route('/delete-bulk', methods=['POST'])
def delete_bulk_assets():
    try:
        data = request.get_json()
        row_numbers = data.get('ids', [])
        
        if not row_numbers:
            return {'success': False, 'message': 'No assets selected'}, 400
        
        # Convert to integers and sort in reverse order
        row_numbers = sorted([int(idx) for idx in row_numbers], reverse=True)
        
        # Read all assets
        assets = []
        header = []
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)
            assets = list(reader)
        
        # Remove from highest index to lowest (to avoid shifting issues)
        deleted_count = 0
        for idx in row_numbers:
            if 1 <= idx <= len(assets):
                del assets[idx - 1]
                deleted_count += 1
        
        # Write back
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(assets)
        
        return {
            'success': True, 
            'message': f'{deleted_count} assets deleted successfully',
            'deleted_count': deleted_count
        }, 200
        
    except Exception as e:
        print(f"Error: {e}")
        return {'success': False, 'message': str(e)}, 500

# ========== RUN THE APP ==========
if __name__ == "__main__":
    init_csv()
    app.run(debug=True)