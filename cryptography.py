# Need to do: pip install PyCryptodome
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate a new RSA key pair
key = RSA.generate(2048)

# Save the private key to a file
with open('private.pem', 'wb') as f:
    f.write(key.export_key('PEM'))

# Save the public key to a file
with open('public.pem', 'wb') as f:
    f.write(key.publickey().export_key('PEM'))

# Load the private key from file
with open('private.pem', 'rb') as f:
    private_key = RSA.import_key(f.read())

# Load the public key from file
with open('public.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())


# Encrypt a message using the public key
cipher = PKCS1_OAEP.new(public_key)
message = b'Hello, world!'
encrypted = cipher.encrypt(message)

# Decrypt the message using the private key
cipher = PKCS1_OAEP.new(private_key)
decrypted = cipher.decrypt(encrypted)

print('\nOriginal message:', message)
print('\nEncrypted message:', encrypted)
print('\nDecrypted message:', decrypted)