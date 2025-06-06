#!/bin/sh
# wait_for_db.sh

set -e

host="db"
port="5432"
user="user"
# Get database name from the first argument, default to postgres if not provided
database="${1:-postgres}"

export PGPASSWORD="password"

>&2 echo "Waiting for PostgreSQL database '$database' at $host:$port..."

until pg_isready -h "$host" -p "$port" -U "$user" -d "$database"; do
  >&2 echo "PostgreSQL database '$database' is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL database '$database' is up - executing command"
exec "$@" 