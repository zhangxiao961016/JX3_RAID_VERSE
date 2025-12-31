import sqlite3
import hashlib
import pandas as pd
from datetime import date, timedelta

DB_FILE = "jx3_verse_v2.db"


def _get_conn():
    return sqlite3.connect(DB_FILE)


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def init_db():
    conn = _get_conn()
    c = conn.cursor()

    # 1. 用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT '侠士', 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. 角色表 (新增：用于管理用户的账号列表)
    c.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            sect TEXT, -- 门派
            server TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            UNIQUE(user_id, name) -- 防止同个用户创建重名角色
        )
    ''')

    # 3. 账本表
    c.execute('''
        CREATE TABLE IF NOT EXISTS raids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            raid_date TEXT,
            dungeon_type TEXT,
            salary INTEGER,
            character_name TEXT,
            expenditure INTEGER DEFAULT 0,
            is_special INTEGER DEFAULT 0,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # 自动迁移逻辑 (略，保持之前的即可，这里重点是characters表)
    conn.commit()
    conn.close()


# ... (User相关函数不变) ...
def create_user(username, password, role):
    conn = _get_conn()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users(username, password, role) VALUES (?,?,?)', (username, make_hashes(password), role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username =? AND password = ?', (username, make_hashes(password)))
    data = c.fetchall()
    conn.close()
    return data


# --- 账本相关 ---
def add_raid_record(user_id, raid_date, dungeon_type, salary, char_name, expenditure, is_special, note):
    conn = _get_conn()
    c = conn.cursor()

    # 自动逻辑：如果记账时输入了一个新名字，自动把它加入到 characters 表中
    # 这样用户就不用先去建角色再记账了，体验更好
    try:
        c.execute("INSERT OR IGNORE INTO characters (user_id, name, sect) VALUES (?, ?, ?)",
                  (user_id, char_name, '未知'))
    except:
        pass

    special_int = 1 if is_special else 0
    c.execute("""
        INSERT INTO raids (user_id, raid_date, dungeon_type, salary, character_name, expenditure, is_special, note) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, raid_date, dungeon_type, salary, char_name, expenditure, special_int, note))
    conn.commit()
    conn.close()


def get_user_stats(user_id):
    conn = _get_conn()
    df = pd.read_sql_query("SELECT * FROM raids WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    if df.empty: return 0, 0, 0, 0, pd.DataFrame()
    return df['salary'].sum(), df['expenditure'].sum(), df['is_special'].sum(), len(df), df


def get_character_stats_by_user(user_id):
    conn = _get_conn()
    query = """
        SELECT character_name as '角色', SUM(salary) as '总收入', SUM(expenditure) as '总支出', SUM(is_special) as '特殊掉落', COUNT(*) as '打本次数'
        FROM raids WHERE user_id = ? GROUP BY character_name ORDER BY SUM(salary) DESC
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    if df.empty: return pd.DataFrame(columns=['角色', '总收入', '总支出', '特殊掉落', '打本次数'])
    df['角色'] = df['角色'].fillna('侠士')
    return df


# --- 角色管理相关 (新增) ---

def get_all_characters(user_id):
    """获取用户的所有角色列表"""
    conn = _get_conn()
    df = pd.read_sql_query("SELECT * FROM characters WHERE user_id = ? ORDER BY created_at DESC", conn,
                           params=(user_id,))
    conn.close()
    return df


def delete_character(char_id, user_id):
    """删除角色 (注意：这只删角色列表，不删账本记录，防止误删导致账平不了)"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM characters WHERE id = ? AND user_id = ?", (char_id, user_id))
    conn.commit()
    conn.close()


def add_character_manual(user_id, name, sect):
    conn = _get_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO characters (user_id, name, sect) VALUES (?, ?, ?)", (user_id, name, sect))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_single_character_details(user_id, char_name):
    """获取单个角色的详细账单"""
    conn = _get_conn()
    df = pd.read_sql_query("SELECT * FROM raids WHERE user_id = ? AND character_name = ? ORDER BY raid_date DESC",
                           conn, params=(user_id, char_name))
    conn.close()
    return df