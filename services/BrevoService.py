from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import os
from dotenv import load_dotenv

class SendinblueService:
    def __init__(self):
        # Configure API key authorization: api-key
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

        # create an instance of the API class
        # create an instance of the API class
        self.api_instance = sib_api_v3_sdk.AccountApi(sib_api_v3_sdk.ApiClient(configuration))
        self.from_email = "iafordevsgrp7@gmail.com"
        try:
            # Get your account information, plan and credits details
            api_response = self.api_instance.get_account()
            print(f"Connected to Sendinblue. {api_response} with the account {api_response.email}.")
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling AccountApi->get_account: %s\n" % e)

        self.transactional_emails_api = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def send_email(self, email, subject, body):
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            sender={ "name": "IA For Dev - Grupo 7 (FIAP)", "email": self.from_email },
            to=[{"email": email}],
            subject=subject,
            html_content=body)
        try:
            # Send a transactional email
            api_response = self.transactional_emails_api.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)