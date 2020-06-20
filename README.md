# check_static_ip
Nagios check for external IPV4 static IP address

# Working example
python CheckStaticIP.py -eip 66.111.222.333
OK - External IP address appears to be 66.111.222.333 as expected.

# Failure example
python CheckStaticIP.py -eip 11.22.33.44
CRITICAL - IP Address was 66.111.222.333, not 11.22.33.44 as expected!
