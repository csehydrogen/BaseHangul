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

입력을 5바이트 크기의 블록으로 나누어 한 블록을 3개의 음절로 변환합니다. 변환 과정은 다음과 같습니다.

```
입력 = A(0x65), B(0x66), C(0x67), D(0x68), E(0x69)
   -> (0x69, 0x68, 0x67, 0x66, 0x65)  (256진법)
   -> 297498001985                    (10진법)
   -> (0x094F, 0x1781, 0x24AD)        (11172진법)
   -> (0xB54F, 0xC381, 0xD0AD)        (0xAC00을 더해 한글 유니코드로 변환)
출력 = 킭(0xD0AD), 쎁(0xC381), 땏(0xB54F)
```

마지막 블록이 5바이트가 아닌 경우 다음과 같이 처리합니다.

* 4바이트 블록

  3개의 음절로 변환합니다. 10진법 기준으로 `0 ~ (256 ** 5 - 1)`은 5바이트 블록에 할당되어 있으므로, 변환 도중에 `256 ** 5`를 더해줍니다.

* 3바이트 블록

  2개의 음절로 변환합니다.

* 2바이트 블록

  2개의 음절로 변환합니다. 10진법 기준으로 `0 ~ (256 ** 3 - 1)`은 3바이트 블록에 할당되어 있으므로, 변환 도중에 `256 ** 3`를 더해줍니다.

* 1바이트 블록

  1개의 음절로 변환합니다.

## Q&A

* 왜 쓰나요?

  압축률이 높습니다. (진지)
  ```python
  >>> s = b'ABCDEFGHIJKLMNO' # len = 15
  >>> base64.b64encode(s)
  'QUJDREVGR0hJSktMTU5P'     # len = 20
  >>> BaseHangul.encode(s)
  '킭쎁땏숂랹뗼덗힕뚨'       # len = 9
  ```
