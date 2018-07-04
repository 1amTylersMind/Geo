#!/usr/bin/env python
import sys
from urllib2 import urlopen
from urllib2 import URLError
from scapy.all import *
"""
PhysicalTracer 
Is designed for users to allow location to quickly be included with a traceroute. 
"""


class PhysicalTracer:

    end = ""

    def __init__(self, mode, endpoint):
        self.end = endpoint
        if mode == 'trace':
            self.start_trace(endpoint)
            ParseTrace('trace.txt')
        if mode == 'geo':
            self.geo_locate(endpoint)

    @staticmethod
    def get_http(host, decoding='utf-8'):
        """ Make HTTP GET request to host"""
        return urlopen(host).read().decode(decoding)

    def geo_locate(self, host):
        """ Get the GeoLocation of a remote host.
        This resource was found from the Team Ultimate tool ReconDog,
        which utilizes web requests to fetch GeoIP data.
        """
        geo = "http://ipinfo.io/" + host + "/geo"

        try:
            geodat = self.get_http(geo)
            print(geodat)
        except URLError:
            print('Bad IP Address! ')

    def start_trace(self, host):
        """
        Run a Traceroute to host using scapy
        :param host:
        :return: nothing
        """
        traceroute(host)


class ParseTrace:

    def __init__(self, trace_file):

        file_contents = self.parse_trace(trace_file)
        ip_addresses = self.extract_data(file_contents)

    @staticmethod
    def parse_trace(trace_file):
        f = open(trace_file, 'r')
        content = f.read(1024)
        # print(content)
        size = len(content)
        words = []
        stringbuilder = ""
        for letters in content:
            if letters == '\n':
                words.append(letters)
            elif letters != ' ':
                stringbuilder += letters
            if letters == ' ':
                words.append(stringbuilder)
                stringbuilder = ""
        return words

    @staticmethod
    def extract_data(contents):
        ips = []
        for word in contents:
			ips.append(word)
        return ips

def menu(opt):
    selection = ''
    if opt == '-trace':
        selection = 'trace'
    if opt == '-geo':
        selection = 'geo'
    return selection


def main():
    PhysicalTracer(menu(sys.argv[1]), sys.argv[2])
    #ParseTrace('trace.txt')


if __name__ == '__main__':
    main()
