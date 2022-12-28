import optparse
import shlex

def cmd_netstat(cmd_args="", std_in=""):
    cmd_args = shlex.split(cmd_args)
    if "--help" in cmd_args or "-h" in cmd_args:
        return """
netstat - Print network connections, routing tables, interface statistics, masquerade connections, and multicast memberships
Synopsis:
  netstat [OPTION]...
Options:
  -a, --all            display all sockets (default: connected)
  -t, --tcp            display TCP sockets
  -u, --udp            display UDP sockets
  -n, --numeric        don't resolve names
  --help               display this help and exit
"""

    std_out = """
tcp        0      0 127.0.0.1:2222          0.0.0.0:*               LISTEN      
tcp6       0      0 ::1:2222                :::*                    LISTEN      
"""

    return std_out

def cmd_iptables(cmd_args="", std_in=""):
    cmd_args = shlex.split(cmd_args)
    # --helpオプションが指定された場合はヘルプを表示する
    if "--help" in cmd_args or "-h" in cmd_args:
        return """
iptables - administration tool for IPv4 packet filtering and NAT
Synopsis:
  iptables [-t table] -[ADC] chain rule-specification [options]
  iptables [-t table] -[RI] chain
  iptables -[LFZ] [chain]
  iptables -[NX] chain
  iptables -E old-chain-name new-chain-name
  iptables -P chain target
  iptables -h (print this help information)
"""

    std_out = """
iptables v1.8.7 (nf_tables): no command specified
Try `iptables -h' or 'iptables --help' for more information.
"""

    # -Lオプションが指定された場合は、現在のフィルタの設定を表示する
    if "-L" in cmd_args:
        std_out = """
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  anywhere             anywhere            
DROP       tcp  --  anywhere             anywhere             tcp dpt:http

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  anywhere             anywhere            

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  anywhere             anywhere
"""

    return std_out

