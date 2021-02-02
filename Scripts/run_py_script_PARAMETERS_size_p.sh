#!/bin/bash

for p in 0.03 0.08
	do
		for group_size in {2..20}	
			do ../../../barrat/anaconda/bin/python SimHomMix_kuniformHG_PARAMETERS_size_p_I.py $group_size $p
		done
done

