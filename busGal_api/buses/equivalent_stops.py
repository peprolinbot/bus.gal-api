# These aren't all of them. Open an issues if you find more or you know how to automate this.
equivalent_stops = {
    13035: 20,
    38917: 12562,
    38906: 35416,
    73: 13220,
    46466: 38911,
    38926: 38924,
    35433: 35428,
    38853: 35434,
    35429: 38768,
    35430: 13067,
    13134: 35413,
    35418: 2768,
    35414: 733,
    8919: 38774
}

equivalent_stops.update(
    dict(zip(equivalent_stops.values(), equivalent_stops.keys())))
