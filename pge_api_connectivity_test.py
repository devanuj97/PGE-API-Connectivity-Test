from email import header
import requests
from constant import AUTH_SERVER_TOKEN_ENDPOINT, CLIENT_ID, CLIENT_SECRET, SERVICE_STATUS_API, SAMPLE_DATA_API

class PgeApiConnectivityTest:
    def __init__(self) -> None:
        self.client_access_token = PgeApiConnectivityTest.get_client_access_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )

    @staticmethod
    def get_client_access_token(*, client_id: str, client_secret: str):
        # Note: for the Access Token request you must attach your SSL Certificate.
        response = requests.post(
            url=AUTH_SERVER_TOKEN_ENDPOINT,
            headers={"Authorization": "Base64 encoding of -- client_ID:client_Secret"},
            json={"grant_type": "client_credentials"},
        )
        """return xml
        example -- 
        <Response xmlns="https://api.pge.com/datacustodian/oauth/v2/token">
            <client_access_token>c03a9825-16f7-400a-b546-9a206ab995db</client_access_token>
            <expires_in>3600</expires_in>
            <scope>3</scope>
            <token_type>Bearer</token_type>
        </Response>
        """
        return response.json()

    def get_status_status_api_call(self):
        response = requests.get(
            url=SERVICE_STATUS_API,
            headers={
                "Authorization": f"Bearer {self.client_access_token}"
            }
        )
        """return xml
        example -- 
        <ServiceStatus xsi:schemaLocation="http://naesb.org/espi espiDerived.xsd" xmlns="http://naesb.org/espi" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <currentStatus>1</currentStatus>
        </ServiceStatus>
        """
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

    