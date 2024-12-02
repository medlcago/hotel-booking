#!/bin/bash

poetry run celery -A src.tasks worker --loglevel=info
