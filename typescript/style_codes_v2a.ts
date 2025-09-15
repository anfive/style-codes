
class StyleJudgementV2 {
    bas: number;
    mov: number;
    din: number;
    com: number;
    sapd: number;
    gcc: number;
    dif: number;
    sog: number;
    pen: number;

    constructor(bas: number, mov: number, din: number, com: number, sapd: number, gcc: number, dif: number, sog: number, pen: number) {
        this.bas = bas;
        this.mov = mov;
        this.din = din;
        this.com = com;
        this.sapd = sapd;
        this.gcc = gcc;
        this.dif = dif;
        this.sog = sog;
        this.pen = pen;
    }

    toString(): string {
        return `BAS: ${this.bas.toFixed(1)}, MOV: ${this.mov.toFixed(1)}, DIN: ${this.din.toFixed(1)}, COM: ${this.com.toFixed(1)}, SAPD: ${this.sapd.toFixed(1)}, GCC: ${this.gcc.toFixed(1)}, DIF: ${this.dif.toFixed(1)}, SOG: ${this.sog}, PEN: ${this.pen}`;
    }

    equals(other: StyleJudgementV2): boolean {
        return this.bas === other.bas &&
            this.mov === other.mov &&
            this.din === other.din &&
            this.com === other.com &&
            this.sapd === other.sapd &&
            this.gcc === other.gcc &&
            this.dif === other.dif &&
            this.sog === other.sog &&
            this.pen === other.pen;
    }
}

const ALPHABET_23 = 'zyxwvutsrqpnmkjhgfedcba';
const PEN_CODE = '0123456789abcdefghjkm';
const DECODE_REGEX = /^(?<a>[a-hj-km-np-z])(?<b>[a-hj-km-np-z])?(?<half_points>[0-9]{1,2})(?:(?<c>[a-hj-km-np-z])?(?<d>[a-hj-km-np-z])?(?<e>[a-hj-km-np-z])?(?:(?<sog>[0-3])?(?<pen>[a-hj-km0-9])?)?)?$/;

function styleDecodeV2a(code: string): StyleJudgementV2 {
    if (!code) {
        throw new Error('Style code is empty');
    }
    code = code.toLowerCase();
    const match = DECODE_REGEX.exec(code);
    if (match === null) {
        throw new Error(`Invalid style code ${code}`);
    }

    const halfPoints = parseInt(match.groups!.half_points);

    const sog = match.groups!.sog === undefined ? 0 : parseInt(match.groups!.sog);
    const pen = match.groups!.pen === undefined ? 0 : PEN_CODE.indexOf(match.groups!.pen);

    const e = match.groups!.e ?? '';
    const d = match.groups!.d ?? '';
    const c = match.groups!.c ?? '';
    const b = match.groups!.b ?? '';
    const a = match.groups!.a;

    if (e === 'z' || (e === '' && (d === 'z' || (d === '' && (c === 'z' && sog === 0 && pen === 0) || (c === '' && b === 'z'))))) {
        // Leading 'z's (zeros) are not allowed, unless as separator for SOG and PEN
        throw new Error(`Invalid style code ${code}`);
    }

    // Decode the encoded values from the regex groups
    const aVal = decode23(a);
    const bVal = b === '' ? 0 : decode23(b);
    const cVal = c === '' ? 0 : decode23(c);
    const dVal = d === '' ? 0 : decode23(d);
    const eVal = e === '' ? 0 : decode23(e);

    // Reconstruct the value from the encoded components
    let value = aVal + bVal * 23 + cVal * 23 * 23 + dVal * 23 * 23 * 23 + eVal * 23 * 23 * 23 * 23;

    // Invert the formula step by step (highest order terms first)
    const difInt = Math.floor(value / (3 * 3 * 3 * 3 * 3 * 3 * 7 * 7));
    value = value % (3 * 3 * 3 * 3 * 3 * 3 * 7 * 7);

    const sapdInt = Math.floor(value / (3 * 3 * 3 * 3 * 3 * 3 * 7));
    value = value % (3 * 3 * 3 * 3 * 3 * 3 * 7);

    const comInt = Math.floor(value / (3 * 3 * 3 * 3 * 3 * 3));
    value = value % (3 * 3 * 3 * 3 * 3 * 3);

    const gccHighDigit = Math.floor(value / (3 * 3 * 3 * 3 * 3));
    value = value % (3 * 3 * 3 * 3 * 3);

    const dinHighDigit = Math.floor(value / (3 * 3 * 3 * 3));
    value = value % (3 * 3 * 3 * 3);

    const movHighDigit = Math.floor(value / (3 * 3 * 3));
    value = value % (3 * 3 * 3);

    const dinLowDigit = Math.floor(value / (3 * 3));
    value = value % (3 * 3);

    const gccLowDigit = Math.floor(value / 3);
    value = value % 3;

    const movLowDigit = value;

    // Reconstruct the original integer values
    const movInt = movLowDigit + movHighDigit * 3;
    const dinInt = dinLowDigit + dinHighDigit * 3;
    const gccInt = gccLowDigit + gccHighDigit * 3;

    // Calculate bas_int from the total half_points
    const basInt = halfPoints - movInt - dinInt - comInt - sapdInt - gccInt - difInt;
    if (basInt < 0 || basInt > 6) {
        throw new Error(`Invalid style code ${code}`);
    }

    // Convert to actual point values (divide by 2)
    const bas = basInt / 2;
    const mov = movInt / 2;
    const din = dinInt / 2;
    const com = comInt / 2;
    const sapd = sapdInt / 2;
    const gcc = gccInt / 2;
    const dif = difInt / 2;

    const sty = new StyleJudgementV2(
        bas,
        mov,
        din,
        com,
        sapd,
        gcc,
        dif,
        sog,
        pen
    );

    return sty;
}

