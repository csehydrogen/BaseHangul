# BaseHangul

유니코드에 포함된 한글 음절 11172자를 이용한 인코딩 및 디코딩 방식입니다.

## 설치

```bash
$ git clone https://github.com/csehydrogen/BaseHangul.git
$ pip install ~/BaseHangul
```

## 사용

```python
>>> import BaseHangul
>>> binary = b'The quick brown fox jumps over the lazy dog'
>>> type(binary)
<class 'bytes'>
>>> encoded = BaseHangul.encode(binary)
>>> encoded
'샼켖무쑡얱끛귚럎뫙뙈뫲끝헎벿뮄믬쇅뭠쾀칀끚뱜섐끝촬깞'
>>> type(encoded)
<class 'str'>
>>> decoded = BaseHangul.decode(encoded)
>>> decoded
b'The quick brown fox jumps over the lazy dog'
>>> type(decoded)
<class 'bytes'>
```

## Unittest

```bash
$ python -m unittest -v test_BaseHangul
test_encdec (test_BaseHangul.TestBaseHangul) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

## Scheme

TODO
