# from licenseware import mongodata
# from marshmallow import Schema, fields
# from licenseware.common.constants import envs


# Failed methods..
# class AppRegisteredToggleSchema(Schema):
#     _id = fields.Str(required=True, unique=True)
#     app_registered = fields.Bool(required=True, default=False)


    
# def toggle_registration(app_registered: bool):
    
#     mongodata.update(
#         schema=AppRegisteredToggleSchema,
#         match={'_id': envs.APP_ID},
#         new_data={'_id': envs.APP_ID, 'app_registered': app_registered},
#         collection="_AppRegisteredToggle"
#     )
    
    
# def check_if_app_registered():
#     results = mongodata.fetch(match={'_id': envs.APP_ID}, collection="_AppRegisteredToggle")
#     app_registered = False
#     if results: app_registered = results[0]['app_registered']
#     return app_registered