import re
from math import floor

class StyleJudgementV1:

    def __init__(self, bas, mov, din, com, sapd, gcc, dif, sog, pen):
        self.bas = bas
        self.mov = mov
        self.din = din
        self.com = com
        self.sapd = sapd
        self.gcc = gcc
        self.dif = dif
        self.sog = sog
        self.pen = pen

    def __str__(self):
        return f'BAS: {self.bas:.1f}, MOV: {self.mov:.1f}, DIN: {self.din:.1f}, COM: {self.com:.1f}, SAPD: {self.sapd:.1f}, GCC: {self.gcc:.1f}, DIF: {self.dif:.1f}, SOG: {self.sog}, PEN: {self.pen}'

    def __eq__(self, other):
        return self.bas == other.bas and \
            self.mov == other.mov and \
            self.din == other.din and \
            self.com == other.com and \
            self.sapd == other.sapd and \
            self.gcc == other.gcc and \
            self.dif == other.dif and \
            self.sog == other.sog and \
            self.pen == other.pen

def style_decode_v1(code) -> StyleJudgementV1:
        if not code:
            raise Exception('Style code is empty')
        code = code.lower()
        match = DECODE_REGEX.fullmatch(code)
        if match is None:
            raise Exception(f'Invalid style code {code}')

        points = int(match.group('points'))

        if(match.group('third') is None):
            if(match.group('second') is None or match.group('second') == 'z'):
                # 1-letter code
                val = decode26(match.group('first'))
                mov = floor(val / (3 * 3))
                remainder = val % (3 * 3)
                din = floor(remainder / 3)
                gcc = remainder % 3
                com = 0
                sapd = 0
                dif = 0
            else:
                # 2-letters code
                val = decode26(match.group('first')) * 23 + \
                    decode23(match.group('second'))

                mov = floor(val / (4 * 4 * 2 * 2 * 2))
                remainder = val % (4 * 4 * 2 * 2 * 2)
                din = floor(remainder / (4 * 2 * 2 * 2))
                remainder = remainder % (4 * 2 * 2 * 2)
                gcc = floor(remainder / (2 * 2 * 2))
                remainder = remainder % (2 * 2 * 2)
                com = floor(remainder / (2 * 2))
                remainder = remainder % (2 * 2)
                sapd = floor(remainder / 2)
                dif = remainder % 2

        else:
            # 3-letters code
            val = decode26(match.group('first')) * 26 * 23 + \
                decode23(match.group('second')) * 26 + \
                decode26(match.group('third'))

            mov = floor(val / (4 * 4 * 4 * 4 * 4))
            remainder = val % (4 * 4 * 4 * 4 * 4)
            din = floor(remainder / (4 * 4 * 4 * 4))
            remainder = remainder % (4 * 4 * 4 * 4)
            gcc = floor(remainder / (4 * 4 * 4))
            remainder = remainder % (4 * 4 * 4)
            com = floor(remainder / (4 * 4))
            remainder = remainder % (4 * 4)
            sapd = floor(remainder / 4)
            dif = remainder % 4

        totalOtherScores = mov + din + com + sapd + gcc + dif
        bas = points - totalOtherScores
        if bas < 0 or bas > 3:
            raise Exception("Invalid style code:" + code)

        sog = 0 if match.group('sog') is None else int(match.group('sog'))
        pen = 0 if match.group('pen') is None else decodePenalties(
            match.group('pen'))

        # Use integer computation to avoid rounding errors...
        score = 55 + 2 * points + 1 * sog - 5 * pen
        score = score / 10

        sty = StyleJudgementV1(
            bas=bas,
            mov=mov,
            din=din,
            com=com,
            sapd=sapd,
            gcc=gcc,
            dif=dif,
            sog=sog,
            pen=pen,
        )

        return sty
        
_ALPHABET_26 = 'abcdefghijklmnopqrstuvwxyz'
def decode26(value):
    return _ALPHABET_26.find(value)

def encode26(value):
    return _ALPHABET_26[value]

_ALPHABET_23 = 'abcdefghjklmnpqrstuvwxy'
def decode23(value):
    return _ALPHABET_23.find(value)

def encode23(value):
    return _ALPHABET_23[value]

_PEN_CODE = '0123456789abcdefghjkl'
def decodePenalties(value):
    return _PEN_CODE.find(str(value))

def encodePenalties(value):
    return _PEN_CODE[value]


DECODE_REGEX = re.compile(
    '^(?P<first>[a-z])(?P<points>[0-9]{1,2})(?:(?P<second>[a-hj-np-z])(?:(?P<third>[a-z])?(?:(?P<sog>[0-3])(?P<pen>[0-9])?)?)?)?$')


def style_encode_v1(style : StyleJudgementV1) -> str:
    a = ''
    b = ''
    c = ''
    if (style.com == 0 and style.sapd == 0 and style.dif == 0
        and (style.mov + style.din + style.gcc < 6)
        and (style.mov < 3 and style.din < 3 and style.gcc < 3)):
        # One-letter format
        a = encode26((style.mov * 3 + style.din) * 3 + style.gcc)
    else:
        if style.sapd < 2 and style.com < 2 and style.dif < 2:
            # Two-letters format
            value = (((((style.mov * 4 + style.din) * 4 + style.gcc) * 2 + style.com) * 2 + style.sapd) * 2 + style.dif)
            a = encode26(value // 23)
            b = encode23(value % 23)
        else:
            # Three-letters format
            value = (((((style.mov * 4 + style.din) * 4 + style.gcc) * 4 + style.com) * 4 + style.sapd) * 4 + style.dif)
            a = encode26(value // (23 * 26))
            remainder = value % (23 * 26)
            b = encode23(remainder // 26)
            c = encode26(remainder % 26)
    
    pen = '' if style.pen == 0 else encodePenalties(style.pen)
    sog = '' if style.sog == 0 and pen == '' else str(style.sog)
    if sog != '' and b == '':
        b = 'z'

    points = style.bas + style.mov + style.din + style.com + style.sapd + style.gcc + style.dif
    points = str(points)
    return a + points + b + c + pen + sog

if __name__ == '__main__':
    # Run test
    codes = {}
    count = 0
    for sapd in range(0, 4):
        for dif in range(0, 4):
            for com in range(0, 4):
                for din in range(0, 4):
                    for gcc in range(0, 4):
                        for mov in range(0, 4):
                            for bas in range(0, 4):
                                sty = StyleJudgementV1(bas, mov, din, com, sapd, gcc, dif, 0, 0)
                                encoded = style_encode_v1(sty)
                                if encoded in codes:
                                    raise Exception(f'Code collision: {encoded} is already used')
                                codes[encoded] = str(sty)
                                decoded = style_decode_v1(encoded)
                                if decoded != sty:
                                    raise Exception(f'Code {encoded} decoded to {decoded}, expected {sty}')
                                count += 1

    expected = 4 ** 7
    if count != expected:
        raise Exception(f'Count is {count}, expected {expected}')

    print(f'Test passed. {count} codes checked.')
