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

    @staticmethod
    def format_site_url(site_url: str):
        """
        Formats the site URL to include the colon(:) in the URL as required by the Microsoft Graph API.
        Example:
        1. Default site URL:
            input: https://<tenant-name>.sharepoint.com/
            output: tenant.sharepoint.com
        2. Custom site URL:
            input: https://<tenant-name>.sharepoint.com/sites/<site-name>
            output: tenant.sharepoint.com:/sites/<site-name>

        :param site_url: The original SharePoint site URL.
        :return: The formatted site URL with a colon after the tenant domain.
        """

        # Check if the site URL contains the "/sites/" substring and format the URL accordingly
        if "/sites/" in site_url:
            parts = site_url.split("/sites/")
            if parts[0].endswith(":"):
                # If the URL already contains a colon, use the URL as is
                formatted_url = site_url
            else:
                # Add a colon after the tenant domain
                formatted_url = f"{parts[0]}:/sites/{parts[1]}"
        else:
            formatted_url = site_url

        # Remove the  https:// prefix from the site URL
        formatted_url = formatted_url.replace("https://", "")
        return formatted_url

    def get_site_id(self, site_url):
        """
        This function retrieves the ID of a SharePoint site using the Microsoft Graph API.

        Parameters:
        site_url (str): The URL of the SharePoint site.

        Returns:
        str: The ID of the SharePoint site.
        """
        # Format the site URL
        site_url = self.format_site_url(site_url)
        # Build URL to request site ID
        full_url = f"https://graph.microsoft.com/v1.0/sites/{site_url}"
        response = requests.get(
            full_url, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        site_id = response.json().get("id")  # Return the site ID
        return site_id

    def get_drive_id(self, site_id):
        """
        This function retrieves the IDs and names of all drives associated with a specified SharePoint site.

        Parameters:
        site_id (str): The ID of the SharePoint site.

        Returns:
        list: A list of dictionaries. Each dictionary represents a drive on the SharePoint site.
              Each dictionary contains the following keys:
              - 'id': The ID of the drive.
              - 'name': The name of the drive.
        """

        # Retrieve drive IDs and names associated with a site
        try:
            drives_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
            response = requests.get(drives_url, headers=self.headers)
            drives = response.json().get("value", [])
            drive_info = [
                ({"id": drive["id"], "name": drive["name"]}) for drive in drives
            ]
            # print(f"Drive Info: {drive_info}")
            return drive_info
        except requests.exceptions.HTTPError as e:
            print(
                f"Error while retrieving document library ID from Microsoft Graph API, Error: {e}"
            )
            return []


if __name__ == "__main__":
    pass
