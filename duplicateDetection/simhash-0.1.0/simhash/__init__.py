#Created by Liang Sun in 2013
import re
import hashlib

class Simhash(object):
    def __init__(self, value):
        self.f = 64
        self.reg = ur'\w+'
        self.value = None

        if isinstance(value, list):
            self.build_by_features(value)
        elif isinstance(value, long):
            self.value = value
        elif isinstance(value, Simhash):
            self.value = value.hash
        else:
            self.build_by_text(value)

    def _slide(self, content, width=2):
        return [content[i:i+width] for i in xrange(len(content)-width+1)]

    def _tokenize(self, content):
        ans = []
        content = ''.join(re.findall(self.reg, content))
        ans = self._slide(content)
        return ans

    def build_by_text(self, content):
        features = self._tokenize(content)
        return self.build_by_features(features)

    def build_by_features(self, features):
        #print features
        
        hashs = [int(hashlib.md5(w).hexdigest(), 16) for w in features]
        
        v = [0]*self.f
        for h in hashs:
            for i in xrange(self.f):
                mask = 1 << i
                v[i] += 1 if h & mask else -1
        ans = 0
        for i in xrange(self.f):
            if v[i] >= 0:
                ans |= 1 << i
        self.value = ans

    def distance(self, another):
        x = (self.value ^ another.value) & ((1 << self.f) - 1)
        ans = 0
        while x:
            ans += 1
            x &= x-1
        return ans
