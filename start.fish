#!/usr/bin/fish

#env (cat .env) fish

export (cat .env |xargs -L 1)

python src/server.py
