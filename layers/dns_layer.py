def resolve_dns(domain):
    import time
    import dns.resolver

    start = time.time()
    answer = dns.resolver.resolve(domain, "A")
    latency = (time.time() - start) * 1000

    ttl = answer.rrset.ttl

    cache = {
        "status": "cache_hit" if ttl > 60 else "cache_miss",
        "reason": "High TTL suggests cached response" if ttl > 60 else "Low TTL suggests fresh lookup"
    }

    return {
        "status": "ok",
        "ips": [rdata.address for rdata in answer],
        "latency": latency,
        "ttl": ttl,
        "cache": cache
    }
