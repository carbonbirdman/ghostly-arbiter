#!/bin/bash --login
# login is important for ensuring configuration is loaded
set -euo pipefail
conda activate /home/birdman/.conda/envs/app
exec python /home/$USER/app/arb_search.py >>  /home/$USER/app/arb_out.txt
