import socket
import logging
import traceback

from dnslib import DNSRecord, DNSHeader, DNSQuestion, RR, A


LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 53

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        logging.error("Resolve error: %s", e)
        return None


def handle_dns_request(data, addr, sock):
    try:
        request = DNSRecord.parse(data)
        qname = str(request.q.qname)
        qtype = request.q.qtype

        logging.info("Received DNS query for: %s", qname)

        ip = resolve_domain(qname.rstrip("."))
        if not ip:
            return

        reply = DNSRecord(
            DNSHeader(id=request.header.id, qr=1, aa=1, ra=1),
            q=DNSQuestion(qname, qtype),
            a=RR(qname, rtype=qtype, rclass=1, ttl=300, rdata=A(ip))
        )

        sock.sendto(reply.pack(), addr)

    except Exception as e:
        logging.error("Failed to handle DNS request: %s, %s", e, traceback.format_exc())


def run_dns_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))
    logging.info("DNS server started on %s:%s", LISTEN_IP, LISTEN_PORT)

    while True:
        data, addr = sock.recvfrom(512)
        handle_dns_request(data, addr, sock)


if __name__ == "__main__":
    run_dns_server()
