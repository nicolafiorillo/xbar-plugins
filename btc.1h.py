#!/usr/bin/env LC_ALL=en_US.UTF-8 /usr/local/bin/python3
#
# <xbar.title>Bitcoin value tracker</xbar.title>
# <xbar.version>v0.1</xbar.version>
# <xbar.author>Nicola Fiorillo</xbar.author>
# <xbar.author.github>nicolafiorillo</xbar.author.github>
# <xbar.desc>Show bitcoin/USD value getting data from https://www.coingecko.com/</xbar.desc>
# <xbar.image>https://github.com/nicolafiorillo/xbar-plugins/raw/main/images/btc_tracker.png</xbar.image>
# <xbar.dependencies>python3</xbar.dependencies>
# <xbar.abouturl>https://github.com/nicolafiorillo/xbar-plugins/raw/main/README.md</xbar.abouturl>
#
# by Nicola Fiorillo (https://www.nicolafiorillo.com, https://github.com/nicolafiorillo)

import datetime
import http.client
import json

def title(value):
    return f'BTC: ${value}'


if __name__ == '__main__':

    final = title('n.a.')
    updated_at = 'n.a'
    error = False

    try:
        conn = http.client.HTTPSConnection("api.coingecko.com")
        conn.request("GET", "/api/v3/simple/price?ids=bitcoin&vs_currencies=USD&include_last_updated_at=true", None, {"accept": "application/json"})
        response = conn.getresponse()
        if response.status != 200:
            print("Error: " + str(response.status) + " " + response.reason)
        else:
            data = json.loads(response.read())
            value = data["bitcoin"]["usd"]
            updated_at = datetime.datetime.fromtimestamp(data["bitcoin"]["last_updated_at"])

            final = title(value)
        conn.close()
    except Exception:
        error = True

    print(final)

    print('---')
    if not error:
        print(f'Last update: {updated_at}')
    else:
        print('Cannot get data read from coingecko.com')

