RULE_KEYS = ["values"]

class EncryptionSelector:
    """
        Get all encryption rules for an uploader.

        Encryption rules are a list[dict] shaped:

        {
            "target": any(filecontent, filename, columns),
            "values": any(regex, columns),
            "description": "concise description for the rule",
            "uploader_id": "needs to match the uploader id from reg service"
        }

    """

    def __init__(self, uploader_id, encryption_rules):
        self.uploader_id = uploader_id
        self.encryption_rules = self._get_uploader_rules(encryption_rules)
        self.filecontent_rules = self.get_rule("filecontent")
        self.filepaths_rules = self.get_rule("filename")
        self.columns_rules = self.get_rule("columns")

    def _get_uploader_rules(self, encryption_rules):
        return [x for x in encryption_rules if x["uploader_id"] == self.uploader_id]
    
    def get_rule(self, rule_target):
        rules = []
        for rule in self.encryption_rules:
            if rule["target"] == rule_target:
                self.append_new_rule(
                    new_rule=rule,
                    rules=rules
                )
        return rules

    def append_new_rule(self, new_rule, rules):
        for key in RULE_KEYS:
            try:
                rules += new_rule[key] if isinstance(new_rule[key], list) else [new_rule[key]]
            except KeyError:
                pass
        return rules