# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from typing import List, Optional, Union

#from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.decorators import apply_defaults
from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator

class JsonToMongoOperator(BaseOperator):

    template_fields = ()
    template_ext = ()
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self,
            file_to_load: str,
            mongoserver: str,
            mongouser: str,
            mongopass: str,
            *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.file_to_load = file_to_load
        self.mongoserver = mongoserver
        self.mongouser = mongouser
        self.mongopass = mongopass

    def execute(self, context):
        import pymongo
        import json
        client = pymongo.MongoClient(self.mongoserver, username=self.mongouser, password=self.mongopass)
        db = client["stock"]
        collection = db["AAPL"]
        with open(self.file_to_load, 'r') as f:
            data = json.load(f)
        collection.insert_one(data)
        return data


class JsonToMongoPlugin(AirflowPlugin):
    name = "JsonToMongoPlugin"
    operators = [JsonToMongoOperator]
    