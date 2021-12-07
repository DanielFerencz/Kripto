from packages.generator.merkle_hellman_knapsack import create_public_key, generate_private_key, encrypt_mh, decrypt_mh
from packages.generator.utils import is_superincreasing

asd = generate_private_key()

dsa = create_public_key(asd)

print(asd, dsa)

crypted = encrypt_mh("szia te", dsa)

print(crypted)

decrypted = decrypt_mh(crypted, asd)

print(decrypted)
