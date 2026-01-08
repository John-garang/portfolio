#!/bin/bash
# Static file server for portfolio
python3 -m http.server ${PORT:-8080}