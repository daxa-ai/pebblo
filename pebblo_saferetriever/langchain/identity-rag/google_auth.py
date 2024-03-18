from typing import List

from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_authorized_identities(
    admin_user_email_address: str, credentials_file_path: str, user_email: str
) -> List[str]:
    """
    Get authorized identities from Google Directory API
    """
    _authorized_identities = [user_email]
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file_path,
        scopes=[
            "https://www.googleapis.com/auth/admin.directory.group.readonly",
            "https://www.googleapis.com/auth/admin.directory.group",
        ],
        subject=admin_user_email_address,
    )
    directory_service = build("admin", "directory_v1", credentials=credentials)

    try:
        groups = directory_service.groups().list(userKey=user_email).execute()
        for group in groups.get("groups", []):
            group_email = group["email"]
            _authorized_identities.append(group_email)
    except Exception as e:
        print(f"Error in : {e}")
    print(f"User: {user_email}, \nAuthorized Identities: {_authorized_identities}\n")
    return _authorized_identities


if __name__ == "__main__":
    email = "user@daxa.ai"
    authorized_identities = get_authorized_identities(email)
