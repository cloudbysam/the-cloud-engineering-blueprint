## Domain Name System (DNS)

Imagine having a phone book filled with numbers with no names to identify who belongs to whom—hectic, right? Now imagine that instead of typing `google.com` to browse, you had to type `142.251.216.46`, and do the same for every other website on the internet. Remembering all those random numbers would be impossible.

While we prefer to browse the internet using **Hostnames** like `google.com`, routers and computers prefer numerical **IP Addresses** (`142.251.216.46`) because they operate fundamentally on binary (0s and 1s). This is where **DNS** comes in.

The Domain Name System (DNS, RFC 1034) translates human-readable hostnames (such as `www.google.com`) into their corresponding IP addresses. Think of it like a translator in a room where a Spanish speaker and a French speaker need to communicate—they rely on someone fluent in both languages to bridge the gap.

## The Hierarchy of DNS Servers

There are three primary classes of DNS servers:
1. **Root DNS Servers:** The highest level of the DNS hierarchy.
2. **Top-Level Domain (TLD) DNS Servers:** Servers managing specific extensions like `.com`, `.org`, or `.net`.
3. **Authoritative DNS Servers:** The official servers that hold the actual IP records for a specific domain.

To see how they interact, suppose a client wants to resolve `www.amazon.com`:
- The client first contacts a **Root Server**, which returns the IP address for the `.com` TLD servers.
- The client then contacts a **TLD Server**, which returns the IP address of Amazon's authoritative name servers.
- Finally, the client contacts an **Authoritative Server** for Amazon, which provides the actual IP address for `www.amazon.com`.

## Break down of the steps
- **The Root (.):** Asks the master world servers where `.com` lives.
- **The TLD (.com):** Asks the `.com` servers where `amazon.com` is registered.
- **The Name Servers:** Finds Amazon's official master DNS servers.
- **The Authoritative Servers:** Gets the actual IP address of `amazon.com`.

To see how DNS translates the hostname to an IP address in action, run `dig @1.1.1.1 amazon.com +trace` in your terminal. You will get output similar to this:

