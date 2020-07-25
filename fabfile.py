
from __future__ import with_statement
from fabric.api import local, env, settings, abort, run, cd
from fabric.contrib.console import confirm
import time

env.use_ssh_config = True
env.hosts = ['testphp-deployer']
# env.hosts = ['104.236.85.162']
# env.user = 'deployer'
# env.key_filename = '~/.ssh/id_deployex'

code_dir='/var/www/deploy-stage'
app_dir='/var/www/application'

repo='Marceti/testphp.git'

timestamp="release_%s" % int(time.time() * 1000)

release_dir=code_dir+'/releases'
current_release_dir=code_dir+'/releases/'+timestamp

logs_dir=code_dir+'/logs'

def deploy():
    fetch_repo()
    prepare_logs_folder()
    add_env_symlinks()
    run_composer()
    update_permissions()
    update_symlinks()


def fetch_repo():
    print('*** Fetching repo ***********************************************************************' )
    with cd(code_dir):
        with settings(warn_only=True):
            run("mkdir releases")
    with cd(release_dir):
        run("git clone -b master github.com:%s %s" % (repo, timestamp))

def prepare_logs_folder():
    print('*** Preparing logs folder ***********************************************************************' )
    with cd(current_release_dir):
        run("rm -r storage/logs")
        run("ln -nfs %s storage/logs" % (logs_dir))


def add_env_symlinks():
    print('*** Preparing env file ***********************************************************************' )
    with cd(code_dir):
        run("ln -s %s %s " % (code_dir+'/.env', current_release_dir+'/.env'))


def run_composer():
    print('*** Running composer install ***********************************************************************' )
    with cd(current_release_dir):
        run("composer install --prefer-dist --no-scripts")
        run("php artisan package:discover --ansi --env=production")
        run("php artisan key:generate --ansi --env=production")

def update_permissions():
    print('*** Update permissions ***********************************************************************' )
    with cd(current_release_dir):
        run("chmod -R ug+rwx .")
        run("chgrp -R www-data .")


def update_symlinks():
    print('*** create simlinks  ***********************************************************************' )
    with cd(code_dir):
        run("rm -rf %s" % (app_dir))
        run("ln -s %s %s" % (current_release_dir, app_dir))
        run("chgrp -h www-data %s" % app_dir)
        #run("service php7.3-fpm reload")

