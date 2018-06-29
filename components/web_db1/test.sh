#!/bin/bash

json_delay="{'delay_post_f': $1, 'delay_post_b': $2, 'delay_get_f': $3, 'delay_get_b': $4}"
curl http://127.0.0.1:8001/api/v1/setdelay/k1 -X POST -H 'Content-Type:application/json' --data "$json_delay"
