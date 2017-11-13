#!/usr/bin/python

from __future__ import division
import yaml
import sys
import os
import math

if len(sys.argv) != 2:
	print "Usage: generate_rate_limits.py <num_hosts>"
	exit()

fname = "../files/rate_limits/rgw-rate-limit." + os.environ["D42_CLUSTER_TYPE"] +".yml"
outname = "../files/rate_limits/rgw-rate-limit-per-node." + os.environ["D42_CLUSTER_TYPE"] +".yml"
num_hosts = int(sys.argv[1])

print os.environ["D42_APPID"]
if os.environ["D42_APPID"] == "stage-d42sa": 
    num_rd_hosts = num_hosts
    num_wr_hosts = num_hosts
elif os.environ["D42_APPID"] == "prod-d42sa":
    num_rd_hosts = 13
    num_wr_hosts = 9
else:
    print "D42_APPID is not defined correctly"
    exit()
    

try:
    stream = open(fname, 'r')
except:
    exit(1)
    
data = yaml.load(stream)

try:
    outfile = open(outname, 'w')
except:
    print "File open of {} Failed".format(outname)
    exit()


if data is not None:
    for i in range(len(data)):
        try:
            outfile.write("- user: {}\n".format(data[i]['user']))
            if 'object' in data[i]:
                outfile.write("  object: \n")
                if 'get' in data[i]['object']:
                    outfile.write("    get:\n")
                    if data[i]['object']['get']['limit'] is not None and data[i]['object']['get']['period'] is not None:
                        outfile.write("      limit: {}\n".format(int(math.ceil(data[i]['object']['get']['limit']/num_rd_hosts))))
                        outfile.write("      period: {}\n".format(data[i]['object']['get']['period']))
                    else:
                        print "ERROR: limit and period both should be there"
                        exit(1)
            
                if 'put' in data[i]['object']:
                    outfile.write("    put:\n")
                    if data[i]['object']['put']['limit'] is not None and data[i]['object']['put']['period'] is not None:
                        outfile.write("      limit: {}\n".format(int(math.ceil(data[i]['object']['put']['limit']/num_wr_hosts))))
                        outfile.write("      period: {}\n".format(data[i]['object']['put']['period']))
                    else:
                        print "ERROR: limit and period both should be there"
                        exit(1)

                if 'delete' in data[i]['object']:
                    outfile.write("    delete:\n")
                    if data[i]['object']['delete']['limit'] is not None and data[i]['object']['delete']['period'] is not None:
                        outfile.write("      limit: {}\n".format(int(math.ceil(data[i]['object']['delete']['limit']/num_wr_hosts))))
                        outfile.write("      period: {}\n".format(data[i]['object']['delete']['period']))
                    else:
                        print "ERROR: limit and period both should be there"
                        exit(1)

            if 'bucket' in data[i]:
                outfile.write("  bucket: \n")
                if 'create' in data[i]['bucket']:
                    outfile.write("    create:\n")
                    if data[i]['bucket']['create']['limit'] is not None and data[i]['bucket']['create']['period'] is not None:
                        outfile.write("      limit: {}\n".format(int(math.ceil(data[i]['bucket']['create']['limit']/num_wr_hosts))))
                        outfile.write("      period: {}\n".format(data[i]['bucket']['create']['period']))
                    else:
                        print "ERROR: limit and period both should be there"
                        exit(1)
                        
                if 'delete' in data[i]['bucket']:
                    outfile.write("    delete:\n")
                    if data[i]['bucket']['delete']['limit'] is not None and data[i]['bucket']['delete']['period'] is not None:
                        outfile.write("      limit: {}\n".format(int(math.ceil(data[i]['bucket']['delete']['limit']/num_wr_hosts))))
                        outfile.write("      period: {}\n".format(data[i]['bucket']['delete']['period']))
                    else:
                        print "ERROR: limit and period both should be there"
                        exit(1)
            outfile.write("\n")       
        except Exception as e:
            print "ERROR: {}".format(str(e))
            exit(1)

outfile.close()
