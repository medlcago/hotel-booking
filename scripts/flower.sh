#!/bin/bash

poetry run celery -A src.tasks flower --loglevel=info