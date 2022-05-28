#! /bin/bash

TEMP="$(vcgencmd measure_temp | grep "[0-9]*\.[0-9]" -o)"

DATE="$(date)"

EPOCH_T="$(date +%s)"

echo "${DATE},${EPOCH_T},${TEMP}" >> "${HOME}/temp_hist.csv"
