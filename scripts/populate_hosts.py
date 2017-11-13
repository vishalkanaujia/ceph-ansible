#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import urllib2
import ConfigParser

HOST_TYPES = ['MON', 'RGW', 'OSD', 'ALL']
IAAS_RM_INSTANCE_LIST_URI = 'http://10.33.65.0:8080/compute/v1/apps/{}/instances?view=summary'
IAAS_RM_INSTANCE_DETAILS_URI = 'http://10.33.57.71:8080/admin/v1/instance?ip='


def populate(args):
    host_type = 'ALL'
    if len(args) == 5:
        if args[4].upper() not in HOST_TYPES:
            print "Unknown host type %s, populating all host types" % (args[4])
            host_type = 'ALL'
        else:
            host_type = args[4].upper()
    Config = ConfigParser.ConfigParser(allow_no_value=True)
    cfgfile = open("../hosts/{}".format(args[3]), "w")
    Config.add_section("mons")
    Config.add_section("d1losds")
    Config.add_section("d1xlosds")
    Config.add_section("d1mosds")
    Config.add_section("i1xlosds")
    Config.add_section("d1internalosds")
    Config.add_section("d1le1osds")
    Config.add_section("rgws")
    instance_list_url = IAAS_RM_INSTANCE_LIST_URI.format(args[1])
    print "Getting: " + instance_list_url
    r = urllib2.urlopen(instance_list_url)
    data = json.load(r)
    for instance in data:
        instance_details_url = IAAS_RM_INSTANCE_DETAILS_URI + \
            instance['primary_ip']
        print "Getting: " + instance_details_url

        if 'mon-{}'.format(args[2]) in instance['hostname']:
            if host_type == 'MON' or host_type == 'ALL':
                Config.set('mons', instance['primary_ip'])

        if 'rgw-{}'.format(args[2]) in instance['hostname']:
            if host_type == 'RGW' or host_type == 'ALL':
                Config.set('rgws', instance['primary_ip'])

        if 'osd-{}'.format(args[2]) in instance['hostname']:
            if host_type != 'OSD' and host_type != 'ALL':
                continue

            mothership = json.load(urllib2.urlopen(instance_details_url))
            bareMetalId = mothership['motherShip']['bareMetalID']
            if 'Huawei' in bareMetalId:
                print("skipping " + instance['primary_ip'] +
                      " because bareMetal is " + bareMetalId)
                continue

            if instance["instance_type"] == "d1.large":
                Config.set("d1losds", instance["primary_ip"])
            if instance["instance_type"] == "d1.large.e1":
                Config.set("d1le1osds", instance["primary_ip"])
            if instance["instance_type"] == "d1.medium":
                Config.set("d1mosds", instance["primary_ip"])
            if instance["instance_type"] == "i1.xlarge":
                Config.set("i1xlosds", instance["primary_ip"])
            if instance["instance_type"] == "d1.xlarge":
                Config.set("d1xlosds", instance["primary_ip"])
            if instance["instance_type"] == "d1.internal":
                Config.set("d1internalosds", instance["primary_ip"])

    Config.write(cfgfile)
    cfgfile.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: python populate_hosts.py <appId> <clusterName> <inventory file>"
        sys.exit(0)
    populate(sys.argv)
