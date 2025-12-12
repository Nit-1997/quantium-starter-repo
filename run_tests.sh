#!/bin/bash

source venv/bin/activate

pytest test_app.py

exit $?
