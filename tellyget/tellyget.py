from tellyget.auth import Auth
from tellyget.guide import Guide

import argparse

parser = argparse.ArgumentParser(description='Generate iptv configs')

parser.add_argument('-u', '--user', type=str, required=True, help='user name for login')
parser.add_argument('-p', '--passwd', type=str, required=True, help='password for login')
parser.add_argument('-m', '--mac', type=str, required=True, help='MAC of box')
parser.add_argument('-i', '--imei', type=str, default='', help='imei of box')
parser.add_argument('-a', '--address', type=str, default='', help='IP address of box')
parser.add_argument('-I', '--interface', type=str, help='interface of iptv')
parser.add_argument('-U', '--authurl', type=str, default='http://eds.iptv.gd.cn:8082/EDS/jsp/AuthenticationURL', help='authenticate url')
parser.add_argument('-o', '--output', type=str, default='iptv.m3u', help='m3u output path')
parser.add_argument('-f', '--filter', nargs='+', default=['^\d+$'], help='channel filter')
parser.add_argument('-A', '--all-channel', default=False, action='store_true', help='no filter sd channels')



def main():
    args = parser.parse_args()
    print(args)
    auth = Auth(args)
    auth.authenticate()
    guide = Guide(args, auth.session, auth.base_url)
    channels = guide.get_channels()

    playlist = guide.get_playlist(channels)
    guide.save_playlist(playlist)
