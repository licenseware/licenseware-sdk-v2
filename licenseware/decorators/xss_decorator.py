import re
from functools import wraps

from flask import request

from licenseware.common.constants import states
from licenseware.utils.logger import log
from licenseware.utils.miscellaneous import get_flask_request_dict


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
    if not re.search(r"<|>", string, re.I):
        return

    # string = "hTTP-EQUIV=XXXX with a folowup of charset=XXXXXX"
    charset_change = re.search(
        r"HTTP-EQUIV\s{0,}=\s{0,}.*charset\s{0,}=\s{0,}.*", string, re.I
    )
    if charset_change:
        raise Exception(
            f"1.Attempt at changing page charset on: {charset_change.group()}"
        )

    # string = "onclick = alert(XXXX);"
    onchange_event = re.search(r"on.{1,}\s{0,}=\s{0,}.{1,}", string, re.I)
    if onchange_event:
        raise Exception(f"2.Attempt at adding js events on: {onchange_event.group()}")

    # string="JavaSCript: alert(x)"
    jsonchange_event = re.search(r"javascript\s{0,}:\s{0,}.{1,}", string, re.I)
    if jsonchange_event:
        raise Exception(f"3.Attempt at adding js events on: {jsonchange_event.group()}")

    # string="SRC=XX"
    js_script = re.search(r"src\s{0,}=\s{0,}.{1,}", string, re.I)
    if js_script:
        raise Exception(
            f"4.Attempt at adding inserting a js script on: {js_script.group()}"
        )

    # string="a script img iframe, FRAMESET, EMBED, svg, input"
    mjs_script = re.search(
        r"a\s{1,}|script\s{1,}|img\s{1,}|iframe\s{1,}|frameset\s{1,}|embed\s{1,}|svg\s{1,}|input\s{1,}",
        string,
        re.I,
    )
    if mjs_script:
        raise Exception(
            f"5.Attempt at adding inserting a script on: {mjs_script.group()}"
        )

    # string="href=XX"
    link = re.search(r"href\s{0,}=\s{0,}.{1,}", string, re.I)
    if link:
        raise Exception(f"6.Attempt at adding a malicious link at: {link.group()}")

    # string="<!-- XXXX --> <? php ?>"
    comments = re.search(r"<!--.*-->|<\?.*\?>", string, re.I)
    if comments:
        raise Exception(
            f"7.Attempt at adding js script inside comments on: {comments.group()}"
        )

    # string="alert(XXXX), confirm(XXXX), prompt(XXXX), eval(XXXX)"
    js_alerts = re.search(
        r"alert\(.*\)|confirm\(.*\)|prompt\(.*\)|eval\(.*\)", string, re.I
    )
    if js_alerts:
        raise Exception(f"8.Attempt at adding js dialog boxes on: {js_alerts.group()}")


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
        except Exception as err:
            log.warning(
                f"XSS ATTEMPT | Request headers: {dict(request.headers)} | URL {request.url} | Message: {request_dict}"
            )
            return {
                "status": states.FAILED,
                "message": "These inputs are not allowed (posible XSS)",
                "reason": str(err),
            }, 406

    return decorated


def xss_before_request():

    request_dict = get_flask_request_dict(request)

    try:
        xss_validator(request_dict)
    except Exception as err:
        log.warning(
            f"XSS ATTEMPT | Request headers: {dict(request.headers)} | URL {request.url} | Message: {request_dict}"
        )
        return {
            "status": states.FAILED,
            "message": "These inputs are not allowed (posible XSS)",
            "reason": str(err),
        }, 406
