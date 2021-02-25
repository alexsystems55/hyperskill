import requests


def get_rate(dst_cur: str) -> None:
    """
    Get rate from loaded JSON and cache it

    :param dst_cur:
    :return:
    """
    if src_currency == dst_cur:
        rates_cache[dst_cur] = 1
    else:
        try:
            rates_cache[dst_cur] = response.json()[dst_cur]["rate"]
        except KeyError:
            print("No such currency in the list!")


rates_cache = {}
src_currency = input().lower()

# Download JSON with rates
url = f"http://www.floatrates.com/daily/{src_currency}.json"
response = requests.get(url)
if response.status_code != 200:
    print(f"HTTP error {response.status_code}")
    exit(-1)

# Precache popular currencies
for cur in ("eur", "usd"):
    get_rate(cur)

# Main loop
while True:
    dst_currency = input().lower()
    if dst_currency == "":
        break
    amount = int(input())
    print("Checking the cache…")
    if dst_currency in rates_cache:
        print("Oh! It is in the cache!")
    else:
        print("Sorry, but it is not in the cache!")
        get_rate(dst_currency)
    received = round(rates_cache[dst_currency] * amount, 2)
    print(f"You received {received} {dst_currency.upper()}.")
