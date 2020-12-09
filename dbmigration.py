#!/usr/bin/env python 
from app import app, SqlDB, migrate, manager
from seeders.authseeders import seed_users

@manager.command
def do_seed_users():
    "Seed initial user data"
    seed_users()


if __name__ == '__main__':
    manager.run()