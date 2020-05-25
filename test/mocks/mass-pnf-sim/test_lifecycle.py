from MassPnfSim import MassPnfSim
from glob import glob
from os import popen
from yaml import load, SafeLoader
from ipaddress import ip_address
from test_settings import *
import pytest
from time import sleep

# These test routines perform functional testing in current file tree context
# thus they require that no simulator instances are bootstrapped and running
# prior to running tests

@pytest.mark.parametrize("action", ['start', 'stop', 'trigger', 'status'])
def test_not_bootstrapped(action, caplog, args_start, args_stop, args_trigger, args_status): # pylint: disable=W0613
    try:
        m = getattr(MassPnfSim(eval(f'args_{action}')), action)
        m()
    except SystemExit as e:
        assert e.code == 1
    assert 'No bootstrapped instance found' in caplog.text
    caplog.clear()

def test_bootstrap(args_bootstrap, parser, caplog):
    # Initial bootstrap
    MassPnfSim(args_bootstrap).bootstrap()
    for instance in range(SIM_INSTANCES):
        assert f'Creating pnf-sim-lw-{instance}' in caplog.text
        assert f'Done setting up instance #{instance}' in caplog.text
    caplog.clear()

    # Verify bootstrap idempotence
    try:
        MassPnfSim(args_bootstrap).bootstrap()
    except SystemExit as e:
        assert e.code == 1
    assert 'Bootstrapped instances detected, not overwiriting, clean first' in caplog.text
    caplog.clear()

    # Verify simulator dirs created
    sim_dirname_pattern = MassPnfSim(parser.parse_args([])).sim_dirname_pattern
    assert len(glob(f"{sim_dirname_pattern}*")) == SIM_INSTANCES

    # Verify ROP_file_creator.sh running
    for instance in range(SIM_INSTANCES):
        assert f"ROP_file_creator.sh {instance}" in popen('ps afx').read()

    # Verify simulators configs content is valid
    start_port = 2000
    for instance in range(SIM_INSTANCES):
        instance_ip_offset = instance * 16
        ip_offset = 2
        with open(f"{sim_dirname_pattern}{instance}/{INSTANCE_CONFIG}") as f:
            yml = load(f, Loader=SafeLoader)
        assert URLVES == yml['urlves']
        assert TYPEFILESERVER == yml['typefileserver']
        assert f'sftp://onap:pano@{IPFILESERVER}:{start_port + 1}' in yml['urlsftp']
        assert f'ftps://onap:pano@{IPFILESERVER}:{start_port + 2}' in yml['urlftps']
        assert str(ip_address(IPSTART) + ip_offset + instance_ip_offset) == yml['ippnfsim']
        start_port += 2
        print(yml['ippnfsim'])

def test_bootstrap_status(args_status, capfd):
    MassPnfSim(args_status).status()
    msg = capfd.readouterr()
    for _ in range(SIM_INSTANCES):
        assert 'Simulator containers are down' in msg.out
        assert 'Simulator response' not in msg.out

def test_start(args_start, caplog, capfd):
    MassPnfSim(args_start).start()
    msg = capfd.readouterr()
    for instance in range(SIM_INSTANCES):
        instance_ip_offset = instance * 16
        ip_offset = 2
        assert f'Starting pnf-sim-lw-{instance} instance:' in caplog.text
        assert f'PNF-Sim IP:  {str(ip_address(IPSTART) + ip_offset + instance_ip_offset)}' in msg.out
        assert 'Starting simulator containers' in msg.out
    caplog.clear()

def test_start_status(args_status, docker_containers, capfd):
    sleep(5) # Wait for the simulator to settle
    MassPnfSim(args_status).status()
    msg = capfd.readouterr()
    for instance in range(SIM_INSTANCES):
        assert '"simulatorStatus":"NOT RUNNING"' in msg.out
        assert '"simulatorStatus":"RUNNING"' not in msg.out
        assert f"{PNF_SIM_CONTAINER_NAME}{instance}" in docker_containers

def test_start_idempotence(args_start, capfd):
    '''Verify start idempotence'''
    MassPnfSim(args_start).start()
    msg = capfd.readouterr()
    assert 'Simulator containers are already up' in msg.out
    assert 'Starting simulator containers' not in msg.out

def test_trigger(args_trigger, caplog, capfd):
    MassPnfSim(args_trigger).trigger()
    msg = capfd.readouterr()
    for instance in range(SIM_INSTANCES):
        instance_ip_offset = instance * 16
        ip_offset = 2
        assert f'Triggering pnf-sim-lw-{instance} instance:' in caplog.text
        assert f'PNF-Sim IP:  {str(ip_address(IPSTART) + ip_offset + instance_ip_offset)}' in msg.out
        assert 'Simulator started' in msg.out
    caplog.clear()

def test_trigger_status(args_status, capfd):
    MassPnfSim(args_status).status()
    msg = capfd.readouterr()
    for _ in range(SIM_INSTANCES):
        assert '"simulatorStatus":"RUNNING"' in msg.out
        assert '"simulatorStatus":"NOT RUNNING"' not in msg.out
        assert 'Up' in msg.out
        assert 'Exit' not in msg.out

def test_trigger_idempotence(args_trigger, capfd):
    MassPnfSim(args_trigger).trigger()
    msg = capfd.readouterr()
    assert "Cannot start simulator since it's already running" in msg.out
    assert 'Simulator started' not in msg.out

def test_trigger_custom(args_trigger_custom, caplog, capfd):
    MassPnfSim(args_trigger_custom).trigger_custom()
    msg = capfd.readouterr()
    for instance in range(SIM_INSTANCES):
        instance_ip_offset = instance * 16
        ip_offset = 2
        assert f'Triggering pnf-sim-lw-{instance} instance:' in caplog.text
        assert f'PNF-Sim IP:  {str(ip_address(IPSTART) + ip_offset + instance_ip_offset)}' in msg.out
        assert 'Simulator started' not in msg.out
        assert "Cannot start simulator since it's already running" in msg.out
    caplog.clear()

def test_stop(args_stop, caplog, capfd):
    MassPnfSim(args_stop).stop()
    msg = capfd.readouterr()
    for instance in range(SIM_INSTANCES):
        instance_ip_offset = instance * 16
        ip_offset = 2
        assert f'Stopping pnf-sim-lw-{instance} instance:' in caplog.text
        assert f'PNF-Sim IP:  {str(ip_address(IPSTART) + ip_offset + instance_ip_offset)}' in msg.out
        assert f"ROP_file_creator.sh {instance}" not in popen('ps afx').read()
    caplog.clear()

def test_stop_idempotence(args_stop, caplog, capfd):
    MassPnfSim(args_stop).stop()
    msg = capfd.readouterr()
    for instance in range(SIM_INSTANCES):
        assert f'Stopping pnf-sim-lw-{instance} instance:' in caplog.text
        assert 'ROP_file_creator.sh already not running' in msg.out
        assert 'Simulator containers are already down' in msg.out
    caplog.clear()

def test_clean(args_clean):
    m = MassPnfSim(args_clean)
    m.clean()
    assert not glob(f"{m.sim_dirname_pattern}*")
