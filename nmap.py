import argparse
from subprocess import check_output
import re
from json import dumps
from datetime import datetime

parser = argparse.ArgumentParser('Calls nmap with given arguments \
                                    and pushes the result to a database')

parser.add_argument('--search-address',
                    type=str,
                    help='IP address to search with nmap',
                    required=True)
parser.add_argument('--nmap-option',
                    type=str,
                    help='Option to use with nmap')
parser.add_argument('--search-mask',
                    type=int,
                    help='Subnet mask used to specify a subnet to search')
args = parser.parse_args()

# Generate nmap command
nmap_str = 'nmap'

if args.nmap_option is not None:
    nmap_str += ' -' + args.nmap_option

nmap_str += ' ' + args.search_address

if args.search_mask is not None:
    nmap_str += '/' + str(args.search_mask)

# Call nmap, retrieve raw result
result = check_output(nmap_str, shell=True)
res_iter = iter(result.split('\n'))

# Parse result
hosts = []

while True:
    try:
        line = next(res_iter)

        if re.match('Nmap\sscan\sreport\sfor', line) is not None:
            host_data = {}
            host_data['open_ports'] = []
            host_data['timestamp'] = datetime.now().isoformat()

            raw_data = line.split()

            host_data['name'] = raw_data[4]
            host_data['ip'] = raw_data[5][1:-1]
            for i in range(3):
                next(res_iter)

            line = next(res_iter)
            while line != '':
                raw_data = line.split()
                if raw_data[1] == 'open':
                    port = re.match('\d+', raw_data[0]).group(0)
                    host_data['open_ports'].append(int(port))

                line = next(res_iter)
            hosts.append(host_data)
    except StopIteration:
        break

print(dumps(hosts))
