from google_auth_oauthlib.flow import InstalledAppFlow

# Define the API scopes you need:
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]  # Example


def main():
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file(
        "<Entere file name>", SCOPES
    )  # Replace with your credentials file
    creds = flow.run_local_server(port=0)  # Opens a browser for auth
    # Save the credentials to a file
    with open("<Enter output file name>", "w") as token:
        token.write(creds.to_json())
    print("Token saved to google_token.json")


if __name__ == "__main__":
    main()