function decode23(value: string): number {
    return ALPHABET_23.indexOf(value[0]);
}

function toHalfPoints(points: number): number {
    const value = points * 2;
    if (Math.floor(value) !== value) {
        throw new Error(`Invalid value in category (only multiples of 0.5 are allowed): ${points}`);
    }
    if (value < 0 || value > 6) {
        throw new Error(`Invalid value in category (must be within 0 and 3): ${points}`);
    }
    return Math.floor(value);
}

function styleEncodeV2a(style: StyleJudgementV2): string {
    const basInt = toHalfPoints(style.bas);
    const movInt = toHalfPoints(style.mov);
    const dinInt = toHalfPoints(style.din);
    const comInt = toHalfPoints(style.com);
    const sapdInt = toHalfPoints(style.sapd);
    const gccInt = toHalfPoints(style.gcc);
    const difInt = toHalfPoints(style.dif);

    const movLowDigit = movInt % 3;
    const movHighDigit = Math.floor(movInt / 3);
    const dinLowDigit = dinInt % 3;
    const dinHighDigit = Math.floor(dinInt / 3);
    const gccLowDigit = gccInt % 3;
    const gccHighDigit = Math.floor(gccInt / 3);
    let value =
        movLowDigit +
        gccLowDigit * 3 +
        dinLowDigit * 3 * 3 +
        movHighDigit * 3 * 3 * 3 +
        dinHighDigit * 3 * 3 * 3 * 3 +
        gccHighDigit * 3 * 3 * 3 * 3 * 3 +
        comInt * 3 * 3 * 3 * 3 * 3 * 3 +
        sapdInt * 3 * 3 * 3 * 3 * 3 * 3 * 7 +
        difInt * 3 * 3 * 3 * 3 * 3 * 3 * 7 * 7;

    const a_val = value % 23
    value = Math.floor(value / 23)
    const b_val = value % 23
    value = Math.floor(value / 23)
    const c_val = value % 23
    value = Math.floor(value / 23)
    const d_val = value % 23
    value = Math.floor(value / 23)
    const e_val = value % 23

    const e = e_val === 0 ? '' : ALPHABET_23[e_val]
    const d = d_val === 0 && e === '' ? '' : ALPHABET_23[d_val]
    const c = c_val === 0 && d === '' ? '' : ALPHABET_23[c_val]
    const b = b_val === 0 && c === '' ? '' : ALPHABET_23[b_val]
    const a = ALPHABET_23[a_val]

    const pen = style.pen === 0 ? '' : PEN_CODE[style.pen];
    const sog = style.sog === 0 && pen === '' ? '' : style.sog.toString();

    let cFinal = c;
    if (sog !== '' && cFinal === '') {
        cFinal = 'z';
    }

    const points = basInt + movInt + dinInt + comInt + sapdInt + gccInt + difInt;
    return a + b + points.toString() + cFinal + d + e + sog + pen;
}

function main(): void {
    console.log('Running style codes v2a test...');

    // Run test
    let count = 0;
    const dumpCodes = true;
    
    for (let pen of [0, 1, 10]) {
        for (let sog = 0; sog < 4; sog++) {
            console.log(`PEN: ${pen}, SOG: ${sog}`);
            const codes: { [key: string]: string } = {};
            for (let sapd = 0; sapd < 7; sapd++) {
                for (let dif = 0; dif < 7; dif++) {
                    for (let com = 0; com < 7; com++) {
                        for (let din = 0; din < 7; din++) {
                            for (let gcc = 0; gcc < 7; gcc++) {
                                for (let mov = 0; mov < 7; mov++) {
                                    for (let bas = 0; bas < 7; bas++) {
                                        const sty = new StyleJudgementV2(bas / 2, mov / 2, din / 2, com / 2, sapd / 2, gcc / 2, dif / 2, sog, pen);
                                        const encoded = styleEncodeV2a(sty);
                                        if (encoded in codes) {
                                            throw new Error(`Code collision: ${encoded} is already used`);
                                        }
                                        codes[encoded] = sty.toString();
                                        const decoded = styleDecodeV2a(encoded);
                                        if (!decoded.equals(sty)) {
                                            throw new Error(`Code ${encoded} decoded to ${decoded.toString()}, expected ${sty.toString()}`);
                                        }
                                        count++;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            if (dumpCodes) {
                const fs = require('fs');
                fs.mkdirSync('out', { recursive: true });
                fs.writeFileSync(`out/style_codes_v2a_ts_pen=${pen}_sog=${sog}.json`, JSON.stringify(codes, null, 4));
                console.log(`Codes dumped to style_codes_v2a_pen=${pen}_sog=${sog}.json`);
            }
        }
    }


    const expected = Math.pow(7, 7) * 3 * 4;
    if (count !== expected) {
        throw new Error(`Count is ${count}, expected ${expected}`);
    }

    console.log(`Test passed. ${count} codes checked.`);
}
// Export functions for module use
export { StyleJudgementV2, styleDecodeV2a, styleEncodeV2a };

// Run main if this is the entry point
if (require.main === module) {
    main();
}
