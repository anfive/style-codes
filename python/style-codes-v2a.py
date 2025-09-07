import re
from math import floor

class StyleJudgementV2:

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

def style_decode_v2a(code) -> StyleJudgementV2:
        if not code:
            raise Exception('Style code is empty')
        code = code.lower()
        match = DECODE_REGEX.fullmatch(code)
        if match is None:
            raise Exception(f'Invalid style code {code}')

        half_points = int(match.group('half_points'))

        sog = 0 if match.group('sog') is None else int(match.group('sog'))
        pen = 0 if match.group('pen') is None else _decode_penalties(
            match.group('pen'))

        # Decode the encoded values from the regex groups
        a_val = _decode23(match.group('a'))
        b_val = 0 if match.group('b') is None else _decode23(match.group('b'))
        c_val = 0 if match.group('c') is None else _decode23(match.group('c'))
        d_val = 0 if match.group('d') is None else _decode23(match.group('d'))
        e_val = 0 if match.group('e') is None else _decode23(match.group('e'))

        # Reconstruct the value from the encoded components
        value = a_val + b_val * 23 + c_val * 23 * 23 + d_val * 23 * 23 * 23 + e_val * 23 * 23 * 23 * 23

        # Invert the formula step by step (highest order terms first)
        dif_int = value // (3 * 3 * 3 * 3 * 3 * 3 * 7 * 7)
        value = value % (3 * 3 * 3 * 3 * 3 * 3 * 7 * 7)
        
        sapd_int = value // (3 * 3 * 3 * 3 * 3 * 3 * 7)
        value = value % (3 * 3 * 3 * 3 * 3 * 3 * 7)
        
        com_int = value // (3 * 3 * 3 * 3 * 3 * 3)
        value = value % (3 * 3 * 3 * 3 * 3 * 3)
        
        gcc_high_digit = value // (3 * 3 * 3 * 3 * 3)
        value = value % (3 * 3 * 3 * 3 * 3)
        
        din_high_digit = value // (3 * 3 * 3 * 3)
        value = value % (3 * 3 * 3 * 3)
        
        mov_high_digit = value // (3 * 3 * 3)
        value = value % (3 * 3 * 3)
        
        din_low_digit = value // (3 * 3)
        value = value % (3 * 3)
        
        gcc_low_digit = value // 3
        value = value % 3
        
        mov_low_digit = value

        # Reconstruct the original integer values
        mov_int = mov_low_digit + mov_high_digit * 3
        din_int = din_low_digit + din_high_digit * 3
        gcc_int = gcc_low_digit + gcc_high_digit * 3

        # Calculate bas_int from the total half_points
        bas_int = half_points - mov_int - din_int - com_int - sapd_int - gcc_int - dif_int

        # Convert to actual point values (divide by 2)
        bas = bas_int / 2
        mov = mov_int / 2
        din = din_int / 2
        com = com_int / 2
        sapd = sapd_int / 2
        gcc = gcc_int / 2
        dif = dif_int / 2

        sty = StyleJudgementV2(
            bas=bas,
            mov=mov,
            din=din,
            com=com,
            sapd=sapd,
            gcc=gcc,
            dif=dif,
            sog=sog,
            pen=pen
        )

        return sty
        
_ALPHABET_23 = 'zyxwvutsrqpnmkjhgfedcba'
def _decode23(value):
    return _ALPHABET_23.find(value)

def _encode23(value):
    return _ALPHABET_23[value]

_PEN_CODE = '0123456789abcdefghjkl'
def _decode_penalties(value):
    return _PEN_CODE.find(str(value))

def _encode_penalties(value):
    return _PEN_CODE[value]


DECODE_REGEX = re.compile(
    '^(?P<a>[a-hj-km-np-z])(?P<b>[a-hj-km-np-z])?(?P<half_points>[0-9]{1,2})(?:(?P<c>[a-hj-km-np-z])?(?P<d>[a-hj-km-np-z])?(?P<e>[a-hj-km-np-z])?(?:(?P<sog>[0-3])?(?P<pen>[0-9])?)?)?$')


def _to_half_points(points : int) -> int:
    value = int(points * 2)
    if floor(value) != value:
        raise Exception(f'Invalid value in category (only multiples of 0.5 are allowed): {points}')
    if value < 0 or value > 6:
        raise Exception(f'Invalid value in category (must be within 0 and 3): {points}')
    return value

def style_encode_v2a(style : StyleJudgementV2) -> str:
    bas_int = _to_half_points(style.bas)
    mov_int = _to_half_points(style.mov)
    din_int = _to_half_points(style.din)
    com_int = _to_half_points(style.com)
    sapd_int = _to_half_points(style.sapd)
    gcc_int = _to_half_points(style.gcc)
    dif_int = _to_half_points(style.dif)

    mov_low_digit = mov_int % 3
    mov_high_digit = mov_int // 3
    din_low_digit = din_int % 3
    din_high_digit = din_int // 3
    gcc_low_digit = gcc_int % 3
    gcc_high_digit = gcc_int // 3

    value = mov_low_digit + \
        gcc_low_digit * 3 + \
        din_low_digit * 3 * 3 + \
        mov_high_digit * 3 * 3 * 3 + \
        din_high_digit * 3 * 3 * 3 * 3 + \
        gcc_high_digit * 3 * 3 * 3 * 3 * 3 + \
        com_int * 3 * 3 * 3 * 3 * 3 * 3 + \
        sapd_int * 3 * 3 * 3 * 3 * 3 * 3 * 7 + \
        dif_int * 3 * 3 * 3 * 3 * 3 * 3 * 7 * 7
    a_val = value % 23
    value = value // 23
    b_val = value % 23
    value = value // 23
    c_val = value % 23
    value = value // 23
    d_val = value % 23
    value = value // 23
    e_val = value % 23

    e = _encode23(e_val) if e_val != 0 else ''
    d = _encode23(d_val) if d_val != 0 or e != '' else ''
    c = _encode23(c_val) if c_val != 0 or d != '' else ''
    b = _encode23(b_val) if b_val != 0 or c != '' else ''
    a = _encode23(a_val)

    pen = '' if style.pen == 0 else _encode_penalties(style.pen)
    sog = '' if style.sog == 0 and pen == '' else str(style.sog)
    if sog != '' and c == '':
        c = 'a'

    half_points = bas_int + mov_int + din_int + com_int + sapd_int + gcc_int + dif_int
    points = str(half_points)
    return a + b + points + c + d + e + pen + sog

if __name__ == '__main__':
    # Run test
    codes = {}
    count = 0
    for sapd in range(0, 7):
        for dif in range(0, 7):
            for com in range(0, 7):
                for din in range(0, 7):
                    for gcc in range(0, 7):
                        for mov in range(0, 7):
                            for bas in range(0, 7):
                                sty = StyleJudgementV2(bas / 2, mov / 2, din / 2, com / 2, sapd / 2, gcc / 2, dif / 2, 0, 0)
                                encoded = style_encode_v2a(sty)
                                if encoded in codes:
                                    raise Exception(f'Code collision: {encoded} is already used')
                                codes[encoded] = str(sty)
                                decoded = style_decode_v2a(encoded)
                                if decoded != sty:
                                    raise Exception(f'Code {encoded} decoded to {decoded}, expected {sty}')
                                count += 1

    expected = 7 ** 7
    if count != expected:
        raise Exception(f'Count is {count}, expected {expected}')

    print(f'Test passed. {count} codes checked.')

    dump_codes = True
    if dump_codes:
        import json
        with open('style_codes_v2a.json', 'w') as f:
            json.dump(codes, f, indent=2)
        
