"""Seed the AIS monitoring schema with representative sample data.

This script connects to a PostgreSQL database using credentials supplied via
environment variables and inserts a cohesive dataset across the users,
vessels, monitoring_areas, incidents, comments, and weather_alerts tables.

Environment variables:
    PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD, PGSSLMODE

Example:
    export PGUSER="neondb_owner"
    export PGPASSWORD="..."
    export PGHOST="..."
    export PGPORT="5432"
    export PGDATABASE="neondb"
    python seed_data.py
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

NOW = datetime.utcnow().replace(microsecond=0)


USERS = [
    {
        "id": "0f8fefcc-9cc2-4dc4-a339-d98c024aaa0d",
        "email": "amy.chen@harborwatch.test",
        "first_name": "Amy",
        "last_name": "Chen",
        "profile_image_url": "https://cdn.example.com/profiles/amy-chen.jpg",
        "role": "operator",
        "unit": "Pacific Watch",
        "created_at": NOW - timedelta(days=90),
        "updated_at": NOW - timedelta(days=2),
    },
    {
        "id": "5c3c1f0a-6ea8-4f21-b027-08c3790fb70d",
        "email": "marco.alvarez@harborwatch.test",
        "first_name": "Marco",
        "last_name": "Alvarez",
        "profile_image_url": "https://cdn.example.com/profiles/marco-alvarez.jpg",
        "role": "supervisor",
        "unit": "Northern Command",
        "created_at": NOW - timedelta(days=120),
        "updated_at": NOW - timedelta(days=1, hours=6),
    },
    {
        "id": "f0daae2a-00f7-43d7-82e0-1e9465d9b387",
        "email": "lena.ramirez@harborwatch.test",
        "first_name": "Lena",
        "last_name": "Ramirez",
        "profile_image_url": "https://cdn.example.com/profiles/lena-ramirez.jpg",
        "role": "analyst",
        "unit": "Intelligence Unit",
        "created_at": NOW - timedelta(days=75),
        "updated_at": NOW - timedelta(hours=12),
    },
    {
        "id": "2b93a9eb-2924-4b03-9a36-5a12dd0bafcd",
        "email": "hassan.omer@harborwatch.test",
        "first_name": "Hassan",
        "last_name": "Omer",
        "profile_image_url": "https://cdn.example.com/profiles/hassan-omer.jpg",
        "role": "coordinator",
        "unit": "Search & Rescue",
        "created_at": NOW - timedelta(days=60),
        "updated_at": NOW - timedelta(days=5),
    },
]


MONITORING_AREAS = [
    {
        "id": "6c6c8baf-58b0-4b0a-9b40-d0fa008b4a1f",
        "name": "Northwest Approaches",
        "north_bound": 49.5,
        "south_bound": 47.8,
        "east_bound": -122.1,
        "west_bound": -125.4,
        "created_by_id": "5c3c1f0a-6ea8-4f21-b027-08c3790fb70d",
        "created_at": NOW - timedelta(days=45),
    },
    {
        "id": "de927f1c-3b8f-4ae9-a479-f9d8d8196fd7",
        "name": "Outer Sound Corridor",
        "north_bound": 48.9,
        "south_bound": 47.2,
        "east_bound": -122.3,
        "west_bound": -123.8,
        "created_by_id": "0f8fefcc-9cc2-4dc4-a339-d98c024aaa0d",
        "created_at": NOW - timedelta(days=38),
    },
    {
        "id": "5fa91f5a-50d9-4ef5-a0c6-879f6f5970c0",
        "name": "Coastal Drift Monitoring Zone",
        "north_bound": 47.9,
        "south_bound": 46.4,
        "east_bound": -123.1,
        "west_bound": -125.0,
        "created_by_id": "2b93a9eb-2924-4b03-9a36-5a12dd0bafcd",
        "created_at": NOW - timedelta(days=27),
    },
]


VESSELS = [
    {
        "id": "2db4d51d-ff6b-4b62-a846-5cb7ad863246",
        "name": "MV Horizon Star",
        "call_sign": "WDS1234",
        "mmsi": "366998201",
        "vessel_type": "cargo",
        "length": 182.5,
        "draft": 9.4,
        "destination": "Port of Seattle",
        "current_latitude": 48.112,
        "current_longitude": -122.745,
        "speed": 12.8,
        "heading": 87.0,
        "status": "normal",
        "last_contact": NOW - timedelta(minutes=15),
        "created_at": NOW - timedelta(days=50),
        "updated_at": NOW - timedelta(hours=3),
    },
    {
        "id": "a03c0580-5a53-4e7a-9b33-5ac4a1cf6a45",
        "name": "FV Pacific Dawn",
        "call_sign": "WDF4432",
        "mmsi": "367015490",
        "vessel_type": "fishing",
        "length": 34.7,
        "draft": 3.1,
        "destination": "Kodiak Harbor",
        "current_latitude": 47.936,
        "current_longitude": -123.207,
        "speed": 8.5,
        "heading": 142.0,
        "status": "normal",
        "last_contact": NOW - timedelta(minutes=9),
        "created_at": NOW - timedelta(days=80),
        "updated_at": NOW - timedelta(hours=5),
    },
    {
        "id": "33dcfca8-ff5f-4a0f-8c0d-e0837873e7f0",
        "name": "R/V Ocean Explorer",
        "call_sign": "KLMN45",
        "mmsi": "367128980",
        "vessel_type": "research",
        "length": 72.0,
        "draft": 5.5,
        "destination": "Puget Sound Research Pier",
        "current_latitude": 48.298,
        "current_longitude": -122.982,
        "speed": 4.2,
        "heading": 310.0,
        "status": "maintenance",
        "last_contact": NOW - timedelta(hours=2, minutes=20),
        "created_at": NOW - timedelta(days=65),
        "updated_at": NOW - timedelta(days=1, hours=4),
    },
    {
        "id": "864f7f29-c2f6-4f88-8940-7b29fc6768c2",
        "name": "CS Coastal Guardian",
        "call_sign": "USCG201",
        "mmsi": "338998764",
        "vessel_type": "coast_guard",
        "length": 52.3,
        "draft": 4.8,
        "destination": "Search & Rescue Station 12",
        "current_latitude": 47.652,
        "current_longitude": -122.408,
        "speed": 22.1,
        "heading": 35.0,
        "status": "deployment",
        "last_contact": NOW - timedelta(minutes=4),
        "created_at": NOW - timedelta(days=40),
        "updated_at": NOW - timedelta(minutes=45),
    },
]


INCIDENTS = [
    {
        "id": "56dfc1c1-4e69-4dd0-9a1c-21cbcdd0b4db",
        "title": "Engine Overheat Alarm",
        "description": (
            "The main engine temperature aboard MV Horizon Star exceeded safe "
            "operating levels. Crew reduced speed and initiated cooling."),
        "incident_type": "mechanical",
        "priority": "high",
        "latitude": 48.105,
        "longitude": -122.752,
        "vessel_id": "2db4d51d-ff6b-4b62-a846-5cb7ad863246",
        "requires_attention": True,
        "weather_related": False,
        "status": "active",
        "reported_by_id": "0f8fefcc-9cc2-4dc4-a339-d98c024aaa0d",
        "created_at": NOW - timedelta(hours=6, minutes=10),
        "updated_at": NOW - timedelta(hours=1, minutes=5),
    },
    {
        "id": "8e3cbf8f-0f2c-4d90-9fa2-7bc4739be6ee",
        "title": "Suspicious Vessel Shadowing",
        "description": (
            "FV Pacific Dawn reported an unidentified vessel maintaining a "
            "parallel course for more than 30 minutes."),
        "incident_type": "security",
        "priority": "medium",
        "latitude": 47.942,
        "longitude": -123.198,
        "vessel_id": "a03c0580-5a53-4e7a-9b33-5ac4a1cf6a45",
        "requires_attention": True,
        "weather_related": False,
        "status": "monitoring",
        "reported_by_id": "5c3c1f0a-6ea8-4f21-b027-08c3790fb70d",
        "created_at": NOW - timedelta(hours=11, minutes=40),
        "updated_at": NOW - timedelta(hours=2, minutes=30),
    },
    {
        "id": "c6e7d08a-46f7-4b24-b879-7a0f56b0b8a9",
        "title": "Deckhand Injury",
        "description": (
            "Crew member aboard CS Coastal Guardian sustained a leg injury "
            "while deploying rescue equipment. Medical evacuation requested."),
        "incident_type": "medical",
        "priority": "critical",
        "latitude": 47.661,
        "longitude": -122.395,
        "vessel_id": "864f7f29-c2f6-4f88-8940-7b29fc6768c2",
        "requires_attention": True,
        "weather_related": False,
        "status": "active",
        "reported_by_id": "2b93a9eb-2924-4b03-9a36-5a12dd0bafcd",
        "created_at": NOW - timedelta(hours=1, minutes=25),
        "updated_at": NOW - timedelta(minutes=30),
    },
    {
        "id": "ec5d1631-39e0-4a40-963a-37cc78b73f5a",
        "title": "Rapid Weather Deterioration",
        "description": (
            "Research operations aboard R/V Ocean Explorer paused after wind "
            "gusts exceeded 40 knots and visibility dropped below one mile."),
        "incident_type": "weather",
        "priority": "high",
        "latitude": 48.301,
        "longitude": -122.975,
        "vessel_id": "33dcfca8-ff5f-4a0f-8c0d-e0837873e7f0",
        "requires_attention": False,
        "weather_related": True,
        "status": "resolved",
        "reported_by_id": "f0daae2a-00f7-43d7-82e0-1e9465d9b387",
        "created_at": NOW - timedelta(days=1, hours=3),
        "updated_at": NOW - timedelta(hours=19),
    },
]


COMMENTS = [
    {
        "id": "9c7dc0c1-7b60-41ee-a69a-96910f7ac0f4",
        "content": "Cooling pumps stabilized temperatures. Monitoring for recurrence.",
        "vessel_id": "2db4d51d-ff6b-4b62-a846-5cb7ad863246",
        "incident_id": "56dfc1c1-4e69-4dd0-9a1c-21cbcdd0b4db",
        "author_id": "0f8fefcc-9cc2-4dc4-a339-d98c024aaa0d",
        "created_at": NOW - timedelta(hours=4, minutes=52),
        "attachment_filename": None,
        "attachment_path": None,
        "attachment_mime_type": None,
    },
    {
        "id": "6c03ab8c-4dd5-4db8-8fd7-0b052fe4fa33",
        "content": "Thermal scan attached for engineering review.",
        "vessel_id": "2db4d51d-ff6b-4b62-a846-5cb7ad863246",
        "incident_id": "56dfc1c1-4e69-4dd0-9a1c-21cbcdd0b4db",
        "author_id": "f0daae2a-00f7-43d7-82e0-1e9465d9b387",
        "created_at": NOW - timedelta(hours=3, minutes=5),
        "attachment_filename": "engine-thermal-scan.png",
        "attachment_path": "s3://harborwatch/incidents/56dfc1c1/engine-thermal-scan.png",
        "attachment_mime_type": "image/png",
    },
    {
        "id": "ba6f87a5-32aa-4f25-9615-e748f23218d9",
        "content": "Coast Guard cutter dispatched to intercept suspicious vessel.",
        "vessel_id": "a03c0580-5a53-4e7a-9b33-5ac4a1cf6a45",
        "incident_id": "8e3cbf8f-0f2c-4d90-9fa2-7bc4739be6ee",
        "author_id": "5c3c1f0a-6ea8-4f21-b027-08c3790fb70d",
        "created_at": NOW - timedelta(hours=2, minutes=12),
        "attachment_filename": None,
        "attachment_path": None,
        "attachment_mime_type": None,
    },
    {
        "id": "43a8bcc8-a04a-4f58-9b7b-233394dd3c6f",
        "content": "Medical helicopter en route with ETA 15 minutes.",
        "vessel_id": "864f7f29-c2f6-4f88-8940-7b29fc6768c2",
        "incident_id": "c6e7d08a-46f7-4b24-b879-7a0f56b0b8a9",
        "author_id": "2b93a9eb-2924-4b03-9a36-5a12dd0bafcd",
        "created_at": NOW - timedelta(minutes=38),
        "attachment_filename": None,
        "attachment_path": None,
        "attachment_mime_type": None,
    },
    {
        "id": "dcf038f9-f8a9-4567-8d09-854db069c1da",
        "content": "Weather window improving; operations scheduled to resume at 0600Z.",
        "vessel_id": "33dcfca8-ff5f-4a0f-8c0d-e0837873e7f0",
        "incident_id": "ec5d1631-39e0-4a40-963a-37cc78b73f5a",
        "author_id": "f0daae2a-00f7-43d7-82e0-1e9465d9b387",
        "created_at": NOW - timedelta(hours=18),
        "attachment_filename": None,
        "attachment_path": None,
        "attachment_mime_type": None,
    },
]


WEATHER_ALERTS = [
    {
        "id": "d1bf827c-4c42-4f5f-b650-b7d8d1a1f5e4",
        "title": "Gale Warning - Strait of Juan de Fuca",
        "description": (
            "Sustained winds of 35-45 knots with higher gusts expected. Small "
            "craft should seek safe harbor."),
        "severity": "warning",
        "alert_type": "gale",
        "latitude": 48.3,
        "longitude": -124.1,
        "radius": 55.0,
        "is_active": True,
        "expires_at": NOW + timedelta(hours=12),
        "created_at": NOW - timedelta(hours=2),
    },
    {
        "id": "0c8b96cd-4f74-4f9a-9dd8-b2df7d63d8d9",
        "title": "Dense Fog Advisory - Admiralty Inlet",
        "description": (
            "Visibility less than 0.5 nautical miles through the morning. "
            "Radar navigation recommended."),
        "severity": "advisory",
        "alert_type": "fog",
        "latitude": 48.1,
        "longitude": -122.7,
        "radius": 30.0,
        "is_active": False,
        "expires_at": NOW - timedelta(hours=3),
        "created_at": NOW - timedelta(days=1, hours=6),
    },
]


DATASETS = [
    ("users", USERS),
    ("monitoring_areas", MONITORING_AREAS),
    ("vessels", VESSELS),
    ("incidents", INCIDENTS),
    ("comments", COMMENTS),
    ("weather_alerts", WEATHER_ALERTS),
]


def purge_existing(conn, table_name: str, ids: list[str]) -> None:
    """Delete any rows that would conflict with this seed dataset."""
    if not ids:
        return

    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("DELETE FROM {table} WHERE id = ANY(%s)").format(
                table=sql.Identifier(table_name)
            ),
            (ids,),
        )


def insert_rows(conn, table_name: str, rows: list[dict[str, object]]) -> None:
    """Bulk insert dictionaries into the specified table."""
    if not rows:
        return

    columns = list(rows[0].keys())
    values = [[row[column] for column in columns] for row in rows]

    with conn.cursor() as cur:
        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES %s").format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(", ").join(sql.Identifier(column) for column in columns),
        )
        execute_values(cur, query.as_string(cur), values)


def seed_table(conn, table_name: str, rows: list[dict[str, object]]) -> None:
    ids = [row["id"] for row in rows if "id" in row]
    purge_existing(conn, table_name, ids)
    insert_rows(conn, table_name, rows)
    print(f"Inserted {len(rows)} rows into {table_name}.")


def main() -> None:
    conn = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "postgres"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", ""),
        sslmode=os.getenv("PGSSLMODE", "require"),
    )

    try:
        with conn:
            for table_name, rows in DATASETS:
                seed_table(conn, table_name, rows)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
