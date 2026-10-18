from flask import Blueprint, jsonify, request
from database import get_db_connection

api_bp = Blueprint('api', __name__)

# -------------------------------------------------------------
# 1. GET ALL OPPORTUNITIES (with Search & Category Filtering)
# -------------------------------------------------------------
@api_bp.route('/opportunities', methods=['GET'])
def get_opportunities():
    category = request.args.get('category')
    search_query = request.args.get('q')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM opportunities WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if search_query:
        query += " AND (title LIKE ? OR organization LIKE ? OR tag LIKE ? OR details LIKE ?)"
        wildcard = f"%{search_query}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    opportunities = [dict(row) for row in rows]
    return jsonify({
        "success": True,
        "count": len(opportunities),
        "data": opportunities
    }), 200


# -------------------------------------------------------------
# 2. POST: ADD A NEW OPPORTUNITY (Feature 1 Modal Form)
# -------------------------------------------------------------
@api_bp.route('/opportunities', methods=['POST'])
def add_opportunity():
    data = request.get_json()
    required = ['category', 'tag', 'title', 'organization', 'apply_url']
    for field in required:
        if not data or field not in data:
            return jsonify({"success": False, "message": f"Field '{field}' is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO opportunities (category, tag, title, organization, eligibility, amount, deadline, details, apply_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['category'],
        data['tag'],
        data['title'],
        data['organization'],
        data.get('eligibility', ''),
        data.get('amount', ''),
        data.get('deadline', ''),
        data.get('details', ''),
        data['apply_url']
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"success": True, "message": "Opportunity added successfully!", "id": new_id}), 201


# -------------------------------------------------------------
# 3. POST: SUBSCRIBE FOR CUSTOM NOTIFICATIONS & DEADLINE ALERTS
# -------------------------------------------------------------
@api_bp.route('/subscribe', methods=['POST'])
def subscribe_notifications():
    data = request.get_json()

    if not data or 'email' not in data or not data['email'].strip():
        return jsonify({"success": False, "message": "Valid email address is required"}), 400

    email = data['email'].strip().lower()
    fields_of_interest = data.get('fields', 'all') # e.g. "scholarships, internships"
    notification_type = data.get('notification_type', 'both') # "new_opportunities", "deadline_reminders", or "both"

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO subscribers (email, fields_of_interest, notification_type)
            VALUES (?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                fields_of_interest = excluded.fields_of_interest,
                notification_type = excluded.notification_type
        ''', (email, fields_of_interest, notification_type))
        conn.commit()
        conn.close()
        return jsonify({
            "success": True, 
            "message": "Preferences saved! You will receive tailored deadline & opportunity alerts."
        }), 200
    except Exception as e:
        conn.close()
        return jsonify({"success": False, "message": str(e)}), 500


# -------------------------------------------------------------
# 4. GET SUMMARY STATS
# -------------------------------------------------------------
@api_bp.route('/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM opportunities")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(DISTINCT category) as categories_count FROM opportunities")
    categories_count = cursor.fetchone()['categories_count']
    conn.close()

    return jsonify({
        "success": True,
        "total_opportunities": total,
        "total_categories": categories_count
    }), 200