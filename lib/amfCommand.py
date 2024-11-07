#!/usr/bin/env python
#
# This module is part of the rtmpSnoop project
#  https://github.com/andreafabrizi/rtmpSnoop
#
# Copyright (C) 2013 Andrea Fabrizi <andrea.fabrizi@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA
#
from __future__ import print_function
import os
from lib.Logger import logger

class amfCommand():

    def __init__(self):
        self.name = ""
        self.transaction_id = 0
        self.args = list()


class amfCommands():

    def __init__(self):
        self.commands = list()
        self.RTMP = dict()
        self.RTMP["extra"] = ""

    #Adds a new amfCommand object
    def add(self, amfCmd):
        self.commands.append(amfCmd)

    #Returns the amfCommand object by the name
    def get(self, name):
        for c in self.commands:
            if c.name == name:
                return c

    #Returns the number of the objects
    def count(self):
        return len(self.commands)

    #Prints the amf command object
    def parse(self):

        try:

            #Parsing the "connect" command arguments
            amfCmd = self.get(b"connect")

            for arg in amfCmd.args:
                if type(arg) == dict:
                    for prop in arg:
                        self.RTMP[prop] = arg[prop]
                else:

                    if type(arg) == str:
                        extra_type = "S:"
                    if type(arg) == bool:
                        extra_type = "B:"
                    if type(arg) == int:
                        extra_type = "N:"

                    self.RTMP[b"extra"] += extra_type + str(arg) + " "

            #Parsing the "play" command arguments
            amfCmd = self.get(b"play")

            for arg in amfCmd.args:
                if arg:
                    self.RTMP[b"playPath"] = arg
                    break

            self.RTMP[b"url"] = os.path.join(self.RTMP[b"tcUrl"], self.RTMP[b"playPath"])

        except Exception as e:
            logger.exception(e)

    def printBar(self):
        logger.info("*************************************")

    def printOut(self, mode):
        if mode == "m3u":
            self.printM3Uentry()
        elif mode == "rtmpdump":
            self.printRTMPDump()
        else:
            self.printDefault()

    """
    Prints the stream properties using the standard list format """
    def printDefault(self):

        self.parse()
        self.printBar()

        for prop in [b"url", b"app", b"pageUrl", b"swfUrl", b"tcUrl", b"playPath", b"flashVer", b"extra"]:
            if prop in self.RTMP and len(self.RTMP[prop]) > 0:
                print("%s: %s" % (prop, self.RTMP[prop]))

        self.printBar()

    """
    Prints out the RTMP properties using the m3u format """
    def printM3Uentry(self):

        self.parse()
        self.printBar()

        print("#EXTINF:0,1, Stream")

        line = "%s " % self.RTMP["url"]

        for prop in [b"app", b"pageUrl", b"swfUrl", b"tcUrl", b"playPath"]:
            if prop in self.RTMP:
                line += "%s=%s " % (prop, self.RTMP[prop])

        if "extra" in self.RTMP:
            line += "conn=%s" % self.RTMP[b"extra"]

        line += " live=1"

        print(line)
        self.printBar()

    """
    Prints out the RTMP properties using the rtmpdump format """
    def printRTMPDump(self):

        self.parse()
        self.printBar()

        line = "rtmpdump -r '%s' " % self.RTMP[b"url"]

        if self.RTMP[b"app"]:
            line += "-a '%s' " % self.RTMP[b"app"]
        else:
            line += "-a '' "

        if self.RTMP[b"tcUrl"]:
            line += "-t '%s' " % self.RTMP[b"tcUrl"]

        if self.RTMP[b"playPath"]:
            line += "-y '%s' " % self.RTMP[b"playPath"]

        if self.RTMP[b"swfUrl"]:
            line += "-W '%s' " % self.RTMP[b"swfUrl"]

        if self.RTMP[b"pageUrl"]:
            line += "-p '%s' " % self.RTMP[b"pageUrl"]

        if self.RTMP[b"flashVer"]:
            line += "-f '%s' " % self.RTMP[b"flashVer"]

        if self.RTMP[b"extra"]:
            line += "-C %s " % self.RTMP[b"extra"]

        line += "--live -o "
        if self.RTMP[b"playPath"]:
            filename = os.path.basename(self.RTMP[b"playPath"])
            if filename:
                line += filename
            else:
                line += "stream.flv"
        else:
            line += "stream.flv"

        print(line)
        self.printBar()
