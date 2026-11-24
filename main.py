import sys
import dns.resolver

from database import store

_DNS_LOOKUPS = [ "TXT", "MX", "NS" ]


def run(url: str) -> None:
    """
        Url: the url to be queried for all software integrated to the site of the url
    """
    all_data_dns: list[str] = [
        str(rdata)
        for dns_type in _DNS_LOOKUPS
        for rdata in dns.resolver.resolve(url, dns_type)
    ]

    print('Host', all_data_dns)
    store(key=url, value=all_data_dns)

# Run`python3 main.py {site_url}` on your terminal
#  ex. `python3 main.py figma.com`
if __name__ == "__main__":
    run(sys.argv[1])