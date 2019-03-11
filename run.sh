#!/bin/bash

args="$@"

env_and_db()
{
    source secrets.sh && echo "environment variables set"
    # python3 seed_db.py && echo "database successfully seeded"

}

serve()
{
    if [[ $args = "serve" ]];
    then
        echo "starting server" && python3 server.py
    fi
}


env_and_db
serve