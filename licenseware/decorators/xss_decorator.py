import re
from flask import request
from functools import wraps
from licenseware.utils.logger import log
from licenseware.utils.miscellaneous import get_flask_request_dict
from licenseware.common.constants import states




def xss_validator(request_dict: dict):
    """
    https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html#introduction

    Prevent XSS by not allowing any of the following values to pass:

    Condition which triggers xss evaluation:

    `If string has < or > present then look for posible XSS attacks`

    Checks:
    - any HTTP-EQUIV=XXXX with a folowup of charset=XXXXXX
    - any onXXX=XX which may include a event trigger
    - javascript: in any shape
    - any tag with SRC=XX 
    - any a, script, img, iframe, FRAMESET, EMBED, svg, input tags
    - href=XX
    - any html comment tags <!-- XXXX --> and php tags <? php ?>
    - any alert(XXXX), confirm(XXXX), prompt(XXXX), eval(XXXX)

    """


    string = str(request_dict)

    # Safe if < or > not present (probably)
    if not re.search(r"<|>", string, re.I): return

    # string = "hTTP-EQUIV=XXXX with a folowup of charset=XXXXXX"
    if re.search(r"HTTP-EQUIV\s{0,}=\s{0,}.*charset\s{0,}=\s{0,}.*", string, re.I):
        raise Exception("Attempt at changing page charset!")

    # string = "onclick = alert(XXXX);"
    if re.search(r"on.{1,}\s{0,}=\s{0,}.{1,}", string, re.I):
        raise Exception("Attempt at adding dom events!")

    # string="JavaSCript: alert(x)"
    if re.search(r"javascript\s{0,}:\s{0,}.{1,}", string, re.I):
        raise Exception("Attempt at adding dom events!")

    # string="SRC=XX"
    if re.search(r"src\s{0,}=\s{0,}.{1,}", string, re.I):
        raise Exception("Attempt at adding dom events!")

    # string="a script img iframe, FRAMESET, EMBED, svg, input"
    if re.search(r"a\s{1,}|script\s{1,}|img\s{1,}|iframe\s{1,}|frameset\s{1,}|embed\s{1,}|svg\s{1,}|input\s{1,}", string, re.I):
        raise Exception("Attempt at adding dom events!")

    # string="href=XX"
    if re.search(r"href\s{0,}=\s{0,}.{1,}", string, re.I):
        raise Exception("Attempt at adding dom events!")

    # string="<!-- XXXX --> <? php ?>"
    if re.search(r"<!--.*-->|<\?.*\?>", string, re.I):
        raise Exception("Attempt at adding dom events!")

    # string="alert(XXXX), confirm(XXXX), prompt(XXXX), eval(XXXX)"
    if re.search(r"alert\(.*\)|confirm\(.*\)|prompt\(.*\)|eval\(.*\)", string, re.I):
        raise Exception("Attempt at adding dom events!")



def xss_security(f):
    """ 
        Don't allow users to insert maliciuous data 
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        request_dict = get_flask_request_dict(request)

        try:
            xss_validator(request_dict)
            return f(*args, **kwargs)
        except:    
            log.warning(f'XSS ATTEMPT | Request headers: {dict(request.headers)} | URL {request.url} | Message: {request_dict}')
            return {'status': states.FAILED, 'message': "These inputs are not allowed"}, 406
        
    return decorated
