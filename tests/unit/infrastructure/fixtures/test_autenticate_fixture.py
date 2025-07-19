from datetime import datetime, timedelta, UTC
from emt_madrid.infrastructure.emt_api_client import Credentials

EMAIL = "email"
PASSWORD = "password"

CREDENTIALS = Credentials(email=EMAIL, password=PASSWORD)
TOKEN = "12345678-abcd-1234-abcd-1234567890ab"

now_plus_1h = int((datetime.now(UTC) + timedelta(days=1)).timestamp() * 1000)

# Example response for endpoint "v1/mobilitylabs/user/login/"
LOGIN_OK_RESPONSE = {
    "code": "01",
    "description": "Token extend  into control-cache Data recovered OK",
    "datetime": "2025-07-16T18:06:12.978943",
    "data": [
        {
            "nameApp": "OPENAPI MobilityLabs",
            "levelApp": 0,
            "updatedAt": "2023-07-11T23:32:21.6470000",
            "userName": "username",
            "lastUpdate": {"$date": 1752599387945},
            "idUser": "98765432-abcd-1234-abcd-1234567890ab",
            "priv": "U",
            "tokenSecExpiration": 86399,
            "email": "username@mail.com",
            "tokenDteExpiration": {"$date": now_plus_1h},
            "flagAdvise": True,
            "modeSession": "app",
            "deviceModel": "no_model",
            "accessToken": TOKEN,
            "apiCounter": {
                "current": 0,
                "dailyUse": 20000,
                "owner": 0,
                "licenceUse": "Please mention EMT Madrid MobilityLabs as data source. Thank you and enjoy!",
                "aboutUses": "If you need to extend the daily use of this API, please, register your App in Mobilitylabs and use your own X-ClientId and  passKey instead of generic login (more info in https://mobilitylabs.emtmadrid.es/doc/new-app and https://apidocs.emtmadrid.es/#api-Block_1_User_identity-login)",
            },
            "username": "username",
        }
    ],
}

USER_NOT_FOUND_RESPONSE = {
    "code": "92",
    "description": "Error: User not found (lapsed: 138 millsecs)",
    "datetime": "2025-07-16T18:13:59.692855",
    "data": [],
}

INVALID_PASSWORD_RESPONSE = {
    "code": "89",
    "description": "Error: Invalid user or Password (lapsed: 68 millsecs)",
    "datetime": "2025-07-16T18:14:43.434401",
    "data": [],
}

LOGIN_EXPIRED_TOKEN_RESPONSE = {
    "code": "01",
    "description": "Token extend  into control-cache Data recovered OK",
    "datetime": "2025-07-16T18:06:12.978943",
    "data": [
        {
            "nameApp": "OPENAPI MobilityLabs",
            "levelApp": 0,
            "updatedAt": "2023-07-11T23:32:21.6470000",
            "userName": "username",
            "lastUpdate": {"$date": 1751652984945},
            "idUser": "98765432-abcd-1234-abcd-1234567890ab",
            "priv": "U",
            "tokenSecExpiration": 86399,
            "email": "username@mail.com",
            "tokenDteExpiration": {"$date": 1751652984945},
            "flagAdvise": True,
            "modeSession": "app",
            "deviceModel": "no_model",
            "accessToken": TOKEN,
            "apiCounter": {
                "current": 0,
                "dailyUse": 20000,
                "owner": 0,
                "licenceUse": "Please mention EMT Madrid MobilityLabs as data source. Thank you and enjoy!",
                "aboutUses": "If you need to extend the daily use of this API, please, register your App in Mobilitylabs and use your own X-ClientId and  passKey instead of generic login (more info in https://mobilitylabs.emtmadrid.es/doc/new-app and https://apidocs.emtmadrid.es/#api-Block_1_User_identity-login)",
            },
            "username": "username",
        }
    ],
}

API_LIMIT_EXCEEDED_RESPONSE = {
    "code": "98",
    "description": "Limit use API reached, please, contact with mobilitylabs@emtmadrid.es (lapsed: 691 millsecs)",
    "datetime": "2025-07-17T17:42:02.261385",
    "data": [],
}
