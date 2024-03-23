#!/bin/bash

CF_API_KEY="17cd06f5b17982b00fac2cac259022d786e47"
CF_ZONE_ID="eed6a2806913e672377543c42a10462c"
CF_EMAIL="alperenruzgar@gmail.com"

curl -X POST "https://api.cloudflare.com/client/v4/zones/eed6a2806913e672377543c42a10462c/purge_cache" \
     -H "X-Auth-Email: alperenruzgar@gmail.com" \
     -H "X-Auth-Key: 17cd06f5b17982b00fac2cac259022d786e47" \
     -H "Content-Type: application/json" \
     --data '{"purge_everything":true}'