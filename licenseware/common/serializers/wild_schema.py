from marshmallow import Schema, INCLUDE


class WildSchema(Schema):
    """ 
        This schema is used when we are moving data already validated 
    """
    class Meta:
        unknown = INCLUDE
