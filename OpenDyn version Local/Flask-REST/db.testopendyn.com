;
; BIND data file for testopendyn.com
;

$TTL	604800
			8		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL


;address of this domain
	IN	A	33.33.33.1

;DNS Server

;hostlist
;endhostlist

