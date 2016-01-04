#!/bin/bash
( cd /vagrant ; celery worker -A bin.api.celery_work )