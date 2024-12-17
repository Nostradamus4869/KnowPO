#!/bin/bash

python generate_inner_answer.py  > ../../logs/sqaudZen-generate_inner_answer.log 2>&1 &
pid1=$!  

python generate_counterfactual.py  > ../../logs/sqaudZen-generate_counterfactual.log 2>&1 &
pid2=$! 

wait $pid1
python generate_IR.py

wait $pid2

python generate_context.py --split_point 25000
python generate_RandC.py --split_point 25000
python generate_negative.py  > ../../logs/sqaudZen-generate_negative.log 2>&1 &

