#!/bin/bash
mkdir -p /mnt/gold/dockerfiles

echo "Extracting..."
tar -xJf /mnt/inputs/gold.tar.xz -C /mnt/gold/dockerfiles
echo "  + Done!"

find /mnt/gold/dockerfiles -type f | sort \
  | python3 /app/app.py gold
