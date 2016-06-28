from elasticsearch import Elasticsearch
import argparse
import json
from sys import stdin


parser = argparse.ArgumentParser('Takes a JSON object from input stream \
                                 and uploads the object to an Elastic server')

parser.add_argument('--address',
                    type=str,
                    help='IP address of the server running the database',
                    required=True)
parser.add_argument('--port',
                    type=int,
                    help='Port used by the database',
                    required=True)
parser.add_argument('--index',
                    type=str,
                    help='Index that data is uploaded to',
                    required=True)
parser.add_argument('--type',
                    type=str,
                    help='Type assigned to every object uploaded',
                    required=True)
args = parser.parse_args()

elastic = Elasticsearch(['{}:{}'.format(args.address, args.port)])

upload_data = json.loads(stdin.read())

bulk_body = ''
for entry in upload_data:
    bulk_body += '{"create": {}}\n'
    bulk_body += json.dumps(entry) + '\n'

response = elastic.bulk(bulk_body, args.index, args.type)

errors = response.items()[1][1]
if errors:
    exit(1)
