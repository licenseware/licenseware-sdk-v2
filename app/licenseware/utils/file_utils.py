import os, re
import string, random
import shutil
from werkzeug.utils import secure_filename as werkzeug_secure_filename
from app.licenseware.common.constants import envs



generate_dir_id = lambda : "".join([random.choice(list(string.digits)) for _ in range(6)])



def secure_filename(fname):
    """
        Custom handling of secure filename 
        Added an exception for review lite files `~` char
    """
    
    review_lite_file = re.search(r"feature|option|version", fname, re.IGNORECASE)
    
    if review_lite_file: fname = re.sub('~', '_SECURE_TILDA_', fname)
    
    fname = werkzeug_secure_filename(fname)
    
    if review_lite_file: fname = re.sub('_SECURE_TILDA_', '~', fname)
    
    return fname



def save_file(file, tenant_id=None, path=None):
    """
        Save to disk flask file stream
        
    """
    
    filename = secure_filename(file.filename)

    dir_id = generate_dir_id() # doing this to avoid overwriting already uploaded files 
    save_path = path or os.path.join(envs.FILE_UPLOAD_PATH, tenant_id, dir_id)
    if not os.path.exists(save_path): os.makedirs(save_path) 
    
    file.seek(0)  # move cursor to 0 (stream left it on last read)
    file_path = os.path.join(save_path, filename)
    file.save(file_path)
    
    return file_path



def unzip(file_path):

    """
        Extracts: “zip”, “tar”, “gztar”, “bztar”, or “xztar”.    
        Returns the path where the file was extracted
    """

    if not file_path.endswith(('.zip', '.tar.bz2')):
        return file_path
        
    file_name = os.path.basename(file_path)
    file_dir  = os.path.dirname(file_path)

    extract_path = os.path.join(file_dir, file_name + "_extracted")
    
    shutil.unpack_archive(file_path, extract_path)
    
    return extract_path



def get_filepaths_from_event(event):
    """
        :event - redis event similar to the one bellow:
            event = {
                'tenant_id': '2ac111c7-fd19-463e-96c2-1493aea18bed', 
                'files': 'filename1,filename2',
                'event_type': 'ofmw_archive' # for normalization purposes 'event_type' is the same as 'unit_type' and 'file_type'
            }

        returns a list of filepaths or list of folder paths if an archive is found in 'files' 

    """

    filepath = lambda filename: os.path.join(envs.FILE_UPLOAD_PATH, event['tenant_id'], filename)
    filenames = event['files'].split(",")

    return [unzip(filepath(filename)) for filename in filenames]




