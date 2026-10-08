# backend/lawyer_connect.py
"""
Lawyer Connect module for LawBot 2.0.
Provides API logic for lawyer search, profiles, and consultation requests.
"""

from backend.database import get_db, dict_from_row


def get_lawyers(
    specialization: str | None = None,
    location: str | None = None,
    language: str | None = None,
) -> list[dict]:
    """
    Get lawyers with optional filters.
    Filters are case-insensitive partial matches.
    """
    conn = get_db()
    query = "SELECT * FROM lawyers WHERE 1=1"
    params = []

    if specialization and specialization.lower() not in ("all", "all specializations", ""):
        query += " AND LOWER(specialization) LIKE LOWER(?)"
        params.append(f"%{specialization}%")

    if location and location.lower() not in ("all", "all locations", ""):
        query += " AND LOWER(location) LIKE LOWER(?)"
        params.append(f"%{location}%")

    if language and language.lower() not in ("all", "all languages", ""):
        query += " AND LOWER(languages) LIKE LOWER(?)"
        params.append(f"%{language}%")

    query += " ORDER BY experience_years DESC"

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict_from_row(r) for r in rows]


def get_lawyer_by_id(lawyer_id: int) -> dict | None:
    """Get a single lawyer by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM lawyers WHERE id = ?", (lawyer_id,)).fetchone()
    conn.close()
    return dict_from_row(row) if row else None


def create_consultation_request(data: dict) -> dict:
    """Create a new consultation request."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO consultation_requests
            (name, legal_issue, preferred_language, preferred_date,
             contact_info, description, lawyer_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["name"],
            data["legal_issue"],
            data.get("preferred_language", ""),
            data.get("preferred_date", ""),
            data["contact_info"],
            data.get("description", ""),
            data.get("lawyer_id"),
        ),
    )
    conn.commit()
    request_id = cursor.lastrowid
    conn.close()
    return {"id": request_id, "status": "Pending", "message": "Consultation request submitted successfully."}


def get_consultation_requests() -> list[dict]:
    """Get all consultation requests (for demo purposes)."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM consultation_requests ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict_from_row(r) for r in rows]


def get_filter_options() -> dict:
    """Get unique values for filter dropdowns."""
    conn = get_db()

    specs = conn.execute(
        "SELECT DISTINCT specialization FROM lawyers ORDER BY specialization"
    ).fetchall()
    locs = conn.execute(
        "SELECT DISTINCT location FROM lawyers ORDER BY location"
    ).fetchall()

    # Extract unique languages from comma-separated field
    lang_rows = conn.execute("SELECT languages FROM lawyers").fetchall()
    languages = set()
    for row in lang_rows:
        for lang in row["languages"].split(","):
            languages.add(lang.strip())

    conn.close()

    return {
        "specializations": [r["specialization"] for r in specs],
        "locations": [r["location"] for r in locs],
        "languages": sorted(languages),
    }
