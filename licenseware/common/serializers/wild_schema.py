from marshmallow import INCLUDE, Schema


class WildSchema(Schema):
    """
    This schema is used when we are moving data already validated
    """

    class Meta:
        unknown = INCLUDE
