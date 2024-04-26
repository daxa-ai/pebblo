import requests
import os

def get_authorized_identities(access_token, user_email):
    
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/memberOf"

    payload={}

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    group_names = []
    
    groups_list = response.json()['value']
    manually_created_groups = [group for group in groups_list if 'Unified' in group.get('groupTypes', [])]

    for group_data in manually_created_groups:
        # print(group_data.get('displayName'))
        group_names.append(group_data.get('displayName'))
    
    print(f"Authorized : {group_names}")