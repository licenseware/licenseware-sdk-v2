import uuid
import datetime
import datetime
import dateutil.parser as dateparser
from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.common.serializers import PublicTokenSchema


def valid_public_token(public_token:str):
    
    results = mongodata.fetch(
        match = {"token": public_token},
        collection = envs.MONGO_COLLECTION_TOKEN_NAME
    )

    if not results:
        return False

    now = datetime.datetime.utcnow()
    exp = dateparser.parse(results[0]["expiration_date"])

    if now > exp:
        mongodata.delete(
            match = {"token": public_token},
            collection = envs.MONGO_COLLECTION_TOKEN_NAME
        )
        return False

    return True



def get_public_token(tenant_id: str):

    data = dict(
        tenant_id = tenant_id,
        token = str(uuid.uuid4()),
        expiration_date = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat(),
    )

    results = mongodata.fetch(
        match={"tenant_id": tenant_id},
        collection=envs.MONGO_COLLECTION_TOKEN_NAME
    )   

    if results:
        if valid_public_token(results[0]["token"]):
            return results[0]["token"]

    mongodata.update(
        schema=PublicTokenSchema,
        match={"tenant_id": tenant_id},
        new_data=data,
        collection=envs.MONGO_COLLECTION_TOKEN_NAME
    )

    return data["token"]

    

def delete_public_token(tenant_id: str):

    mongodata.delete(
        match={"tenant_id": tenant_id},
        collection=envs.MONGO_COLLECTION_TOKEN_NAME
    )

    return "Public token deleted"

    

