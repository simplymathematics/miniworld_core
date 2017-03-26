import gzip
import json
import shutil
import subprocess
import sys
import tempfile
import urllib2
from StringIO import StringIO

import os
import pytest
from copy import deepcopy

import signal

from miniworld.util import JSONConfig

devnull = open(os.devnull, "w")


@pytest.fixture
def config_path(tmpdir_factory):
    return str(tmpdir_factory.mktemp('config').join('config.json'))


def pytest_addoption(parser):
    parser.addoption("--no-server", action="store_true",
                     help="Start the miniworld server from outside")


@pytest.fixture(scope='session')
def image_path():
    image_url = 'https://downloads.openwrt.org/chaos_calmer/15.05.1/x86/kvm_guest/openwrt-15.05.1-x86-kvm_guest-combined-ext4.img.gz'
    image_name = os.path.basename(image_url)
    # always use the same file path to prevent multiple downloads
    image_path = str(os.path.join(tempfile.gettempdir(), image_name))

    if not os.path.exists(image_path):
        print('downloading {} to {}'.format(image_url, image_path))
        data = StringIO(urllib2.urlopen(image_url).read())
        gzip_data = gzip.GzipFile(fileobj=data)
        with open(image_path, 'w') as f:
            f.write(gzip_data.read())
    return image_path


@pytest.fixture
def runner(tmpdir_factory, config_path, request):
    class Runner(object):
        def __init__(self, debug=True):
            self.scenario = str(tmpdir_factory.mktemp('scenarios').join('scenario.json'))
            self.config = config_path
            self.server_proc = None
            self.is_start_server = not request.config.getoption("--no-server")
            self.debug = True

            if not os.path.exists(config_path):
                shutil.copy2('sample_configs/config.json', config_path)
                if self.debug:
                    self.enable_debug()
                print('config: {}:'.format(config_path))
                with open(config_path, "r") as f:
                    print(f.read())
            os.environ['CONFIG'] = config_path

        def enable_debug(self):
            config = JSONConfig.read_json_config(self.config)
            config['logging']['level'] = 'DEBUG'
            #config['logging']['debug'] = True
            config['logging']['log_provisioning'] = True
            with open(config_path, "w") as f:
                f.write(json.dumps(config, indent=4))

        def __enter__(self):
            env = deepcopy(os.environ)
            env.update({'CONFIG': self.config})
            if self.is_start_server:
                self.server_proc = subprocess.Popen(['./start_server.sh'], env=env)
                sys.stderr.write('server started\n')
            else:
                sys.stderr.write('please start the server yourself')
            self.connect_to_server()

            return self

        def __exit__(self, type, value, traceback):
            # check for rpc errors
            self.check_for_errors()
            # shut down gracefully
            subprocess.check_call(['./mw.py', 'stop'])
            if self.server_proc:
                self.server_proc.kill()

                def hard_shutdown(*args, **kwargs):
                    if not self.server_proc.poll() is not None:
                        print('graceful shutdown did not succeed')
                        self.server_proc.send_signal(signal.SIGKILL)
                        signal.alarm(0)

                        assert False

                signal.signal(signal.SIGALRM, hard_shutdown)
                signal.alarm(5)
                self.server_proc.wait()

        def start_scenario(self, scenario):
            '''
            Parameters
            ----------
            scenario: dict
            '''
            with open(self.scenario, 'w') as f:
                scenario_json = json.dumps(scenario, indent=4)
                f.write(scenario_json)
                f.flush()
                print('scenario:\n{}'.format(scenario_json))
                subprocess.check_call(['./mw.py', 'start', f.name])

        def check_for_errors(self):
            subprocess.check_call(['./mw.py', 'ping'])

        def step(self):
            subprocess.check_call(['./mw.py', 'step'])

        @staticmethod
        def connect_to_server():
            print('connecting to server')
            while 1:
                try:
                    subprocess.check_call(['./mw.py', 'ping'], stdout=devnull, stderr=devnull)
                    sys.stderr.write('.')
                    return
                except subprocess.CalledProcessError:
                    pass

    return Runner
