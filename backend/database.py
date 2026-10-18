import sqlite3

DATABASE_NAME = 'opphub.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Opportunities Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            tag TEXT NOT NULL,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            eligibility TEXT,
            amount TEXT,
            deadline TEXT,
            details TEXT,
            apply_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Subscribers & Email Notification Preferences Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            fields_of_interest TEXT NOT NULL,   -- e.g. "scholarships, internships, hackathons"
            notification_type TEXT NOT NULL,    -- "new_opportunities", "deadline_reminders", or "both"
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print(" Database & Subscribers table initialized successfully!")

if __name__ == '__main__':
    init_db()