import os
import json
from langchain_community.document_loaders import BiliBiliLoader
from database import get_db_connection, initialize_database
from langchain.docstore.document import Document

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 从环境变量获取 BiliBiliLoader 所需的参数
SESSDATA = os.getenv("SESSDATA")
BUVID3 = os.getenv("BUVID3")
BILI_JCT = os.getenv("BILI_JCT")

def gather_bilibili_data(urls):
    """
    根据给定的 Bilibili 视频 URL 列表，获取视频信息并存储到数据库中
    """
    loader = BiliBiliLoader(
        video_urls=urls,
        sessdata=SESSDATA,
        buvid3=BUVID3,
        bili_jct=BILI_JCT
    )
    documents = loader.load()
    
    for doc in documents:
        insert_video_into_db(doc)

def insert_video_into_db(document: Document):
    """
    将单个 Document 对象中的视频信息插入到数据库中
    """
    try:
        metadata = document.metadata
        # 处理复杂字段（例如 dict 类型的字段，需要转换为 JSON 字符串）
        desc_v2 = json.dumps(metadata.get('desc_v2', []))
        rights = json.dumps(metadata.get('rights', {}))
        stat = json.dumps(metadata.get('stat', {}))
        dimension = metadata.get('dimension', {})
        owner = metadata.get('owner', {})
        argue_info = metadata.get('argue_info', {})
        ugc_season = metadata.get('ugc_season', {})
        honor_reply = metadata.get('honor_reply', {})
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO videos (
                    bvid, aid, title, description, desc_v2, tid, tname, copyright,
                    pic, pubdate, ctime, duration, rights, owner_mid, owner_name,
                    owner_face, stat, dynamic, dimension_width, dimension_height,
                    dimension_rotate, season_id, premiere, teenage_mode,
                    is_chargeable_season, is_story, is_upower_exclusive, is_upower_play,
                    enable_vt, vt_display, no_cache, url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    metadata.get('bvid'),
                    metadata.get('aid'),
                    metadata.get('title'),
                    metadata.get('desc'),
                    desc_v2,
                    metadata.get('tid'),
                    metadata.get('tname'),
                    metadata.get('copyright'),
                    metadata.get('pic'),
                    metadata.get('pubdate'),
                    metadata.get('ctime'),
                    metadata.get('duration'),
                    rights,
                    owner.get('mid'),
                    owner.get('name'),
                    owner.get('face'),
                    stat,
                    metadata.get('dynamic'),
                    dimension.get('width'),
                    dimension.get('height'),
                    dimension.get('rotate'),
                    metadata.get('season_id'),
                    metadata.get('premiere'),
                    metadata.get('teenage_mode'),
                    metadata.get('is_chargeable_season'),
                    metadata.get('is_story'),
                    metadata.get('is_upower_exclusive'),
                    metadata.get('is_upower_play'),
                    metadata.get('enable_vt'),
                    metadata.get('vt_display'),
                    metadata.get('no_cache'),
                    metadata.get('url')
                )
            )
            conn.commit()
            print(f"视频 {metadata.get('bvid')} 已入库。")
    except Exception as e:
        print(f"插入视频 {document.metadata.get('bvid')} 时出错: {e}")
