#!/usr/bin/env LC_ALL=en_US.UTF-8 /usr/local/bin/python3
#
# <xbar.title>Bitcoin value tracker</xbar.title>
# <xbar.version>v0.1</xbar.version>
# <xbar.author>Nicola Fiorillo</xbar.author>
# <xbar.author.github>nicolafiorillo</xbar.author.github>
# <xbar.desc>Show bitcoin/USD value getting data from https://www.coingecko.com/</xbar.desc>
# <xbar.image>https://github.com/nicolafiorillo/xbar-plugins/raw/main/images/btc_tracker.png</xbar.image>
# <xbar.dependencies>python3</xbar.dependencies>
# <xbar.abouturl>https://github.com/nicolafiorillo/xbar-plugins/blob/main/README.md</xbar.abouturl>
#
# by Nicola Fiorillo (https://www.nicolafiorillo.com, https://github.com/nicolafiorillo)
#
# Coingecko API documentation:
# https://www.coingecko.com/en/api/documentation
#

import datetime
import http.client
import json

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

def btc_vs_usd(value, percentage_diff):
    color = RED if percentage_diff < 0.0 else GREEN
    return f'1₿: ${value} ({color}{percentage_diff}%{RESET})'


def usd_vs_sat(value):
    return f'1$: {value} sats'


if __name__ == '__main__':

    percentage_diff = 0.0
    btc_usd = btc_vs_usd('--,--', percentage_diff)
    updated_at = 'n.a'
    error = False
    usd_sat = usd_vs_sat('--')

    try:
        conn = http.client.HTTPSConnection("api.coingecko.com")
        conn.request("GET", "/api/v3/simple/price?ids=bitcoin&vs_currencies=USD&include_last_updated_at=true&include_24hr_change=true", None, {"accept": "application/json"})
        response = conn.getresponse()
        if response.status != 200:
            print("Error: " + str(response.status) + " " + response.reason)
        else:
            data = json.loads(response.read())
            usd = data["bitcoin"]["usd"]
            updated_at = datetime.datetime.fromtimestamp(data["bitcoin"]["last_updated_at"])
            percentage_diff = round(data["bitcoin"]["usd_24h_change"], 1)

            btc_usd = btc_vs_usd(usd, percentage_diff)
            usd_sats = usd_vs_sat(round(100000000 / usd))
        conn.close()
    except Exception:
        error = True

    print(btc_usd)
    print('---')

    if not error:
        print(usd_sats)
        print(f'Last update: {updated_at}')
    else:
        print('Cannot get data from coingecko.com')

