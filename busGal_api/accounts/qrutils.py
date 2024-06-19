import base64
import datetime
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import logging

# All this functionality was extracted after decompilation of the original app. The debug messages are also trying to emulate those in the original app, for easy diffing between the two


map_public_key_XN = [None,  # Must be 1-indexed
                     "MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgF7Qu36bTZzyGnLZcHsvNQgPt/NDvNkdFhEmKi4FqddsT1p9tCKjJRTrFu3ZTmR+w7brnOiTBxY9E3NuDq0E3SKREhkVKWHwRQs0qMQDtOo3+m3iC+QLOdfKdJd+SGTUqBayfouWFpYzetArKgBxwK2STUY6/Yc0p5cFQiX4Gdc3AgMBAAE=",
                     "MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgHKM6MiGgLynPwSvazD3YYt1bRDodLz4xr+UzowuUtsArcQBoAY/wA8ep4FylD5iFMFGcBTCVo8HHHwipO20y9PF1Sktmx/C2wb0NkSe2i1ZYnZjetvm08wGOUCg0wm1l3TzeUpw77zWpO/7E+LIigmtVsY5/Yc0p5cFQiX4Gdc3AgMBAAE=",
                     "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDCbL+YV+kcYn7iCehptq26rPD0MeTSRw33yjr+5XIhOiqCVkgRP494HF64r+b+7s24+kwxt0guD8NZ/FnUmR9QBwXf3wC/dEzOd0vgZ9SBo2MvPlIY+HjnSW3bMVufYNFGwkjATnKEmGJ1G41GQaPqOGN4VDi0QnXByF0cNICzmQIDAQAB",
                     "MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgGg8vZIpgsJPUemRbE8hrtfbX909AAvJQ/muvoYm3gFJSxcVjBcUaiY6luXk+g/h0ojt37w3G5oy9nF4ttFmNov6B/pSgQd1TMrgu4q8XDNU28dQrxIl20skOH35f74BJVtCw26QUh0Z41hI7F5lGrHA/6baEtquLCyvEGyo2PT1AgMBAAE=",
                     "MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgEe1dfJe0P6oGR3InGbPdA8kphtc5MdamjukNpKw9OX+OqJOlBwXGI0pIocRx2Bnruzr81rBDMi3adf+jsRkdw5PDusY4Nh4HJ6OHw2iu4O9zYgH0GiJtxF4vO7v6csSYZ8e4bb4nY/dn2Lq4vbs8oH7wtx5FSGipzlEAG/yOi6ZAgMBAAE=",
                     "MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgGWc/j2aXj2R7CuJvM85KmLrYoQOoMaWkd2hno6PF2KmbdzSEqZo1xV+PBt8/h4lX6wCBf6IH78GGHbY2EZjAz93qNGQa0xYlndTMWVWGv/X5fnYrbbAiNSquSgecTJ0C53QeOpYOWmI2RSXZZ2rcwQKW3Jz03VCJGwJtxkqXBStAgMBAAE=",
                     "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbJEbavnp51cn9qhCu7gExdx+4HI5C5e7+551lXXRRE6Djw195wM1zh0h3PB7BgRU1ZFSF1LByqdosnBdqwH8F5dymvQabQ6gm9Iitvl5V7f0OgCc1uKUPgkn25vMiKINRjx36GkbO5PCs9pv1KWrNgv2eMtysa/ynuETUJrdtqQIDAQAB",
                     "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCHaYF2g+9XfmjCU0JSldtT6I63aS2aeaTo4aydwjBlOpknqzeMMH+mO6l60aA4/qNKS243bO2bgJCG54G/ZoaN9tbkSVZj3Cm7n8ZBIdbn6Sjn7tnBopcng/X0q2AhV6ysFoqKAM9yHK3B6fvgXLLEE9ZruvS1lNVQpZw6xtJjpwIDAQAB",
                     "MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgHx2NaovbRw1PwO+p5zhvg8e6acn/anamdVLeBBknJZRB7IWn//AUjBx5fhkZucpnR0ANr1059DLgfutXPGR6DtttFHIC2W/SBL7CsfO6iKUY+QAGUN+vEY7Ndq927vB7zEhIow0q2E5FjW7bp0xzp9WmGouFp6+SLCi0fvbg7HBAgMBAAE=",
                     "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDNThiD8iQj0+BoRMA+KKYL8v+IWYFs4YzIWpM435pbl48YxLvjc0jHONBjU0fPE33azrTOH0aaKmwU/IJxBmQF2Bcmy7WIHe84C02Ir4H3FM11Jr+NaTuhwyCXo2HYrT3Rls4lK1wrq2QX7+CZOhdVkUajs0EETtraV+sM0gcGxQIDAQAB"]

logger = logging.getLogger(__name__)


def encode_ECB_as_hex_string(key, data):
    key = bytes.fromhex(key)
    data = bytes.fromhex(data)
    cipher = DES.new(key, DES.MODE_ECB)
    padded_data = pad(data, 8)
    encrypted_data = cipher.encrypt(padded_data)

    return encrypted_data.hex()


def b64_to_hex(s):
    return base64.b64decode(s).hex()


def create_qr(id_signature_keys, static_data, custom_datetime=None):
    logger.debug(msg=f"DOG: {id_signature_keys}")
    signature = map_public_key_XN[id_signature_keys]
    logger.debug(msg=f"DOG: {signature}")
    signature_hex = b64_to_hex(signature)[:16]

    logger.debug(msg=f"DOG-Static base 64: {static_data}")
    static_data_hex = b64_to_hex(static_data)
    logger.debug(msg=f"DOG-Static Hexa: {static_data_hex}")

    calendar = custom_datetime or datetime.datetime.utcnow()
    logger.debug(msg=f"DOG_D: {calendar.strftime('%y-%m-%d %H:%M:%S')}")
    year_bin = bin(calendar.year - 2000)[2:]
    month_bin = bin(calendar.month)[2:]
    day_bin = bin(calendar.day)[2:]
    hour_bin = bin(calendar.hour)[2:]
    minute_bin = bin(calendar.minute)[2:]
    secound_bin = bin(calendar.second)[2:]
    date_hex = hex(int(year_bin.zfill(6) + month_bin.zfill(4) + day_bin.zfill(5) +
                   hour_bin.zfill(5) + minute_bin.zfill(6) + secound_bin.zfill(6), 2))[2:]

    logger.debug(msg=f"DOG-Dynamic Hexa: {date_hex}")
    logger.debug(msg=f"DOG-Key Hexa: {signature_hex}")

    date_encoded_hex = encode_ECB_as_hex_string(
        signature_hex, date_hex + "00000000")[:16]
    logger.debug(msg=f"DOG-Result encrypt: {date_encoded_hex}")

    final_hex = static_data_hex + date_encoded_hex
    logger.debug(msg=f"DOG-Total Hexa: {final_hex}")

    final_b64 = base64.b64encode(bytes.fromhex(final_hex)).decode('utf-8')
    logger.debug(msg=f"DOG-Total Base64: {final_b64}") # In the app this has a bug and outputs "DOG-Total Hexa" again

    return final_b64
