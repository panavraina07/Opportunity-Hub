from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db
from routes import api_bp

# Initialize Flask App
app = Flask(__name__)

# Enable CORS for all routes (allows your HTML frontend to call APIs)
CORS(app)

# Register API Blueprint with URL prefix '/api'
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to OpportunityHub API Server!",
        "status": "Online",
        "documentation": {
            "GET /api/opportunities": "Fetch all opportunities (supports ?category= and ?q=)",
            "POST /api/opportunities": "Create new opportunity",
            "GET /api/stats": "Get overall statistics"
        }
    })

if __name__ == '__main__':
    # Initialize database table on server start
    init_db()
    
    # Run development server on port 5000
    print(" Starting OpportunityHub Backend at http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True)