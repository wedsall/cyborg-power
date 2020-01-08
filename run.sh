#!/bin/bash

export PATH=~/anaconda3/bin:${PATH}
source activate pyomo

pyomo solve --solver=cbc implants.py
#glpk, ipopt, cbc
