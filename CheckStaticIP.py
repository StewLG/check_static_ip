#!/usr/bin/env python3

# Copyright (c) 2020 Stewart Loving-Gibbard

'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import argparse
import sys
import string
import requests

# Thanks kindly to whoever made this
IPV4_CHECK_URL = "http://ip4only.me/api/";

def SetupParser():
    # Build parser for arguments
    parser = argparse.ArgumentParser(description='Checks to make sure that external IP V4 address is still an expected IP address')
    parser.add_argument('-eip', '--expectedip', required=True, type=str, help='Expected IPV4 address')
    #parser.add_argument('-d', '--debug', required=False, action='store_true', help='Display debugging information; run script this way and record result when asking for help.')
    return parser;

def ExitIfNoArguments(parser):
    # if no arguments, print out help
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

def CheckIPV4StaticIP(expectedIP4Address):
    try:
        response = requests.get(IPV4_CHECK_URL);
    except:
        # Site wasn't there, internet is totally down, etc.
        print (f'CRITICAL - Problem when when trying to retrieve URL {IPV4_CHECK_URL}. Exception: {sys.exc_info()}')
        sys.exit(2);

    # Site isn't working properly, URL changed, etc.
    if (response.status_code != requests.codes.ok):
        print (f'CRITICAL - Received status code {response.status_code} when trying to retrieve URL {IPV4_CHECK_URL}')
        sys.exit(2);

    ipAddressLine = response.text;
    #print ("Result: "+ ipAddressLine);
    
    # We expect commas in the output from the web site
    if ("," not in ipAddressLine):
        print (f'CRITICAL - Got unparsable response {ipAddressLine} from {IPV4_CHECK_URL}')
        sys.exit(2);
    
    ipAddress = ipAddressLine.split(',')[1];
    #print ("IPv4: "+ ipAddress);
    if (ipAddress == expectedIP4Address):
        print (f'OK - External IP address appears to be {expectedIP4Address} as expected.')
        sys.exit(0)
    else:
        print (f'CRITICAL - IP Address was {ipAddress}, not {expectedIP4Address} as expected!')
        sys.exit(2)

def main():
    # Build parser for arguments
    parser = SetupParser();
 
    # Exit and show help if no arguments
    ExitIfNoArguments(parser);
 
    # Parse the arguments
    args = parser.parse_args(sys.argv[1:])
    
    # Check the static IPV4
    CheckIPV4StaticIP(args.expectedip);

if __name__ == '__main__':
    main()
    
