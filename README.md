# TRACER

This app can be found here https://tracer-pied.vercel.app/api/analyze?url=bloomberg.com where the qeury param `url` can be set to any website.

I have only set a backend server that takes a request with the URL to be scrapped via a query parameter. The server then would use the `dnspython` library to look up the given URL contains and gather the detected sites in it. The app uses Mongodb as a storage system.

### Set up:

The set up was quite simple. I'm using Mongodb document storage in two separate collections:

1. a collection of raw results from the `dig` query
2. a collection of cleaned up version of the results from the original `dig` query

This enables me to do two things: return the cleaned version of the `dig` results from the given url, and maintain a source of truth for the exact string of each detection the URL was matched on.

### Flow:

```
Request: [ client ] → www.website.com → [ server ]

Response: [ client ] ← [ COMPANIES ] ← [ server ] →  dig lookups → [ storage ]

```

### Improvements:

1. I would have like more time to set up a frontend so this can be a more cohesive app.

2. I wanted to use more sophisticated detecting mechanism of the other sites like using Python's `request` library to parse the HTML.
