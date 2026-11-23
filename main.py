import sys
import dns.resolver

from database import store_object

DNS_LOOKUPS = [ "TXT", "MX", "NS" ]

def run(url: str) -> None:
    """
        Url: the url to be queried for all software integrated to the site of the url
    """
    all_data_dns = []
    for dns_type in DNS_LOOKUPS:
        # found here: https://www.dnspython.org/examples/
        txtAnswers = dns.resolver.resolve(url, dns_type, lifetime=5)
        for rdata in txtAnswers:
            all_data_dns.append(rdata)
            print('Host', rdata)

    store_object(key=url, value=all_data_dns)

if __name__ == "__main__":
    run(sys.argv[1])