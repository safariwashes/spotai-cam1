from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_PATH = 'final_carwash_complete.db'

@app.route('/cam1', methods=['POST'])
def cam1_webhook():
    try:
        data = request.get_json()

        lp = data.get('LP')
        scan_time = data.get('scan_time')

        if not lp or not scan_time:
            return jsonify({"error": "Missing LP or scan_time"}), 400

        # Get current date and time
        now = datetime.now()
        created_on = now.date().isoformat()
        created_at = now.time().strftime('%H:%M:%S')

        # Insert into Cam1 table
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO Cam1 (LP, scan_time, Created_on, Created_at)
            VALUES (?, ?, ?, ?)
        ''', (lp, scan_time, created_on, created_at))
        conn.commit()
        conn.close()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 👇 This part is required to start the app
if __name__ == '__main__':
    app.run(debug=True)
