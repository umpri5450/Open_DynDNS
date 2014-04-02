;
; BIND data file for testopendyn.com
;

$TTL	604800
@	IN	SOA	ns1.testopendyn.com. admin.testopendyn.com. (
			3		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL


;address of this domain
	IN	A	33.33.33.1

;DNS Server
@	IN	NS	ns1.testopendyn.com.

;hostlist
toto	IN	A	33.33.33.50
ns1	IN	A	33.33.33.1
kiki	IN	A	1.1.1.3
lala	IN	A	2.2.2.4
fala	IN	A	3.3.3.4
shitty	IN	A	4.4.4.5
host1	IN	A	11.11.11.11
;endhostlist

