#!/usr/bin/env python3

import requests
import sys

def fetch_exchange_rates(app_id):
    api_url = 'https://openexchangerates.org/api/latest.json'
    params = {'app_id': app_id}

    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        print('Failed to fetch exchange rates. Status code:', response.status_code)
        sys.exit(1)

    data = response.json()
    return data['rates']

def convert_currency(amount, source_rate, target_rate):
    converted_amount = amount * (1 / source_rate) * target_rate
    return round(converted_amount, 2)

def main():
    if len(sys.argv) != 4:
        print('Usage: python3 script.py <amount> <source_currency> <target_currency>')
        sys.exit(1)

    try:
        amount = float(sys.argv[1])
    except ValueError:
        print('Error: First argument must be a valid amount.')
        sys.exit(1)

    source_currency = sys.argv[2].upper()
    target_currency = sys.argv[3].upper()

    app_id = 'ENTER OPENEXCHANGERATES APP ID HERE'
    exchange_rates = fetch_exchange_rates(app_id)

    if source_currency not in exchange_rates or target_currency not in exchange_rates:
        print('Error: Invalid source or target currency.')
        sys.exit(1)

    source_rate = exchange_rates[source_currency]
    target_rate = exchange_rates[target_currency]

    converted_amount = convert_currency(amount, source_rate, target_rate)
    print(f'{amount:.2f} {source_currency} is equivalent to {converted_amount:.2f} {target_currency}')

if __name__ == "__main__":
    main()
