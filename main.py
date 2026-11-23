import sys
import dns.resolver

def run(url):
    # found here: https://www.dnspython.org/examples/
    answers = dns.resolver.resolve(url, 'TXT')
    for rdata in answers:
        print('Host', rdata)


if __name__ == "__main__":
    run(sys.argv[1])