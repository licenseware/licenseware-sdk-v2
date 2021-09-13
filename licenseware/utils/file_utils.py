import os, re
import shutil
from werkzeug.utils import secure_filename as werkzeug_secure_filename
from licenseware.common.constants import envs



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

    # dir_id = generate_id() # doing this to avoid overwriting already uploaded files 
    # dir_id works only for uploaders with one file sent for processing
    save_path = path or os.path.join(envs.FILE_UPLOAD_PATH, tenant_id)
    if not os.path.exists(save_path): os.makedirs(save_path) 
    
    file.seek(0)  # move cursor to 0 (stream left it on last read)
    file_path = os.path.join(save_path, filename)
    file.save(file_path)
    file.close()
    
    return file_path



def unzip(file_path:str):

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



def recursive_unzip(file_path:str):
    """
        Iterate over an archive and recursively extract all archives using unzip function
    """
    
    if os.path.exists(file_path + '_extracted'):
        unziped_base = file_path + '_extracted'
    elif file_path.endswith(('.zip', '.tar.bz2')):
        unziped_base = unzip(file_path)
    
    for root, dirs, filenames in os.walk(unziped_base):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if not os.path.exists(file_path): continue
            if file_path.endswith(('.zip', '.tar.bz2')):
                unzip(file_path)
                os.remove(file_path)
                recursive_unzip(file_path)
            
    return unziped_base