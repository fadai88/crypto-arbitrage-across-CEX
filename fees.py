import requests
from bs4 import BeautifulSoup

def fetch_withdrawal_fees(exchange, coin_symbol):
    url = f'https://withdrawalfees.com/exchanges/{exchange}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        
        if not table:
            raise ValueError("Table not found on the page")
        
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) > 1:
                symbol_div = columns[0].find('div', class_='symbol')
                if symbol_div and symbol_div.text.strip() == coin_symbol:
                    withdrawal_fee_div = columns[1].find('div', class_='fee')
                    if withdrawal_fee_div:
                        withdrawal_fee = withdrawal_fee_div.text.strip()
                        try:
                            return float(withdrawal_fee.split()[0])
                        except ValueError:
                            return withdrawal_fee  # Return as string if not a number
        
        print(f"{coin_symbol} not found on {exchange} at withdrawalfees.com.")
        return None
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# fetch_withdrawal_fees('binance', 'MINA')


import time
import hashlib
import hmac
import json

def gen_sign(method, url, query_string=None, payload_string=None):
    key = ''        # api_key
    secret = ''     # api_secret

    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}

if __name__ == "__main__":
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    common_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/futures/orders'
    body = {"contract": "BTC_USD", "size": 100, "price": "30", "tif": "gtc"}
    request_content = json.dumps(body)
    sign_headers = gen_sign('POST', prefix + url, "", request_content)
    sign_headers.update(common_headers)
    print('signature headers: %s' % sign_headers)
    res = requests.post(host + prefix + url, headers=sign_headers, data=request_content)
    print(res.status_code)
    print(res.content)

# coding: utf-8
host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

url = '/wallet/withdraw_status'
query_param = ''
# for `gen_sign` implementation, refer to section `Authentication` above
sign_headers = gen_sign('GET', prefix + url, query_param)
headers.update(sign_headers)
r = requests.request('GET', host + prefix + url, headers=headers)
print(r.json())

"""
# Your Binance API Key and Secret (keep these secure)
api_key = '78V3ctP4eXqkgZ844fYgnVU5Yjt4mbQ2pOUVlU9iPD97PWrKrKvOppgmG8qjDcXz'
api_secret = 'LzkAwnhNvFUjdBXUBbKC4G9tvx7p2K5LB1oU5o0qKEypjEXKTAnNiZq9U61j964T'  # Not required for public endpoints, but ensure you have it for private endpoints

# Binance API endpoint for asset configuration
url = 'https://api.binance.com/sapi/v1/capital/config/getall'

# Set up headers with API Key
headers = {
    'X-MBX-APIKEY': api_key
}

# Send a GET request to the endpoint with headers
response = requests.get(url, headers=headers)
data = response.json()

# Check for errors
if 'code' in data:
    print(f"Error: {data['msg']}")
else:
    # Specify the coin you're interested in
    coin = 'PEOPLE'

    # Find and print withdrawal and deposit details for the specified coin
    found = False
    for asset in data:
        if asset['asset'] == coin:
            found = True
            withdrawal_fee = asset.get('withdrawFee', 'Not available')
            deposit_fee = asset.get('depositFee', 'Not available')
            network_list = asset.get('networkList', [])
            
            print(f"Withdrawal fee for {coin}: {withdrawal_fee}")
            print(f"Deposit fee for {coin}: {deposit_fee}")
            print(f"Networks for {coin}:")
            for network in network_list:
                print(f"  - Network: {network['network']}, Withdrawal Fee: {network.get('withdrawFee', 'Not available')}, Deposit Fee: {network.get('depositFee', 'Not available')}")
            break

    if not found:
        print(f"{coin} not found on Binance.")
"""
