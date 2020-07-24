from __future__ import with_statement
from fabric.api import local, env, settings, abort, run, cd
from fabric.contrib.console import confirm
import time

env.use_ssh_config = True
env.hosts = ['testphp']
# env.hosts = ['104.236.85.162']
# env.user = 'deployer'
# env.key_filename = '~/.ssh/id_deployex'

code_dir='/var/www/deploy-stage'
app_dir='/var/www/application'
repo='git@github.com:Marceti/testphp.git'
timestamp="release_%s" % int(time.time() * 1000)
release_dir=code_dir+'/releases'
current_release_dir=code_dir+'/releases/'+timestamp
logs_dir=code_dir+'/logs'


def deploy():
    fetch_repo()
    run_composer()
    update_permissions()
    prepare_logs_folder()
    add_env_symlinks()
    update_symlinks()


def fetch_repo():
    print('*** Fetching repo ***' )
    with cd(code_dir):
        with settings(warn_only=True):
            run("mkdir releases")
    with cd(release_dir):
        run("git clone -b master %s %s" % (repo, timestamp))

def run_composer():
    print('*** Running composer install ***' )
    with cd(current_release_dir):
        run("composer install --prefer-dist --no-scripts")
        run("php artisan clear-compiled --env=production")
        run("php artisan optimize --env=production")

def update_permissions():
    print('*** Update permissions ***' )
    with cd(current_release_dir):
        run("chgrp -R www-data .")
        run("chmod -R ug+rwx .")

def prepare_logs_folder():
    print('*** Preparing logs folder ***' )
    with cd(current_release_dir):
        run("rm -r storage/logs")
        run("ln -nfs %s storage/logs" % (logs_dir))
        run("chgrp -R www-data storage/logs")

def add_env_symlinks():
    print('*** Preparing env file ***' )
    with cd(code_dir):
        run("ln -nfs %s %s " % (code_dir+'/.env', current_release_dir+'/.env'))

def update_symlinks():
    with cd(code_dir):
        run("ln -nfs %s %s" % (current_release_dir, app_dir))
        run("chgrp -h www-data %s" % app_dir)
        run("sudo service php7.3-fpm reload")
