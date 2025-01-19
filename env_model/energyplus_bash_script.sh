#!/bin/bash

# Set paths to EnergyPlus files
ENERGYPLUS_IDD="/Applications/energyplus/Energy+.idd"   # Adjust for your version
WEATHER_FILE="USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"          # Replace with actual path
INPUT_FILE="5ZoneAirCooled.idf" # Replace with actual path

timestamp=$(date +%s)
dirname="sim_$timestamp"
mkdir $dirname

OUTPUT_DIR=$dirname

energyplus -i "$ENERGYPLUS_IDD" \
           -w "$WEATHER_FILE" \
           "$INPUT_FILE"\
           -d "$OUTPUT_DIR"

# # Optional: Print a success message
echo "EnergyPlus simulation completed!"


# ok so we got it to work with the default models still need to find a coulple 
# things out 
# 1. I need to figure out cost fields / calculating cost on a basic building 
# 2. I need to use pyscript to grab the c02 emissions to input it into the 
#    model