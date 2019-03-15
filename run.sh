#!/bin/bash

args="$@"

env_and_db()
{
    source secrets.sh && echo "Environment variables set"
    python3 seed_db.py && echo "Database successfully seeded as storybored"

}

serve()
{
    if [[ $args = "serve" ]];
    then
        echo "Starting server" && python3 server.py
    fi
}


env_and_db
serve