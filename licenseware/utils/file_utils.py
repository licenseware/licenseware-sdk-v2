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
        raise ValueError("Only '.zip', '.tar.bz2' archives are accepted")
        
    file_name = os.path.basename(file_path)
    file_dir  = os.path.dirname(file_path)

    extract_path = os.path.join(file_dir, file_name + "_extracted")
    
    shutil.unpack_archive(file_path, extract_path)
    
    return extract_path



def recursive_unzip(file_path:str):
    """
        Iterate over an archive and recursively extract all archives using unzip function
    """
 
    if file_path.endswith(('.zip', '.tar.bz2')):
        unziped_base = unzip(file_path)
    else:
        unziped_base = file_path
    
    archives_found = False
    for root, dirs, filenames in os.walk(unziped_base):
        for filename in filenames:
            
            fpath = os.path.join(root, filename)
            
            if not fpath.endswith(('.zip', '.tar.bz2')): continue
            if not os.path.exists(fpath): continue
            
            unzip(fpath)
            os.remove(fpath)
            archives_found = True
    
    file_path = file_path + '_extracted' if not file_path.endswith('_extracted') else file_path
    
    if archives_found: 
        recursive_unzip(file_path)    
        
    return file_path
    
