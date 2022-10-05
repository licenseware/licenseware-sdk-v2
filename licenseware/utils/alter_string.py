from dataclasses import asdict, dataclass


@dataclass
class AlteredStrVersions:
    original: str
    title: str
    title_joined: str
    dash: str
    dash_upper: str
    underscore: str
    underscore_upper: str

    def dict(self):  # pragma no cover
        return asdict(self)


def get_altered_strings(s: str):

    strli = s.strip().replace("-", "|").replace("_", "|").replace(".", "|").split("|")
    str_title = " ".join([v.capitalize() for v in strli])  # odb-service => Odb Service
    str_title_joined = "".join(
        [v.capitalize() for v in strli]
    )  # odb-service => OdbService
    str_dash = "-".join([v.lower() for v in strli])  # odb-service => odb-service
    str_dash_upper = "-".join([v.upper() for v in strli])  # odb-service => ODB-SERVICE
    str_underscore = "_".join([v.lower() for v in strli])  # odb-service => odb_service
    str_underscore_upper = "_".join(
        [v.upper() for v in strli]
    )  # odb-service => ODB_SERVICE

    return AlteredStrVersions(
        original=s,
        title=str_title,
        title_joined=str_title_joined,
        dash=str_dash,
        dash_upper=str_dash_upper,
        underscore=str_underscore,
        underscore_upper=str_underscore_upper,
    )
