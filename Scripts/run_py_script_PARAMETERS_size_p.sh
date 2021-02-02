#!/bin/bash

for p in 0.03 0.08
	do
		for group_size in {2..20}	
			do python test.py $group_size $p
		done
done

