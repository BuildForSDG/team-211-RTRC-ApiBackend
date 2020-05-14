import requests
from django.conf import settings

def confirm_payment(reference):
    __version__ = '1.21'


    headers = { 
                "Content-Type": "application/json", 
                "Authorization": "Bearer " + settings.PAYSTACK_SECRET,
                "user-agent": "pyPaystack-{}".format(__version__)
                }
    
    resp = requests.get(
        "{}/transaction/verify/{}".format(settings.PAYSTACK_BASE, reference),
        headers=headers,
        verify=True
        )

    if resp.status_code == 404:
        return None
    elif resp.status_code in [200, 201]:
        return resp.json()
    return None
