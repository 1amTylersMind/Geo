import os, sys, time


def read_file(f):

    for line in f.readlines():
        print f.name
        for file in open(line,'r').readlines():
            data = []
            for IP in file:
                data.append(IP)
    return data


def main():
    start = time.time()
    if len(sys.argv) < 2:
        os.system('cd ..;cd IP_DB; ls | while read line; do'
                  ' python cartographics.py -boot $line; done')

    else:
        if sys.argv[1] == '-boot':
            f = open(sys.argv[2],'r')
            data = read_file(f)
            print(str(len(data))+" lines in "+f.name)

    dt = time.time()
    print 'Finished the Accounting in ' + str((dt-start)/1000) + ' seconds'


if __name__ == '__main__':
    main()

