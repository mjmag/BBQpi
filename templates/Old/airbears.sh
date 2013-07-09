#!/bin/bash
if [[ `ping -c 1 google.com | awk '/packets received/ {print $4}'` = "0" ]]; then
curl https://auth.berkeley.edu/cas/login?service=https%3a%2f%2fwlan.berkeley.edu%2fcgi-bin%2flogin%2fcalnet.cgi%3fsubmit%3dCalNet%26url%3d -silent | awk '/ type="hidden" name="lt" value="/ {print $0 }' | sed 's/^.*type=\"hidden\" name=\"lt\" value=\"\([^\"].*\)\".*$/username=mariom\&password=Mario%20rocks!\&_eventId=submit\&lt=\1/' | sed 's/[ ]/+/' | curl https://auth.berkeley.edu/cas/login?service=https%3a%2f%2fwlan.berkeley.edu%2fcgi-bin%2flogin%2fcalnet.cgi%3fsubmit%3dCalNet%26url%3d -silent -c cookiejar.txt -L --data @- | awk '/Authentication complete./ {print $0}' | sed "s/^.*\(Authentication[^<]*\)<p.*$/\1/"
fi
rm /var/www/cgi-bin/ipaddress
curl https://icanhazip.com >>/var/www/cgi-bin/ipaddress

