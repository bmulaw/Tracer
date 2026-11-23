import sys
import dns.resolver

from database import store_raw, store_cleaned
from rules import extract_company_identifiers

DNS_LOOKUPS = [ "TXT", "MX", "NS" ]

def store(key: str, value: str) -> None:
    """
        Key: the key for the mongodb record
        Value: the value for the key to be stored in mongodb
    """
    cleaned_company_ids = extract_company_identifiers(value)
    store_raw(key=key, value=value)
    store_cleaned(key=key, value=cleaned_company_ids)

def run(url: str) -> None:
    """
        Url: the url to be queried for all software integrated to the site of the url
    """
    all_data_dns: list[str] = []
    for dns_type in DNS_LOOKUPS:
        # found here: https://www.dnspython.org/examples/
        txtAnswers = dns.resolver.resolve(url, dns_type, lifetime=5)
        for rdata in txtAnswers:
            all_data_dns.append(str(rdata))
            print('Host', rdata)

    store(key=url, value=all_data_dns)

# Run`python3 main.py {site_url}` on your terminal
#  ex. `python3 main.py figma.com`
if __name__ == "__main__":
    run(sys.argv[1])