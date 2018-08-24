import pygeoip, sys, os, time
import PIL.Image as image
import matplotlib.pyplot as plt
import numpy as np


class Map:
    modes = {0:'US',1:'global'}
    MODE = -1
    # gi = pygeoip.GeoIP('GeoIP.dat')
    ''' Example:
    gi.country_code_by_name('google.com')
    gi.country_code_by_addr('64.233.161.99')
    gi.country_name_by_addr('64.233.161.99')
    gi = pygeoip.GeoIP('GeoIPRegion.dat')
    gi.region_by_name('apple.com')
    gi = pygeoip.GeoIP('GeoIPCity.dat')
    gi.record_by_addr('64.233.161.99')
    gi = pygeoip.GeoIP('GeoIPISP.dat')
    gi.isp_by_name('cnn.com')
    '''

    country_info = {}
    city_info = {}
    ip_info = {}

    def __init__(self, mode):
        self.MODE = self.modes[mode]
        if self.MODE == 'US':
            self.MAP = plt.imread('us_continental.jpg')
            self.labeled = plt.imread('us_labeled.jpg')
            self.showMap()

    def getIPinfo(self):
        os.system('./curious.sh >> ipdata.txt')
        ipdat = open('ipdata.txt','r')
        rawinfo = list()
        for line in ipdat.readlines():
            rawinfo.append(line)
        print(str(len(rawinfo))+" hosts scanned")

        return rawinfo

    def showMap(self):
        fig, axes = plt.subplots()
        plt.imshow(self.MAP)
        plt.show()
        plt.imshow(self.labeled)
        plt.show()
        # Get the image data of the plain map
        img = image.open('us_continental.jpg')
        imgmatrix = np.array(img)
        print(imgmatrix.shape)
        # Get the image data of the labeled map
        ref = image.open('us_labeled.jpg')
        refmat = np.array(ref)
        print(refmat.shape)


def get_http(host, decoding='utf-8'):
    """ Make HTTP GET request to host"""
    return urlopen(host).read().decode(decoding)


def geo_locate(host):
    """ Get the GeoLocation of a remote host.
    This resource was found from the Team Ultimate tool ReconDog,
    which utilizes web requests to fetch GeoIP data.
    """
    geo = "http://ipinfo.io/" + host + "/geo"

    try:
        geodat = get_http(geo)
        print(geodat)
    except:
        print('Bad IP Address! ')

def processInternetCensus():
    data = open('ipdata.txt', 'r')
    ipdata = list()
    unused = list()
    for line in data.readlines():
        try:
            if (line.split('.in-addr.arpa domain name pointer ')[1].__contains__(' not found: 3(NXDOMAIN)')):
                unused.append(line.split('.in-addr.arpa domain name pointer ')[0])
            else:
                ipdata.append(line.split('.in-addr.arpa domain name pointer ')[1])
        except:
            pass

    return ipdata,unused


def createLargerSearchSet():
    os.system('su root ./searchspace.sh >> search.txt')
    file = open('search.txt',' r')
    servers = list()
    for line in file.readlines():
        servers.append(line)
    return servers


def main():
    print('Making sure the Image libraries are installed')
    os.system('pip install scipy')
    os.system('pip install matplotlib')
    print("Building a map")
    if len(sys.argv) == 2:
        print(sys.argv[1])
        geo_locate(sys.argv[1])
    else:
        iMap = Map(0)
        start = time.time()
        # iMap.getIPinfo()
        print(str(time.time() - start)+"seconds left")

        # Now get a long list of errthing
        # But will shuffle it first because I'm not trying
        # To overload any one's servers!
        inetmap, emptydoms = processInternetCensus()
        print(str(len(inetmap))+
        " Networks dicovered from initial search")
        createLargerSearchSet()

if __name__ == '__main__':
    main()