from database import get_db_connection, init_db

def seed_data():
    init_db() # Ensure table exists first
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear old records to prevent duplicate seeding
    cursor.execute('DELETE FROM opportunities')

    starter_items = [
        # SCHOLARSHIPS
        ("scholarship", "Corporate", "SBI Platinum Jubilee Asha Scholarship 2026", "SBI Foundation", 
         "Classes 9–12, UG, PG (NIRF Top 300 / NAAC A / MBBS / IIT-IIM)", "₹15,000 – ₹15,00,000", "4 September 2026", "≥75% or 7.9 CGPA", "https://www.sbiashascholarship.co.in"),
        
        ("scholarship", "Private", "Reliance Foundation Scholarship 2026–27", "Reliance Foundation", 
         "Full-time first-year UG & PG students", "Up to ₹2 Lakh (UG) / ₹6 Lakh (PG)", "Open for 2026", "Merit + need-based", "https://scholarships.reliancefoundation.org"),
        
        ("scholarship", "Corporate", "HDFC Parivartan ECSS Scheme", "HDFC Bank", 
         "Classes 1–12, Diploma, ITI, Polytechnic, UG & PG", "Up to ₹75,000", "31 August 2026", "Family income ≤₹2.5L", "https://www.hdfcbank.com/personal/parivartan"),
        
        # INTERNSHIPS
        ("internship", "Government", "AICTE National Internship Portal", "AICTE, Govt. of India", 
         "UG & Engineering Students", "Varies per role", "July–November 2026", "DRDO, ISRO & Govt. Agencies", "https://internship.aicte-india.org"),
        
        ("internship", "Central", "PM Internship Scheme 3.0", "Govt. of India", 
         "Passed 10/12, ITI, Diploma, UG", "₹9,000/month", "Ongoing", "1 Crore youth coverage target", "https://pminternship.mca.gov.in"),

        # HACKATHONS
        ("hackathon", "Cyber", "Indian Army Terrier Cyber Quest 2026", "Indian Army × CyberPeace", 
         "Open for all college students", "Certificates, Cash & Defence Exposure", "31 August 2026", "Bug Hunting (CTF) & AI Kavach", "https://terriercyberquest.in"),
        
        ("hackathon", "Space", "ISRO Bharatiya Antariksh Hackathon 2026", "ISRO × Hack2skill", 
         "UG/PG/PhD in teams of 3-4", "ISRO Mentorship & Internship", "1 July 2026", "15 space & climate challenges", "https://hack2skill.com"),

        # WORKSHOPS
        ("workshop", "Design Thinking", "Samsung Solve for Tomorrow 2026", "Samsung India", 
         "Age 14–22 years", "Certificates & Incubation", "3 July 2026", "100+ cities nationwide", "https://www.samsung.com/in/solvefortomorrow"),

        # COMPETITIONS
        ("competition", "Automotive", "National Automobile Olympiad 2026", "ASDC", 
         "School & College Students", "National Ranking & Trophies", "August–September 2026", "35 MCQs · 35 minutes", "https://nao.asdc.org.in"),

        # GOVERNMENT SCHEMES
        ("government", "Women", "Karnataka Deepika Scholarship 2026–27", "Karnataka Higher Education Dept.", 
         "Girl students in govt. schools", "₹30,000/year", "31 August 2026", "For 51,399 girl students", "https://www.karnataka.gov.in")
    ]

    cursor.executemany('''
        INSERT INTO opportunities (category, tag, title, organization, eligibility, amount, deadline, details, apply_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', starter_items)

    conn.commit()
    conn.close()
    print(" Sample data seeded successfully into opphub.db!")

if __name__ == '__main__':
    seed_data()