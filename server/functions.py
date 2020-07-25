import hashlib
import random,string
def md5value(s):
    md5 = hashlib.md5()
    md5.update(s.encode())
    return md5.hexdigest()
def genRandomString(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))