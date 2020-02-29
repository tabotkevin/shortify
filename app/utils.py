# Base 62 characters set
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def b62_encode(id, characters=BASE62):

    base = len(characters)
    ret = []
    # convert base10 id into base62 id
    while id > 0:
        val = id % base
        ret.append(characters[val])
        id = id // base
    # since ret has reversed order of base62 id, reverse ret before return it
    return "".join(ret[::-1])

def b62_decode(short_url, characters=BASE62):

    base = len(characters)
    url_len = len(short_url)
    num = 0
    idx = 0
    # convert base62 id into base10 id
    for char in short_url:
        power = (url_len - (idx + 1))
        num += characters.index(char) * (base ** power)
        idx += 1

    return num
