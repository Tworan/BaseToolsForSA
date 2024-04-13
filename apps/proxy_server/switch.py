import requests 
import argparse

url = "http://10.201.195.175:9090/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9"

parser = argparse.ArgumentParser()
parser.add_argument("--node", help="node name")

args = parser.parse_args()

data = {"name": args.node}
ret = requests.put(url, json=data)
print(ret)
