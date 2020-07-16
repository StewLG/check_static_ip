# check_static_ip
Nagios check for external IPV4 static IP address. Version 1.1.

The check calls distinct separate free services to determine the external IP Address. If at least ONE matches,
the check succeeds. 

If ALL of the services fail to return the expected IP address, the check fails. The thinking is that these free services are
not 100% reliable, and come with no guarantees, so if at least one gives the expected correct IP address as an answer we assume
it's just a problem with one of the IP address service(s).

# Working example
```
python CheckStaticIP.py -eip 66.111.222.333
OK - External IP address appears to be 66.111.222.333 as expected, 3/3 IP address services succeeded
```
# Failure example 1 - all services work and agree, but IP address does not match expected
```
python CheckStaticIP.py -eip 11.22.33.44
CRITICAL - Expected 11.22.33.44, but none matched. Got following mismatching addresses or errors from IP Address services: ['66.111.222.333', '66.111.222.333', '66.111.222.333']
```
# Failure Example 2 - all services fail (internet is down for example)
```
python CheckStaticIP.py --expectedip 11.22.33.44
CRITICAL - Expected 11.22.33.44, but none matched. Got following mismatching addresses or errors from IP Address services: ['Error retrieving http://ip4only.me/api, status
 code: 404', '', 'Error retrieving https://api.ipify.org']
```
# Success, but at least one service is failing (quietly, see above)
```
python CheckStaticIP.py --expectedip 11.22.33.44
OK - External IP address appears to be 11.22.33.44 as expected, 2/3 IP address services succeeded.
```
## If you wanted to investigate the above, use the debug flag:
```
python CheckStaticIP.py --expectedip 11.22.33.44 --debug
AllResults: [False, True, True]
ErrorMessages: ['Error retrieving http://ip4only.me/api, status code: 404']
OK - External IP address appears to be 11.22.33.44 as expected, 2/3 IP address services succeeded.
```

Suggestions for additional free IPV4 IP address APIs gladly taken.