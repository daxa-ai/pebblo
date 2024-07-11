from dotenv import load_dotenv

import asyncio
import os
from typing import Optional

from msgraph import GraphServiceClient
from azure.identity import ClientSecretCredential
from kiota_abstractions.api_error import APIError


load_dotenv()  # While running RAG app, move to line no. 2


async def get_authorized_identities(
    user_id: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    tenant_id: Optional[str] = None,
):
    client_id = client_id or os.environ.get("O365_CLIENT_ID")
    client_secret = client_secret or os.environ.get("O365_CLIENT_SECRET")
    tenant_id = tenant_id or os.environ.get("O365_TENANT_ID")
    if not all([client_id, client_secret, tenant_id]):
        raise EnvironmentError(
            "atleast one of {O365_CLIENT_ID, O365_CLIENT_SECRET or O365_TENANT_ID not provided"
        )
    credentials = ClientSecretCredential(
        tenant_id,
        client_id,
        client_secret,
    )
    graph_client = GraphServiceClient(credentials)

    # user = graph_client.users.by_user_id(user_id)
    try:
        groups = await graph_client.users.by_user_id(user_id).member_of.get()
    except APIError:
        print(f"ms_graph API error: invalid user: {user_id}")
        return [user_id]
    auth_iden = [
        group.__dict__.get("mail")
        for group in groups.value
        if group.__dict__.get("mail")
    ] + [user_id]
    return auth_iden


if __name__ == "__main__":
    print(asyncio.run(get_authorized_identities("arpit@daxaai.onmicrosoft.com")))
