import json
from xml.dom import minidom

import datetime
import os
import re
from bs4 import BeautifulSoup


class Guide:
    def __init__(self, config, session, base_url, get_channels_data):
        self.config = config
        self.session = session
        self.base_url = base_url
        self.get_channels_data = get_channels_data
        self.channel_filters = self.config['guide']['channel_filters'].encode('unicode_escape')
        self.channel_filters = json.loads(self.channel_filters)

    def get_channels(self):
        response = self.session.post(self.base_url + '/EPG/jsp/getchannellistHWCTC.jsp')
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', string=re.compile('ChannelID="[^"]+"'))
        print(f'Found {len(scripts)} channels')
        channels = []
        filtered_channels = 0
        for script in scripts:
            match = re.search(r'Authentication.CTCSetConfig\(\'Channel\',\'(.+?)\'\)', script.string, re.MULTILINE)
            channel_params = match.group(1)
            channel = {}
            for channel_param in channel_params.split('",'):
                key, value = channel_param.split('="')
                channel[key] = value
            if self.match_channel_filters(channel):
                filtered_channels += 1
            else:
                channels.append(channel)
        print(f'Filtered {filtered_channels} channels')
        removed_sd_candidate_channels = self.remove_sd_candidate_channels(channels)
        print(f'Removed {removed_sd_candidate_channels} SD candidate channels')
        return channels

    def match_channel_filters(self, channel):
        for channel_filter in self.channel_filters:
            match = re.search(channel_filter, channel['ChannelName'])
            if match:
                return True
        return False

    def remove_sd_candidate_channels(self, channels):
        if not self.config['guide'].getboolean('remove_sd_candidate_channels'):
            return 0
        channels_count = len(channels)
        channels[:] = [channel for channel in channels if not Guide.is_sd_candidate_channel(channel, channels)]
        new_channels_count = len(channels)
        return channels_count - new_channels_count

    @staticmethod
    def is_sd_candidate_channel(channel, channels):
        for c in channels:
            if c['ChannelName'] == channel['ChannelName'] + '高清':
                return True
        return False

    def get_playlist(self, channels):
        content = '#EXTM3U\n'
        for channel in channels:
            content += f"#EXTINF:-1 tvg-id=\"{channel['ChannelID']}\",{channel['ChannelName']}\n"
            channel_url = channel['ChannelURL']
            content += f"{channel_url}\n"
        return content

    def save_playlist(self, playlist):
        path = self.config['guide']['playlist_path']
        Guide.save_file(path, playlist)
        print(f'Playlist saved to {path}')

    @staticmethod
    def save_file(file, content):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'w') as f:
            f.write(content)
            f.close()
