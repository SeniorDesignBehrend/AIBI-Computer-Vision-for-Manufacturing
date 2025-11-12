"""Local data persistence for scan events and logs."""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class DataStorage:
    """Handles local storage of scan events and system logs."""
    
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scan_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workstation_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    synced INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    workstation_id TEXT,
                    timestamp TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_scan_events_workstation 
                ON scan_events(workstation_id)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_scan_events_synced 
                ON scan_events(synced)
            """)
            
            conn.commit()
    
    def store_scan_event(self, payload: Dict[str, Any]) -> int:
        """Store a scan event locally."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """INSERT INTO scan_events (workstation_id, timestamp, payload)
                   VALUES (?, ?, ?)""",
                (payload["workstation_id"], payload["timestamp"], json.dumps(payload))
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_unsynced_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve unsynced scan events for downstream synchronization."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT id, payload FROM scan_events 
                   WHERE synced = 0 
                   ORDER BY created_at ASC 
                   LIMIT ?""",
                (limit,)
            )
            return [
                {"id": row[0], "payload": json.loads(row[1])}
                for row in cursor.fetchall()
            ]
    
    def mark_synced(self, event_ids: List[int]):
        """Mark events as synced with downstream system."""
        with sqlite3.connect(self.db_path) as conn:
            placeholders = ",".join("?" * len(event_ids))
            conn.execute(
                f"UPDATE scan_events SET synced = 1 WHERE id IN ({placeholders})",
                event_ids
            )
            conn.commit()
    
    def log_event(self, level: str, message: str, workstation_id: Optional[str] = None):
        """Log a system event."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO system_logs (level, message, workstation_id, timestamp)
                   VALUES (?, ?, ?, ?)""",
                (level, message, workstation_id, datetime.now().isoformat())
            )
            conn.commit()
    
    def get_recent_logs(self, limit: int = 100, level: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve recent system logs."""
        with sqlite3.connect(self.db_path) as conn:
            if level:
                cursor = conn.execute(
                    """SELECT level, message, workstation_id, timestamp 
                       FROM system_logs 
                       WHERE level = ?
                       ORDER BY created_at DESC 
                       LIMIT ?""",
                    (level, limit)
                )
            else:
                cursor = conn.execute(
                    """SELECT level, message, workstation_id, timestamp 
                       FROM system_logs 
                       ORDER BY created_at DESC 
                       LIMIT ?""",
                    (limit,)
                )
            
            return [
                {
                    "level": row[0],
                    "message": row[1],
                    "workstation_id": row[2],
                    "timestamp": row[3]
                }
                for row in cursor.fetchall()
            ]
