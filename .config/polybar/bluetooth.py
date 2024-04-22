#! /usr/bin/env python
import subprocess
import argparse
parser = argparse.ArgumentParser(description='bluetooth status for polybar')

parser.add_argument('-d', '--disconnected', help='diconnected format', type=str, default='未连接')
parser.add_argument('-m', '--mac', help='device mac address', type=str, required=True)
parser.add_argument('-f', '--format', help='output format', type=str, default='{mac}')

args = parser.parse_args()

device = ''
battery = '0'

def show(f):
  return f.replace("{mac}", args.mac).replace("{device}", device).replace("{battery}", battery)


result = subprocess.run(['bluetoothctl', 'info', args.mac], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

output = result.stdout.split('\n')


if len(output) > 3:
  kv = {i[0].strip(): i[1].strip() for i in map(lambda x: x.split(':'), output[1:-1])}
  if kv["Connected"] == 'yes':
    device = kv["Name"]
    battery = kv["Battery Percentage"][6:-1]
    print(show(args.format))
  else:
    print(show(args.disconnected))
else:
  print(show(args.disconnected))
