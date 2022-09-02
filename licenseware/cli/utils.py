import os
import random
import re


def get_random_int():
    return random.randint(10, 99)


def get_env_value(envkey: str):

    if os.path.exists("./deploy/.env.debug"):
        envfile = "./deploy/.env.debug"
    elif os.path.exists("./tox.ini"):
        envfile = "./tox.ini"
    else:
        raise Exception("Neither ./deploy/.env.debug or ./tox.ini file was found")

    with open(envfile, "r") as f:
        data = f.read()

    m = re.search(r".*" + envkey + r"=(.+).*", data)
    if not m:
        raise Exception(f"{envkey} not found in ./deploy/.env.debug or ./tox.ini")

    return m.group(1)
