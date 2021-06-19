#!/bin/bash

mongoimport --host 127.0.0.1  -d restaurant_app -c restaurants --type json --file /src/data/data.json 
