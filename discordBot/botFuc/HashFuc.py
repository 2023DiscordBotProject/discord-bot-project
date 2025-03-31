from Crypto.Hash import SHA512


def hashFuc(text):
    hashCode = SHA512.new()
    hashCode.update(text.encode('utf-8'))
    cipherText = hashCode.hexdigest()

    return cipherText
