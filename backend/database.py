# backend/database.py
"""
SQLite database setup and seed data for LawBot 2.0.
Handles lawyers and consultation_requests tables.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "lawbot.db"


def get_db() -> sqlite3.Connection:
    """Get a database connection with row factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create tables and seed data if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    # Create lawyers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lawyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            location TEXT NOT NULL,
            languages TEXT NOT NULL,
            experience_years INTEGER NOT NULL,
            profile TEXT NOT NULL,
            contact TEXT NOT NULL,
            availability TEXT NOT NULL DEFAULT 'Available'
        )
    """)

    # Create consultation_requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultation_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            legal_issue TEXT NOT NULL,
            preferred_language TEXT,
            preferred_date TEXT,
            contact_info TEXT NOT NULL,
            description TEXT,
            lawyer_id INTEGER,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lawyer_id) REFERENCES lawyers(id)
        )
    """)

    # Seed lawyers if table is empty
    cursor.execute("SELECT COUNT(*) FROM lawyers")
    count = cursor.fetchone()[0]

    if count == 0:
        seed_lawyers = [
            (
                "Adv. Rajesh Sharma",
                "Criminal Law",
                "Mumbai, Maharashtra",
                "Hindi, English, Marathi",
                18,
                "Senior criminal lawyer specializing in criminal trials, bail matters, "
                "white-collar crimes, and FIR quashing. Has represented clients in the "
                "Bombay High Court and various Sessions Courts across Maharashtra. Known "
                "for his thorough case preparation and persuasive courtroom arguments.",
                "+91 98231 44567",
                "Available",
            ),
            (
                "Adv. Priya Mehta",
                "Family Law",
                "Ahmedabad, Gujarat",
                "Hindi, English, Gujarati",
                12,
                "Experienced family law practitioner handling divorce cases, child custody "
                "disputes, domestic violence matters, and matrimonial mediation. Advocates "
                "for amicable resolution and has a strong track record in negotiated settlements.",
                "+91 90995 88772",
                "Available",
            ),
            (
                "Adv. Arjun Verma",
                "Cyber Law",
                "Bengaluru, Karnataka",
                "Hindi, English, Kannada",
                9,
                "Technology law specialist handling cyber fraud, online harassment, hacking "
                "disputes, data protection cases, and IT Act matters. Formerly worked with "
                "a leading tech company's legal team before starting independent practice.",
                "+91 97455 22110",
                "Available",
            ),
            (
                "Adv. Neha Kulkarni",
                "Corporate Law",
                "Pune, Maharashtra",
                "Hindi, English, Marathi",
                14,
                "Corporate law expert specializing in business contracts, mergers and "
                "acquisitions, startup compliance, SEBI regulations, and corporate governance. "
                "Has advised over 50 startups on incorporation and compliance matters.",
                "+91 88067 43012",
                "Available",
            ),
            (
                "Adv. Sandeep Reddy",
                "Property Law",
                "Hyderabad, Telangana",
                "Hindi, English, Telugu",
                11,
                "Property and real estate law specialist handling property disputes, title "
                "verification, registration matters, RERA compliance, and land acquisition "
                "cases. Extensive experience with revenue court proceedings.",
                "+91 99895 11234",
                "Available",
            ),
            (
                "Adv. Kavitha Nair",
                "Constitutional Law",
                "Thiruvananthapuram, Kerala",
                "Hindi, English, Malayalam",
                20,
                "Constitutional law expert with two decades of experience in fundamental "
                "rights litigation, PIL matters, and administrative law. Has appeared before "
                "the Kerala High Court in several landmark cases.",
                "+91 94470 33891",
                "Available",
            ),
            (
                "Adv. Mohit Gupta",
                "Labour Law",
                "Delhi, NCR",
                "Hindi, English, Punjabi",
                15,
                "Labour and employment law specialist handling industrial disputes, wrongful "
                "termination cases, workplace harassment claims, and compliance with labour "
                "codes. Represents both employers and employees.",
                "+91 98110 67234",
                "Available",
            ),
            (
                "Adv. Deepa Iyer",
                "Consumer Law",
                "Chennai, Tamil Nadu",
                "Hindi, English, Tamil",
                8,
                "Consumer rights advocate specializing in consumer complaints, product "
                "liability, unfair trade practices, and e-commerce disputes. Has successfully "
                "handled cases before District, State, and National Consumer Forums.",
                "+91 98410 55678",
                "Available",
            ),
            (
                "Adv. Vikram Singh",
                "Criminal Law",
                "Jaipur, Rajasthan",
                "Hindi, English, Rajasthani",
                22,
                "Veteran criminal defense lawyer with over two decades of experience in "
                "serious criminal matters including murder trials, NDPS cases, and economic "
                "offences. Known for meticulous cross-examination skills.",
                "+91 94140 78901",
                "Available",
            ),
            (
                "Adv. Ananya Das",
                "Intellectual Property Law",
                "Kolkata, West Bengal",
                "Hindi, English, Bengali",
                10,
                "IP law specialist handling trademark registration, patent filing, copyright "
                "disputes, and trade secret protection. Works with creative professionals, "
                "tech companies, and pharmaceutical firms on IP strategy.",
                "+91 98300 44567",
                "Available",
            ),
            (
                "Adv. Rahul Joshi",
                "Tax Law",
                "Pune, Maharashtra",
                "Hindi, English, Marathi",
                16,
                "Tax law expert specializing in income tax disputes, GST compliance, tax "
                "planning, and representation before Income Tax Appellate Tribunal. Formerly "
                "worked with a Big Four accounting firm.",
                "+91 90280 33456",
                "Busy",
            ),
            (
                "Adv. Shalini Verma",
                "Family Law",
                "Delhi, NCR",
                "Hindi, English, Urdu",
                13,
                "Family law practitioner focusing on matrimonial disputes, maintenance claims, "
                "domestic violence cases, and child welfare matters. Active member of the "
                "Delhi Mediation Centre for family dispute resolution.",
                "+91 98710 22345",
                "Available",
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO lawyers (name, specialization, location, languages,
                                 experience_years, profile, contact, availability)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            seed_lawyers,
        )
        print(f"[database] Seeded {len(seed_lawyers)} lawyers.")

    conn.commit()
    conn.close()
    print(f"[database] Database ready at: {DB_PATH}")


def dict_from_row(row: sqlite3.Row) -> dict:
    """Convert a sqlite3.Row to a plain dict."""
    return dict(row)
