#!/bin/bash
    while :
    do
      tellyget -u $USER -p $PASSWORD -m $MACADDR -I $INTERFACE -o /output/iptv.m3u && cd /output && sed 's/^igmp.*rtsp/rtsp/' iptv.m3u > rtsp.m3u && sed 's/zoneoffset=0&icpid/icpid/' -i rtsp.m3u && python /app/rearrange_m3u.py rtsp.m3u
      sleep 3600
    done
