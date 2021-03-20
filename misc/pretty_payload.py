import sys

payload = sys.argv[1]

print("payload = \"", end='')
for i in range(0, len(payload)):
    print(payload[i], end='')
    if i % 75 == 0 and i != 0:
        print("\"\npayload = payload + \"", end='')

print("\"")
