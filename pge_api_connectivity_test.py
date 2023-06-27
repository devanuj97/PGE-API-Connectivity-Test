import os
from email import header
import requests
from constant import AUTH_SERVER_TOKEN_ENDPOINT, CLIENT_ID, CLIENT_SECRET, SERVICE_STATUS_API, SAMPLE_DATA_API
import base64

class PgeApiConnectivityTest:
    def __init__(self) -> None:
        self.client_access_token = PgeApiConnectivityTest.get_client_access_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )

    @staticmethod
    def get_client_access_token(*, client_id: str, client_secret: str):
        cl_id =  base64.b64encode(client_id.encode("ascii"))
        cl_sec = base64.b64encode(client_secret.encode("ascii"))
        response = requests.post(
            url=f"{AUTH_SERVER_TOKEN_ENDPOINT}",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"{cl_id.decode('ascii')}:{cl_sec.decode('ascii')}"},
            verify=f"{os.getcwd()}/certs/api.pge.com.cer",
        )
        return response.text

    def get_status_status_api_call(self):
        response = requests.get(
            url=SERVICE_STATUS_API,
            headers={
                "Authorization": f"Bearer {self.client_access_token}"
            }
        )
        print(response.json())
        return response.json()

    def get_sample_data(self):
        response = requests.get(
            url=SAMPLE_DATA_API,
            headers={
                "Authorization": f"Bearer {self.client_access_token}"
            }
        )
        # return https://www.pge.com/includes/docs/xml/myhome/addservices/moreservices/sharemydata/MeterReadings_Example.xml
        return response.json()

    