#!/bin/sh

if [ "$1" = "up" ]; then
    echo "Upgrading head..."
    alembic upgrade head
elif [ "$1" = "down" ]; then
    echo "Downgrading to $2..."
    alembic downgrade $2
elif [ "$1" = "rev" ]; then
    echo "Generating revision $2..."
    alembic revision --autogenerate -m $2
elif [ "$1" = "his" ]; then
    echo "Getting history..."
    alembic history
else
    echo "Unknown command"
fi
