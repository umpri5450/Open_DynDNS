;
; BIND data file for testopendyn.com
;
$TTL	604800
@	IN	SOA	ns.testopendyn.com. admin.testopendyn.com. (
			      3		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL


;address of this domain
	IN	A	192.168.1.200

;DNS Server
@	IN	NS	ns.testopendyn.com.

;hostlist
host1	IN	A	11.11.11.11

host2	IN	A	192.168.1.199
ns	IN	A	192.168.1.200

