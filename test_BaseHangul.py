import unittest

from BaseHangul import encode, decode

class TestBaseHangul(unittest.TestCase):
    def test_encdec(self):
        # from rfc4648
        test_vectors = [b'', b'f', b'fo', b'foo', b'foob', b'fooba', b'foobar']
        for tv in test_vectors:
            self.assertEqual(tv, decode(encode(tv)))

if __name__ == '__main__':
    unittest.main()
