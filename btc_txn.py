from bit import wif_to_key

key = wif_to_key(os.getenv('btctest_key'))

addresses = [
    "mfm9NFhkwvUhok3K644cibc9YQazJ5hpyT"
    ]

outputs = []

for address in addresses:
    outputs.append((address,.00000000001,"btc"))

print(key.send(outputs))