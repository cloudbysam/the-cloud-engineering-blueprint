# Communication Models 

For machines to communicate over the internet, they follow certain rules, referred to as **Communication Protocols**. There are different communication protocols operating at different layers in the **Communication models**. The layers in a communication model represent how data travels from one location to another across the internet in a reliable way. 

The two communication models responsible for defining how data is transported across the internet are the **Open Systems Interconnection (OSI)** model and the **TCP/IP** model."

---

## OSI Model

The OSI model is a **reference model** that divides the communication network into seven layers. It is mostly used as a teaching tool to help engineers understand and troubleshoot networks.

## TCP/IP

**Internet communication** happens via the TCP/IP model. The TCP/IP model, also referred to as the internet protocol suite, mainly includes TCP ([RFC 793](https://www.ietf.org/rfc/rfc793.txt)), IP, and UDP. The TCP/IP model combines multiple layers of the OSI model into one layer to execute similar functionality.

---

## The 7-Layer OSI to 4-Layer TCP/IP Comparison

| OSI Model Layer | | TCP/IP Model Layer | Common Protocols | Layer Responsibility (One-Line Definition) |
| :--- | :---: | :--- | :--- | :--- |
| Application Layer | ┐ | | | Network services for user applications (end-user interaction). |
| Presentation Layer | ├─> | Application Layer | HTTP, HTTPS, FTP, SMTP, DNS, SSH, DHCP | Data formatting, encryption, decryption, and compression. |
| Session Layer | ┘ | | | Establishes, manages, and terminates sessions between applications. |
| Transport Layer | ──> | Transport Layer | TCP, UDP | Breaks data into segments for reliable delivery. |
| Network Layer | ──> | Network Layer | IP (IPv4/IPv6), ICMP, ARP, OSPF | Packages segments into packets and determines the best physical path for them (routing and IP addressing). |
| Data Link Layer | ┌─> | Network Access Layer | Ethernet, Wi-Fi (802.11), PPP | Defines packet framing, MAC addressing, and error-free local links. |
| Physical Layer | ┘ | | Cables, Fiber Optics, Hubs, Bits | Transmits raw unstructured binary data over a physical medium. |


## Visual Breakdown
- The top three OSI layers (**Application, Presentation, Session**) combine into the single TCP/IP **Application Layer**.
- The **Transport** and **Network** layers map directly one-to-one between both models.
- The bottom two OSI layers (**Data Link, Physical**) combine into the single TCP/IP **Network Access Layer**.

## Reference
* [RFC 1122: Requirements for Internet Hosts — Communication Layers](https://datatracker.ietf.org/doc/html/rfc1122) - The standard detailing the 4-layer TCP/IP architectural model and layer interaction rules.
* [IETF Internet Standards Directory](https://www.rfc-editor.org/search/?status=internet+standard) - Official index of active RFC standards governing internet protocols.
* [RFC 793: Transmission Control Protocol](https://www.ietf.org/rfc/rfc793.txt) - The original specification defining TCP operation and header structure.