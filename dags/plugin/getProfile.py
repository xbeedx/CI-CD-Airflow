from typing import List, Optional, Union

#from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.decorators import apply_defaults
from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator

class GetProfileOperator(BaseOperator):

    template_fields = ()
    template_ext = ()
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self,
            *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def execute(self, context):
        import requests
        import time
        import json
        import pymongo
        urlProfile = 'https://financialmodelingprep.com/api/v3/company/profile/AAPL'
        payload = {
            'apikey': 'b5c4e8d0b3f2e3c1b0e8c2f3b0e8c2f3'
        }
        responseProfile = requests.get(urlProfile, params=payload)
        dataProfile = responseProfile.json()
        
        data = {}
        # get timestamp to timestamp format
        data["timestamp"] = time.time()
        data["profile"] = dataProfile

        with open('/tmp/profile.json', 'w') as f:
            json.dump(data, f)

        return data



class GetProfilePlugin(AirflowPlugin):
    name = "GetProfilePlugin"
    operators = [GetProfileOperator]
    