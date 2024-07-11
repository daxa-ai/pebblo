import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class SharepointADHelper:
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ):
        self.client_id = client_id or os.environ.get("O365_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("O365_CLIENT_SECRET")
        self.tenant_id = tenant_id or os.environ.get("O365_TENANT_ID")
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            raise EnvironmentError(
                "At-least one of O365_CLIENT_ID, O365_CLIENT_SECRET or O365_TENANT_ID not provided"
            )
        self.access_token = self.get_access_token()
        if not self.access_token:
            raise EnvironmentError(
                "o365 client id/secret or tenant id is invalid."
                "Please check the environment variables."
            )
        self.headers = {"Authorization": "Bearer" + self.access_token}

    def get_authorized_identities(self, user_id: str):
        """
        Retrieves the authorized identities for a given user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of authorized identities, including associated group emails and the user ID.
        """
        user = self._get_users(user_id)
        user_index_id = user.get("id")
        if not user_index_id:
            print(
                f"Could not find the user `{user_id}` information in Microsoft Graph API. Not authorized."
            )
            return [user_id]
        associated_groups = self._get_associated_groups(user_index_id)
        associated_groups_emails = [
            group.get("mail")
            for group in associated_groups["value"]
            if group.get("mail")
        ]
        return associated_groups_emails + [user_id]

    def _get_associated_groups(self, user_index_id: str):
        """
        Retrieves the associated groups for a given user.

        Args:
            user_index_id (str): The index ID of the user.

        Returns:
            dict: A dictionary containing the associated groups information.

        Raises:
            Exception: If there is an error while making the API request.
        """
        url = f"https://graph.microsoft.com/v1.0/users/{user_index_id}/memberOf"
        try:
            response = requests.get(url=url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            print("Error while retrieving associated groups from Microsoft Graph API")
            return {}
        else:
            return response.json()

    def _get_users(self, user_id: str):
        """
        Retrieves information about a specific user from the Microsoft Graph API.

        Args:
            user_id (str): The ID of the user to retrieve information for.

        Returns:
            dict: A dictionary containing the user's information.

        Raises:
            Exception: If there is an error while making the API request.
        """
        url = f"https://graph.microsoft.com/v1.0/users/{user_id}"
        try:
            response = requests.get(url=url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            print("Error while retrieving user information from Microsoft Graph API")
            return {}
        else:
            return response.json()

    def get_access_token(self):
        """
        Retrieves an access token from Microsoft Graph API using client credentials.
        Returns:
            str: The access token.
        Raises:
            requests.exceptions.HTTPError: If the request to retrieve the access token fails.
        """
        # ToDo: This access token should be cached and refreshed when it expires
        # It should also be stored in home directory or in a secure location
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
        }
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()  # Raise exception if the request failed
        except requests.exceptions.HTTPError:
            print("Error while retrieving access token from Microsoft Graph API")
            return ""
        else:
            return response.json()["access_token"]


if __name__ == "__main__":
    pass
