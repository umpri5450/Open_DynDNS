;
; BIND data file for testopendyn.com
;
$TTL	604800
@	IN	SOA	ns.testopendyn.com. admin.testopendyn.com. (
			7		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL


;address of this domain
	IN	A	55.55.55.1

;DNS Server
	IN	NS	ns.testopendyn.com.

;hostlist
ns	IN	A	11.11.11.11
host1	IN	A	22.22.22.22
;endhostlist
