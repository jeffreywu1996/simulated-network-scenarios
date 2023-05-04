import os
import subprocess
import shlex
import logging
from typing import List

# tcdel = "/usr/local/bin/tcdel"
# tcset = "/usr/local/bin/tcset"
# tcshow = "/usr/local/bin/tcshow"

tcdel = subprocess.check_output(["which", "tcdel"]).strip().decode()
tcset = subprocess.check_output(["which", "tcset"]).strip().decode()
tcshow = subprocess.check_output(["which", "tcshow"]).strip().decode()
nslookup = subprocess.check_output(["which", "nslookup"]).strip().decode()

NET_INT = "eth0"

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


def parse_ip(domains: List[str]) -> List[str]:
    """return ip address that required by tcset"""
    ips = list()
    for d in domains:
        output = subprocess.check_output([nslookup, d]).strip().decode().split("\n")
        for v in output[::-1]:
            if v.startswith("Address:"):
                idx = v.index(":") + 1
                ips.append(v[idx:].lstrip())
            if v.startswith("Non-authoritative answer:"):
                break
    # print(ips)
    return ips


def reset():
    logger.info("Resetting all network restraints")
    subprocess.call([tcdel, NET_INT, "--all"])
    network_up()


def set(delay=None, loss=None, rate=None, port=None):
    logger.info(f'Setting network shaping with delay={delay}, loss={loss}, rate={rate}, port={port}')

    # cmd = [tcset, NET_INT, "--overwrite", "--network", "", "--ipv6"]
    # cmd = [tcset, NET_INT, "--overwrite", "--network", "ip", "--network", "ip", "--network", "ip", ]
    # cmd = [tcset, NET_INT, "--overwrite", "--network", GRPC_SERVERS]
    cmd = [tcset, NET_INT, "--overwrite"]

    ips = parse_ip(GRPC_SERVERS.split(","))
    for ip in ips:
        cmd.extend(["--network", ip])

    if delay:
        cmd.append("--delay")
        cmd.append(delay)
    if loss:
        cmd.append("--loss")
        cmd.append(loss)
    if rate:
        cmd.append("--rate")
        cmd.append(rate)
    if port:
        cmd.append("--port")
        cmd.append(port)

    subprocess.call(cmd)


def show():
    subprocess.call([tcshow, "--device", NET_INT, "--ipv6"])


def network_down():
    logger.info(f"Stopping network, grpc servers: {GRPC_ENV}")
    cmd = f"iptables -I OUTPUT -p tcp -d {GRPC_SERVERS} -j DROP"
    # cmd = "iptables -I OUTPUT -p tcp --dport 18200,18300,18400 -j DROP"
    subprocess.call(shlex.split(cmd))


def network_up():
    logger.info(f"Starting network, grpc_servers: {GRPC_ENV}")
    cmd = f"iptables -I OUTPUT -p tcp -d {GRPC_SERVERS} -j ACCEPT"
    subprocess.call(shlex.split(cmd))
