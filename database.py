import sqlite3
import json
from contextlib import contextmanager

DATABASE = 'bilibili_videos.db'

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

def initialize_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 创建 videos 表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bvid TEXT UNIQUE,
            aid INTEGER,
            title TEXT,
            description TEXT,
            desc_v2 TEXT,
            tid INTEGER,
            tname TEXT,
            copyright INTEGER,
            pic TEXT,
            pubdate INTEGER,
            ctime INTEGER,
            duration INTEGER,
            rights TEXT,
            owner_mid INTEGER,
            owner_name TEXT,
            owner_face TEXT,
            stat TEXT,
            dynamic TEXT,
            dimension_width INTEGER,
            dimension_height INTEGER,
            dimension_rotate INTEGER,
            season_id INTEGER,
            premiere TEXT,
            teenage_mode INTEGER,
            is_chargeable_season BOOLEAN,
            is_story BOOLEAN,
            is_upower_exclusive BOOLEAN,
            is_upower_play BOOLEAN,
            enable_vt INTEGER,
            vt_display TEXT,
            no_cache BOOLEAN,
            url TEXT
        )
        """)

        # 创建 analysis_results 表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            analysis_text TEXT,
            FOREIGN KEY(video_id) REFERENCES videos(bvid)
        )
        """)
        conn.commit()