```bash
; <<>> DiG 9.18.39-0ubuntu0.24.04.7-Ubuntu <<>> @1.1.1.1 amazon.com +trace
; (1 server found)
;; global options: +cmd
.                     516389  IN      NS      a.root-servers.net.
.                     516389  IN      NS      b.root-servers.net.
.                     516389  IN      NS      c.root-servers.net.
.                     516389  IN      NS      d.root-servers.net.
.                     516389  IN      NS      e.root-servers.net.
                      516389  IN      RRSIG   NS 8 0 518400 20260930210000 20260917200000 57780 . wi9KM0lK29OSiYp3WEHv0KbeZbPw4hDpPEscAPmk5R10UuZa7ACYNRu0 nSQKW26tvqcZFa+XRYW+XfRhQWgzDCjfbSPKADxByD8+sP8CPS8tSjic STf3mOi7Nm2w/yKwpw+SO7zTDgobiD6gkYsjpiep8P2PVR9MDudZfCQ0 SwK6dPl6V7y+CrcuLFqfbvPYYqcHQO2ocZfEMGL6xs6Xio5kTM4y235z yFvaL3jVI4GqkurV2V5rSPV6Jz7L/UP5ELEmLMzwIh4/GM+SpphbIFl9 /LsXao0izpEQ3zrMSTmoM/vbiosSBhgdXd/J32aXyyUwlUhHpkTo2q7x 80gdBw==
;; Received 525 bytes from 1.1.1.1#53(1.1.1.1) in 51 ms
com.                    172800  IN      NS      e.gtld-servers.net.
com.                    172800  IN      NS      m.gtld-servers.net.
com.                    86400   IN      DS      19718 13 2 8ACBB0CD28F41250A80A491389424D341522D946B0DA0C0291F2D3D7 71D7805A
com.                    86400   IN      RRSIG   DS 8 1 86400 20260930210000 20260917200000 57780 . D0CPq+8DNVmk0i1YjWBaZu1J1YDNKyHIKz0/ktamMgHwkf6bJeqZB5dO rC+U+v/6beTZFR/xfMNwOUKftEl5f9d5t8fMJJrsVpIvXsumRkIeP+0N QXmTOZc3HyieX2GWKjfwoV7fjOtticEp1VfQWqf29hqnRWE8MUQm+VUi yysoOOhzdKVU+SxWQu0fh7zoH+JHlLSIQS4JgP1F8RhAP3WO7x+MKvMJ eLGWNTm/eMbAyUGQCKZjZdnLcDLEtA5RiR/M4H2AdFj7eujb0KbsOt9C mgR9aGDszzwsB0wf8ivbjsRNubXeOI7dJ5XwdlwL60ACPuMx4BEv56rl 5jaZ9g==
;; Received 1170 bytes from 199.7.83.42#53(l.root-servers.net) in 155 ms

amazon.com.             172800  IN      NS      ns-521.awsdns-01.net.
amazon.com.             172800  IN      NS      ns-264.awsdns-33.com.
amazon.com.             172800  IN      NS      ns-1707.awsdns-21.co.uk.
amazon.com.             172800  IN      NS      ns-1447.awsdns-52.org.
amazon.com.             172800  IN      NS      ns-1447.awsdns-52.org.
CK0POJMG874LJREF7EFN8430QVIT8BSM.com. 900 IN NSEC3 1 1 0 - CK0Q35HRS4H76G6CHNB9414CJN6S5UPL NS SOA RRSIG DNSKEY NSEC3PARAM
CK0POJMG874LJREF7EFN8430QVIT8BSM.com. 900 IN RRSIG NSEC3 13 2 900 20260923002559 20260915231559 41446 com. SW9E4N4uyc81uZIXCjCAfOCX2gk8jvJ074NSYi6jbd8BcQRi985h4fay 7M/ocD5JAuVYyk6M9H4xPILTDKAFzg==
K200V84I256ANM893J2Q7LOV6CAIURDF.com. 900 IN NSEC3 1 1 0 - K201KNR33BBBF7ESFVA94JV96315189D NS DS RRSIG
K200V84I256ANM893J2Q7LOV6CAIURDF.com. 900 IN RRSIG NSEC3 13 2 900 20260923015436 20260916004436 41446 com. 21ImGHf5XppAvBh108M36wkIRBTX21uVH9Xi0OEz3hWaATlWzslRkhun UeJeVCS8UqR6Zncsmtllld6UYs96lw==
;; Received 577 bytes from 192.31.80.30#53(d.gtld-servers.net) in 200 ms

amazon.com.             900     IN      A       98.82.161.185
amazon.com.             900     IN      A       98.87.170.71
amazon.com.             900     IN      A       98.87.170.74
amazon.com.             7200    IN      NS      ns-1447.awsdns-52.org.
amazon.com.             7200    IN      NS      ns-1707.awsdns-21.co.uk.
amazon.com.             7200    IN      NS      ns-264.awsdns-33.com.
amazon.com.             7200    IN      NS      ns-521.awsdns-01.net.
;; Received 224 bytes from 205.251.198.171#53(ns-1707.awsdns-21.co.uk) in 140 ms
```

## Additional DNS Services
Beyond basic hostname-to-IP translation, DNS also provides:
- **Host aliasing:** Mapping canonical hostnames to alternate alias names (CNAME records).
- **Mail server aliasing:** Directing mail exchanges for a domain (MX records).
- **Load distribution:** Distributing traffic across multiple replica IP addresses for a single hostname (Multiple A records / Round-robin DNS).

---

## Key RFCs & References

* [RFC 1034: Domain Names - Concepts and Facilities](https://datatracker.ietf.org/doc/html/rfc1034) - The foundational specification detailing DNS domain hierarchy and query models.
* [RFC 1035: Domain Names - Implementation and Specification](https://datatracker.ietf.org/doc/html/rfc1035) - Core specification defining DNS message formats, record types (A, NS, CNAME, MX), and master file formats.
* [RFC 2181: Clarifications to the DNS Specification](https://datatracker.ietf.org/doc/html/rfc2181) - Updates TTL handling, name authority rules, and response code behaviors.
* [RFC 4033: DNS Security Introduction and Requirements](https://datatracker.ietf.org/doc/html/rfc4033) - Introduces DNSSEC mechanisms for authenticating DNS data origins (explaining records like `RRSIG` and `DS` in recursive traces).
* [IANA Root Zone Database](https://www.iana.org/domains/root/db) - Official directory of all top-level domains and root name server delegations.