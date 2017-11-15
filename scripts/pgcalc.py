import sys
import json
import urllib2
import ConfigParser
import math

def nearestPow2(aSize):
	pow2belowThreshold = 0.25
	if aSize == 0:
		return 0.0
	tmp=math.pow(2, round(math.log(aSize)/math.log(2)))
	if tmp<(aSize*(1-pow2belowThreshold)):
		tmp*=2;
	return tmp;

def populate(args):
	minValue=nearestPow2(math.floor(int(args[1])/int(args[2]))+1)
	calcValue=nearestPow2(math.floor((int(args[3])*int(args[1])*float(args[4]))/(100*int(args[2]))));
	if(minValue>calcValue):
		if args[7] == "replicated":
			print "sudo ceph osd pool create {} {} {}_ruleset_{};sudo ceph osd pool set {} size {};sudo ceph osd pool set {} min_size {};sleep 1;".format(args[5],int(minValue),args[7],args[6],args[5],args[2],args[5],args[8])
		if args[7] == "erasurecoded":
			print "sudo ceph osd pool create {} {} erasure ecprofile {}_ruleset_{}; while [ $(sudo ceph -s | grep creating -c) -gt 0 ]; do echo -n .;sleep 1; done".format(args[5],int(minValue),args[7],args[6],args[5],args[2])
	else:
		if args[7] == "replicated":
			print "sudo ceph osd pool create {} {} {}_ruleset_{};sudo ceph osd pool set {} size {};sudo ceph osd pool set {} min_size {};sleep 1;".format(args[5],int(calcValue),args[7],args[6],args[5],args[2],args[5],args[8])
		if args[7] == "erasurecoded":
			print "sudo ceph osd pool create {} {} erasure ecprofile {}_ruleset_{}; while [ $(sudo ceph -s | grep creating -c) -gt 0 ]; do echo -n .;sleep 1; done".format(args[5],int(calcValue),args[7],args[6],args[5],args[2])
if __name__ == "__main__":
	if len(sys.argv) != 9:
		print "Usage: python pgcalc.py <OSD#> <Size> <Target PGs per OSD> <%Data> <Pool Name> <Pool Root> <erasurecoded/replicated> <min_size>"
		sys.exit(0)
	populate(sys.argv)
