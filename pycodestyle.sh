#!/bin/bash

# Ignoring autogenerated files
#  -- Migration directories
# Ignoring error codes
#  -- E128 continuation line under-indented for visual indent
#  -- E225 missing whitespace around operator
#  -- E501 line too long

pycodestyle --exclude=migrations,tests --ignore=E128,E225,E501 .
