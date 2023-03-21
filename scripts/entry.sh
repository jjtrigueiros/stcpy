#!/bin/bash

# - starts application

set -o errexit
set -o pipefail
set -o nounset

echo Starting Starlite App...
uvicorn --host 0.0.0.0 stcpy:app

