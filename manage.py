from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
import os
from app import create_app

os_env = os.environ
app_settings = os_env.get('APP_SETTINGS','config.DevConfig')

app = create_app(app_settings)


manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('server', Server())
if __name__ == '__main__':
    manager.run()
