#!/bin/sh

echo "init"
python comm.py --settings=droneA
echo "fim"
exec "$@"
