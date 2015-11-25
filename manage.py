from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand
import os
from app import create_app
from models import Job
from database import db

os_env = os.environ
app_settings = os_env.get('APP_SETTINGS','config.DevConfig')

app = create_app(app_settings)

def make_context():
    return {'app': app, 'db': db, 'Job':Job}

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=make_context))

if __name__ == '__main__':
    manager.run()
