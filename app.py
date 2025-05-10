from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_PATH = 'final_carwash_complete.db'

def handle_cam_feed(table_name, lp, scan_time):
    # Get timestamps
    now = datetime.now()
    created_on = now.date().isoformat()
    created_at = now.time().strftime('%H:%M:%S')

    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            LP TEXT UNIQUE,
            scan_time TEXT,
            Created_on DATE,
            Created_at TIME
        )
    ''')

    # Insert data
    cursor.execute(f'''
        INSERT OR IGNORE INTO {table_name} (LP, scan_time, Created_on, Created_at)
        VALUES (?, ?, ?, ?)
    ''', (lp, scan_time, created_on, created_at))

    conn.commit()
    conn.close()


# Shared handler function
def create_cam_endpoint(table_name):
    def endpoint():
        try:
            data = request.get_json()
            lp = data.get('LP')
            scan_time = data.get('scan_time')

            if not lp or not scan_time:
                return jsonify({"error": "Missing LP or scan_time"}), 400

            handle_cam_feed(table_name, lp, scan_time)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return endpoint


# Register endpoints
app.route('/cam1', methods=['POST'])(create_cam_endpoint('Cam1'))
app.route('/cam2', methods=['POST'])(create_cam_endpoint('Cam2'))
app.route('/cam3', methods=['POST'])(create_cam_endpoint('Cam3'))
app.route('/cam4', methods=['POST'])(create_cam_endpoint('Cam4'))
app.route('/cam5', methods=['POST'])(create_cam_endpoint('Cam5'))


# Run locally
if __name__ == '__main__':
    app.run(debug=True)
