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
# nslookup = subprocess.check_output(["which", "nslookup"]).strip().decode()

NET_INT = "eth0"

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)

SERVER_URL = os.getenv("SERVER_URL", "http://server:8001")


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


def set(delay: str = None, loss: str = None, rate: str = None,
        ip: str = None, port: str = None, direction: str = None):
    """
    delay='100ms'
    loss='10%'
    rate='1mbit'
    ip='0.0.0.0/0'
    port='8001'
    direction='outgoing'/'incoming'
    """
    logger.info(f'Setting network shaping with delay={delay}, loss={loss}, rate={rate}, port={port}')

    # cmd = [tcset, NET_INT, "--overwrite", "--network", "", "--ipv6"]
    # cmd = [tcset, NET_INT, "--overwrite", "--network", "ip", "--network", "ip", "--network", "ip", ]
    # cmd = [tcset, NET_INT, "--overwrite", "--network", GRPC_SERVERS]
    cmd = [tcset, NET_INT, "--overwrite"]

    # if ip is None:
    #     ip = SERVER_URL
    # cmd.extend(["--network", ip])

    # ips = parse_ip(GRPC_SERVERS.split(","))
    # for ip in ips:
    #     cmd.extend(["--network", ip])

    cmd.extend(["--port", "8001"])
    cmd.extend(["--direction", "outgoing"])

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


def network_down(ip: str = None, port: str = None):
    # if ip is None:
    #     ip = SERVER_URL
    # logger.info(f"Stopping network to servers: {SERVER_URL}")
    # cmd = f"iptables -I OUTPUT -p tcp -d {SERVER_URL} -j DROP"

    logger.info("Stopping network to servers: server:8001")
    port = 8001
    cmd = f"iptables -I OUTPUT -p tcp --dport {port} -j DROP"
    subprocess.call(shlex.split(cmd))


def network_up(ip: str = None, port: str = None):
    # logger.info(f"Starting network, grpc_servers: {GRPC_ENV}")
    # cmd = f"iptables -I OUTPUT -p tcp -d {GRPC_SERVERS} -j ACCEPT"
    # subprocess.call(shlex.split(cmd))

    logger.info("Starting network to servers: server:8001")
    port = 8001
    cmd = f"iptables -I OUTPUT -p tcp --dport {port} -j ACCEPT"
    subprocess.call(shlex.split(cmd))
