import os
import re
import random


def get_random_int():
    return random.randint(1000, 9999)


def get_env_value(envkey: str):

    if os.path.exists(".env"):
        envfile = ".env"
    elif os.path.exists(".envlocal"):
        envfile = ".envlocal"
    elif os.path.exists("tox.ini"):
        envfile = "tox.ini"
    else:
        raise Exception("Neither .env, .envlocal or tox.ini file was found")
    
    with open(envfile, "r") as f:
        data = f.read() 
    
    m = re.search(r'.*' + envkey + r'=(.+).*', data)
    if not m: raise Exception(f"{envkey} not found in .env, .envlocal or tox.ini") 

    return m.group(1)