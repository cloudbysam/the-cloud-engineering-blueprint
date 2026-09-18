# IP Address

The most used protocol in the network/internet layer is the **Internet Protocol (IP)**. It is a set of rules responsible for delivering data packets from a source IP address to a destination IP address. The IP address uniquely identifies the source and destination of data packets across the network and helps routers route this information from one place to another.

An IPv4 address is 32 bits long. A bit consists of either a `1` or a `0`, meaning every IP address is a combination of 32 binary digits. We take those 32 bits, break them up into four chunks called **octets** (8 bits each), and convert each octet into a **decimal number**. The smallest binary number you can get with 8 bits is `0` and the largest is `255`.

```text
10001000000101100001000101100010 - 32-bit Binary String
10001000 . 00010110 . 00010001 . 01100010 - Four Octets
  136    .    22    .    17    .    98   - Decimal - IP Address

```  

# Subnetting

Subnetting is the process of taking a network and dividing it into smaller sub-networks.

## Attributes of subnetting
- Network ID: Identifies the specific network segment.
- Broadcast IP: Used to transmit data to all devices on the network.
- First Host IP: The lowest usable IP address for a device.
- Last Host IP: The highest usable IP address for a device.
- Next Network: The starting address of the subsequent subnet.
- CIDR / Subnet Mask: Defines the network and host boundaries.

Note: The Network ID and Broadcast IP are reserved and cannot be assigned to individual hosts within the IP block.

## Subnet Mask vs. CIDR
When learning networking, it is easy to get confused between Subnet Masks and CIDR notation because they perform the exact same job: they tell a computer where the network portion of an IP address ends and where the host (device) portion begins.

The only difference is how they are written:

- subnet mask: `255.255.255.0`
- CIDR (classless inter-domain routing): `/24` (representing 1st-24 bits locked for the network)

Think of it like writing a date. Subnet Mask is writing out `September 18, 2026` while CIDR is writing `18/09/26`. They point to the exact same day, but one is much faster to write.  

---

**Key RFCs & References to add at the bottom:**
* [RFC 791: Internet Protocol (IPv4)](https://datatracker.ietf.org/doc/html/rfc791) - The core specification for IPv4 addressing and packet headers.
* [RFC 4632: Classless Inter-domain Routing (CIDR)](https://datatracker.ietf.org/doc/html/rfc4632) - The standard defining CIDR architecture, address assignment, and aggregation strategies.