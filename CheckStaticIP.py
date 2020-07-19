#!/usr/bin/env python3

# Copyright (c) 2020 Stewart Loving-Gibbard

# https://github.com/StewLG/check_static_ip

# Version 1.2

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
import time


# The true/false result of every service checked. If True, the IP address matched the expected one.
AllResults = []
# Only error messages/problems retrieving values.
ErrorMessages = []

def SetupParser():
    # Build parser for arguments
    parser = argparse.ArgumentParser(description='Checks to make sure that external IP V4 address is still an expected IP address')
    parser.add_argument('-eip', '--expectedip', required=True, type=str, help='Expected IPV4 address')
    parser.add_argument('-d', '--debug', required=False, action='store_true', help='Display debugging information; run script this way and record result when asking for help.')
    parser.add_argument('-t', '--timeout', required=False, type=int, help='Timeout in seconds. This is the maximum amount of time in seconds to wait for any particular IP address service. If set to 10 the check will wait up to 10 second per service. The default is an indefinite timeout.')
    return parser;

def ExitIfNoArguments(parser):
    # if no arguments, print out help
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

# IP4Only
IPV4_CHECK_URL = "http://ip4only.me/api";

def GetIPAddress_IP4OnlyDotMe(timeoutInSeconds, shouldShowDebugInfo):
    try:
        if (shouldShowDebugInfo):
            print (f"Fetching from {IPV4_CHECK_URL}")
        response = requests.get(IPV4_CHECK_URL, timeout=timeoutInSeconds);
    except:
        # Site wasn't there, internet is totally down, etc.
        return f"Error retrieving {IPV4_CHECK_URL}"

    # Site isn't working properly, URL changed, etc.
    if (response.status_code != requests.codes.ok):
        return f"Error retrieving {IPV4_CHECK_URL}, status code: {response.status_code}"

    ipAddressLine = response.text;

    # We expect commas in the output from the web site
    if ("," not in ipAddressLine):
        return f"Got unparsable response {ipAddressLine} from {IPV4_CHECK_URL}"
    
    ipAddress = ipAddressLine.split(',')[1]; 
    return ipAddress;


# http://ipv4bot.whatismyipaddress.com/
WHAT_IS_MY_IP_ADDRESS_CHECK_URL = "http://ipv4bot.whatismyipaddress.com";

def GetIPAddress_WhatIsMyIPAddressDotCom(timeoutInSeconds, shouldShowDebugInfo):
    try:
        if (shouldShowDebugInfo):
            print (f"Fetching from {WHAT_IS_MY_IP_ADDRESS_CHECK_URL}")
        response = requests.get(WHAT_IS_MY_IP_ADDRESS_CHECK_URL, timeout=timeoutInSeconds);
    except:
        # Site wasn't there, internet is totally down, etc.
        return f"Error retrieving {WHAT_IS_MY_IP_ADDRESS_CHECK_URL}"

    # Site isn't working properly, URL changed, etc.
    if (response.status_code != requests.codes.ok):
        return f"Error retrieving {WHAT_IS_MY_IP_ADDRESS_CHECK_URL}, status code: {response.status_code}"

    # This service is simple, no CSV or JSON - just the raw IP address
    ipAddress = response.text;
 
    return ipAddress;
    
# https://api.ipify.org
IPIFY_CHECK_URL = "https://api.ipify.org";

def GetIPAddress_IPify(timeoutInSeconds, shouldShowDebugInfo):
    try:
        if (shouldShowDebugInfo):
            print (f"Fetching from {IPIFY_CHECK_URL}")
        response = requests.get(IPIFY_CHECK_URL, timeout=timeoutInSeconds);
    except:
        # Site wasn't there, internet is totally down, etc.
        return f"Error retrieving {IPIFY_CHECK_URL}"

    # Site isn't working properly, URL changed, etc.
    if (response.status_code != requests.codes.ok):
        return f"Error retrieving {IPIFY_CHECK_URL}, status code: {response.status_code}"

    # This service supports JSON etc, but the simple version with just the IP is fine.
    ipAddress = response.text;

    return ipAddress;

def AddResultsAndAnyErrors(expectedIP4Address, resultString):
    currentResult = resultString == expectedIP4Address;
    AllResults.append(currentResult);
    if (not currentResult):
        ErrorMessages.append(resultString);

def CheckAllExternalIPV4Providers(expectedIP4Address, timeoutInSeconds, shouldShowDebugInfo):

    startTime = time.time()

    AddResultsAndAnyErrors(expectedIP4Address, GetIPAddress_IP4OnlyDotMe(timeoutInSeconds, shouldShowDebugInfo))
    AddResultsAndAnyErrors(expectedIP4Address, GetIPAddress_WhatIsMyIPAddressDotCom(timeoutInSeconds, shouldShowDebugInfo))
    AddResultsAndAnyErrors(expectedIP4Address, GetIPAddress_IPify(timeoutInSeconds, shouldShowDebugInfo))

    endTime = time.time();
    elapsedTimeInSeconds = (endTime - startTime);

    # Did at least one service match our expected IP address?
    atLeastOnePositiveResult = any(AllResults);
    # How many services did we check?
    totalServicesChecked = len(AllResults);
    # How many services succeeded?
    totalServicesSucceeded = AllResults.count(True);

    if (shouldShowDebugInfo):
        print(f"AllResults: {AllResults}")
        print(f"ErrorMessages: {ErrorMessages}")
    
    if (atLeastOnePositiveResult):
        print (f'OK - External IP address appears to be {expectedIP4Address} as expected, {totalServicesSucceeded}/{totalServicesChecked} IP address services succeeded. Elapsed time: {elapsedTimeInSeconds:.2f} seconds.')
        sys.exit(0)
    
    # No matching results? Indicate failure and print out errors for debugging.
    if (not atLeastOnePositiveResult):
        print (f'CRITICAL - Expected {expectedIP4Address}, but none matched. Got following mismatching addresses or errors from IP Address services: {ErrorMessages}. Elapsed time: {elapsedTimeInSeconds:.2f} seconds.');
        sys.exit(2);


def main():

    # Build parser for arguments
    parser = SetupParser();
 
    # Exit and show help if no arguments
    ExitIfNoArguments(parser);
 
    # Parse the arguments
    args = parser.parse_args(sys.argv[1:])
    
    # Check the static IPV4
    CheckAllExternalIPV4Providers(args.expectedip, args.timeout, args.debug);

if __name__ == '__main__':
    main()
    
