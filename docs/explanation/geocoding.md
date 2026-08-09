# About geocoding and IP-based location

idfkit can turn a street address, or the machine's own network location, into
the `(latitude, longitude)` pair that [`StationIndex.nearest()`](../weather/station-search.md)
needs. This page explains what the two services behind that convenience are,
what they cost you, and where their limits lie — so you can decide when to lean
on them and when to supply coordinates yourself. For the runnable recipes, see
[How to geocode addresses](../weather/geocoding.md).

## Two services, two trade-offs

`geocode(address)` calls [Nominatim](https://nominatim.org/), the free
OpenStreetMap geocoder. `detect_location()` calls [ipapi.co](https://ipapi.co/)
and infers coordinates from the machine's public IP. Both are free and need no
API key, which is what makes them convenient defaults — but "free and keyless"
is a design choice with consequences, not a free lunch.

Because there's no account, there's no service-level agreement: you're a guest
on shared infrastructure. Nominatim's usage policy asks for **at most one
request per second** and discourages bulk geocoding; `geocode()` serializes
calls to honour that limit for you. If you need to
geocode thousands of addresses, that etiquette is the wrong tool — a paid batch
geocoding service exists precisely so you don't hammer a community resource.

## Accuracy is coarser than it looks

Neither service is a survey instrument, and treating their output as exact
coordinates is the usual mistake.

- **Address geocoding** is only as good as the address you give it and the
  OpenStreetMap data behind it. A full street address in a well-mapped city
  resolves tightly; a partial or ambiguous one may land on a city centroid.
  Results can also shift slightly over time as OpenStreetMap is edited.
- **IP geocoding** is **city-level at best**. That is more than enough to pick a
  TMYx weather station within ~50 km — which is all idfkit uses it for — but it
  is not positioning, and a VPN or corporate network can place you in another
  city or country entirely.

For anything where being in the wrong place is costly, verify the coordinates
before you rely on them, or skip geocoding and pass the numbers directly.

## What leaves your machine

`geocode()` sends the address string to Nominatim over HTTPS. `detect_location()`
sends your machine's public IP address to ipapi.co over HTTPS. If you'd rather
not disclose either, the escape hatch is always available: call
`geocode("city, country")` with a deliberately coarse query, or supply
`(lat, lon)` yourself and make no network call at all.

Results are cached on the local filesystem — Nominatim lookups and the
IP-location result (the latter for one hour by default) — under idfkit's weather
cache directory. That cache is purely a local file; nothing about your queries
is sent anywhere beyond the two services named above.

## When to reach for each

- You have a **known address** → `geocode()`.
- You want **"weather near me"** with no input → `detect_location()`.
- You already know the coordinates, or you're running **at scale**, or you can't
  send addresses/IPs to a third party → skip both and pass `(lat, lon)`
  directly.

## See also

- [How to geocode addresses](../weather/geocoding.md) — the runnable recipes
- [How to search for weather stations](../weather/station-search.md) — where the
  coordinates get used
