@app.route('/cam1', methods=['POST'])
def cam1_webhook():
    try:
        data = request.get_json()
        lp = data.get('LP')
        scan_time = data.get('scan_time')

        if not lp or not scan_time:
            return jsonify({"error": "Missing LP or scan_time"}), 400

        # Get timestamps
        now = datetime.now()
        created_on = now.date().isoformat()
        created_at = now.time().strftime('%H:%M:%S')

        # Connect and create Cam1 if not exists
        conn = sqlite3.connect('final_carwash_complete.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cam1 (
                LP TEXT UNIQUE,
                scan_time TEXT,
                Created_on DATE,
                Created_at TIME
            )
        ''')

        cursor.execute('''
            INSERT OR IGNORE INTO Cam1 (LP, scan_time, Created_on, Created_at)
            VALUES (?, ?, ?, ?)
        ''', (lp, scan_time, created_on, created_at))

        conn.commit()
        conn.close()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
