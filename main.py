import os

import dns.exception
import dns.resolver

from flask import Flask, jsonify, request
from pymongo.errors import PyMongoError

from database import store

_DNS_LOOKUPS = ["TXT", "MX", "NS"]

app = Flask(__name__)

def safe_dns_query(url: str, dns_type: str) -> list[str]:
    try:
        return [str(rdata) for rdata in dns.resolver.resolve(url, dns_type)]
    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        dns.resolver.NoNameservers,
        dns.exception.Timeout,  
    ):
        return []

def run(url: str) -> list[str]:
    """
        Url: the url to be queried for all software integrated to the site of the hostname
    """
    records: list[str] = [
        str(rdata)
        for dns_type in _DNS_LOOKUPS
        for rdata in safe_dns_query(url, dns_type)
    ]

    return store(key=url, value=records)

@app.route("/api/analyze")
def analyze():
    hostname = request.args.get('url')
    print("hostname=", hostname)
    if not hostname:
        return jsonify(error="The 'url' query param must contain a valid hostname."), 400

    try:
        companies = run(hostname)
    except dns.resolver.NXDOMAIN:
        return jsonify(error=f"No such domain: {hostname}"), 404
    except dns.exception.Timeout:
        return jsonify(error="DNS lookup timed out."), 504
    except dns.resolver.NoNameservers:
        return jsonify(error="DNS lookup failed: no nameservers responded."), 502
    except PyMongoError:
        app.logger.exception("Failed to store results for %s", hostname)
        return jsonify(error="Could not store DNS results."), 503

    return jsonify(url=hostname, companies=companies)


if __name__ == "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        debug=True
    )
