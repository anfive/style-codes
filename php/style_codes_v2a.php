<?php

class StyleJudgementV2 {
    public $bas;
    public $mov;
    public $din;
    public $com;
    public $sapd;
    public $gcc;
    public $dif;
    public $sog;
    public $pen;

    public function __construct($bas, $mov, $din, $com, $sapd, $gcc, $dif, $sog, $pen) {
        $this->bas = $bas;
        $this->mov = $mov;
        $this->din = $din;
        $this->com = $com;
        $this->sapd = $sapd;
        $this->gcc = $gcc;
        $this->dif = $dif;
        $this->sog = $sog;
        $this->pen = $pen;
    }

    public function __toString() {
        return sprintf('BAS: %.1f, MOV: %.1f, DIN: %.1f, COM: %.1f, SAPD: %.1f, GCC: %.1f, DIF: %.1f, SOG: %d, PEN: %d',
            $this->bas, $this->mov, $this->din, $this->com, $this->sapd, $this->gcc, $this->dif, $this->sog, $this->pen);
    }

    public function equals($other) {
        return $this->bas === $other->bas &&
            $this->mov === $other->mov &&
            $this->din === $other->din &&
            $this->com === $other->com &&
            $this->sapd === $other->sapd &&
            $this->gcc === $other->gcc &&
            $this->dif === $other->dif &&
            $this->sog === $other->sog &&
            $this->pen === $other->pen;
    }
}

const ALPHABET_23 = 'zyxwvutsrqpnmkjhgfedcba';
const PEN_CODE = '0123456789abcdefghjkl';
const DECODE_REGEX = '/^(?P<a>[a-hj-km-np-z])(?P<b>[a-hj-km-np-z])?(?P<half_points>[0-9]{1,2})(?:(?P<c>[a-hj-km-np-z])?(?P<d>[a-hj-km-np-z])?(?P<e>[a-hj-km-np-z])?(?:(?P<sog>[0-3])?(?P<pen>[a-hj-km0-9])?)?)?$/';

function styleDecodeV2a($code) {
    if (!$code) {
        throw new Exception('Style code is empty');
    }
    $code = strtolower($code);
    
    if (!preg_match(DECODE_REGEX, $code, $matches)) {
        throw new Exception("Invalid style code $code");
    }

    $halfPointStr = $matches['half_points'];
    if (strlen($halfPointStr) == 2 && $halfPointStr[0] == '0') {
        // Leading zero is not allowed
        throw new Exception("Invalid style code $code");
    }
    $halfPoints = intval($matches['half_points']);

    $sog = isset($matches['sog']) ? intval($matches['sog']) : 0;
    $pen = isset($matches['pen']) ? strpos(PEN_CODE, $matches['pen']) : 0;

    $e = $matches['e'] ?? '';
    $d = $matches['d'] ?? '';
    $c = $matches['c'] ?? '';
    $b = $matches['b'] ?? '';
    $a = $matches['a'];

    if ($e === 'z' || ($e === '' && ($d === 'z' || ($d === '' && (($c === 'z' && $sog === 0 && $pen === 0) || ($c === '' && $b === 'z')))))) {
        // Leading 'z's (zeros) are not allowed, unless as separator for SOG and PEN
        throw new Exception("Invalid style code $code");
    }

    // Decode the encoded values from the regex groups
    $aVal = strpos(ALPHABET_23, $a);
    $bVal = $b ? strpos(ALPHABET_23, $b) : 0;
    $cVal = $c ? strpos(ALPHABET_23, $c) : 0;
    $dVal = $d ? strpos(ALPHABET_23, $d) : 0;
    $eVal = $e ? strpos(ALPHABET_23, $e) : 0;

    // Reconstruct the value from the encoded components
    $value = $aVal + $bVal * 23 + $cVal * 23 * 23 + $dVal * 23 * 23 * 23 + $eVal * 23 * 23 * 23 * 23;

    // Invert the formula step by step (highest order terms first)
    $difInt = intval($value / (3 * 3 * 3 * 3 * 3 * 3 * 7 * 7));
    $value = $value % (3 * 3 * 3 * 3 * 3 * 3 * 7 * 7);
    
    $sapdInt = intval($value / (3 * 3 * 3 * 3 * 3 * 3 * 7));
    $value = $value % (3 * 3 * 3 * 3 * 3 * 3 * 7);
    
    $comInt = intval($value / (3 * 3 * 3 * 3 * 3 * 3));
    $value = $value % (3 * 3 * 3 * 3 * 3 * 3);
    
    $gccHighDigit = intval($value / (3 * 3 * 3 * 3 * 3));
    $value = $value % (3 * 3 * 3 * 3 * 3);
    
    $dinHighDigit = intval($value / (3 * 3 * 3 * 3));
    $value = $value % (3 * 3 * 3 * 3);
    
    $movHighDigit = intval($value / (3 * 3 * 3));
    $value = $value % (3 * 3 * 3);
    
    $dinLowDigit = intval($value / (3 * 3));
    $value = $value % (3 * 3);
    
    $gccLowDigit = intval($value / 3);
    $value = $value % 3;
    
    $movLowDigit = $value;

    // Reconstruct the original integer values
    $movInt = $movLowDigit + $movHighDigit * 3;
    $dinInt = $dinLowDigit + $dinHighDigit * 3;
    $gccInt = $gccLowDigit + $gccHighDigit * 3;

    // Calculate bas_int from the total half_points
    $basInt = $halfPoints - $movInt - $dinInt - $comInt - $sapdInt - $gccInt - $difInt;
    if ($basInt < 0 || $basInt > 6) {
        throw new Exception("Invalid style code $code");
    }

    // Convert to actual point values (divide by 2)
    $bas = $basInt / 2;
    $mov = $movInt / 2;
    $din = $dinInt / 2;
    $com = $comInt / 2;
    $sapd = $sapdInt / 2;
    $gcc = $gccInt / 2;
    $dif = $difInt / 2;

    $sty = new StyleJudgementV2(
        $bas,
        $mov,
        $din,
        $com,
        $sapd,
        $gcc,
        $dif,
        $sog,
        $pen
    );

    return $sty;
}

function toHalfPoints(float $points): int {
    $value = $points * 2;
    if (floor($value) != $value) {
        throw new Exception("Invalid value in category (only multiples of 0.5 are allowed): $points");
    }
    if ($value < 0 || $value > 6) {
        throw new Exception("Invalid value in category (must be within 0 and 3): $points");
    }
    return intdiv($value, 1);
}

function styleEncodeV2a($style) {
    $basInt = toHalfPoints($style->bas);
    $movInt = toHalfPoints($style->mov);
    $dinInt = toHalfPoints($style->din);
    $comInt = toHalfPoints($style->com);
    $sapdInt = toHalfPoints($style->sapd);
    $gccInt = toHalfPoints($style->gcc);
    $difInt = toHalfPoints($style->dif);
    
    if ($style->sog < 0 || $style->sog > 3) {
        throw new Exception("Invalid value in SOG (must be within 0 and 3): {$style->sog}");
    }
    if ($style->pen < 0 || $style->pen > 20) {
        throw new Exception("Invalid value in PEN (must be within 0 and 20): {$style->pen}");
    }

    $movLowDigit = $movInt % 3;
    $movHighDigit = intval($movInt / 3);
    $dinLowDigit = $dinInt % 3;
    $dinHighDigit = intval($dinInt / 3);
    $gccLowDigit = $gccInt % 3;
    $gccHighDigit = intval($gccInt / 3);

    $value = $movLowDigit +
        $gccLowDigit * 3 +
        $dinLowDigit * 3 * 3 +
        $movHighDigit * 3 * 3 * 3 +
        $dinHighDigit * 3 * 3 * 3 * 3 +
        $gccHighDigit * 3 * 3 * 3 * 3 * 3 +
        $comInt * 3 * 3 * 3 * 3 * 3 * 3 +
        $sapdInt * 3 * 3 * 3 * 3 * 3 * 3 * 7 +
        $difInt * 3 * 3 * 3 * 3 * 3 * 3 * 7 * 7;

    $aVal = $value % 23;
    $value = intval($value / 23);
    $bVal = $value % 23;
    $value = intval($value / 23);
    $cVal = $value % 23;
    $value = intval($value / 23);
    $dVal = $value % 23;
    $value = intval($value / 23);
    $eVal = $value % 23;

    $e = $eVal !== 0 ? ALPHABET_23[$eVal] : '';
    $d = $dVal !== 0 || $e !== '' ? ALPHABET_23[$dVal] : '';
    $c = $cVal !== 0 || $d !== '' ? ALPHABET_23[$cVal] : '';
    $b = $bVal !== 0 || $c !== '' ? ALPHABET_23[$bVal] : '';
    $a = ALPHABET_23[$aVal];

    $pen = $style->pen === 0 ? '' : PEN_CODE[$style->pen];
    $sog = $style->sog === 0 && $pen === '' ? '' : strval($style->sog);
    if ($sog !== '' && $c === '') {
        $c = 'z';
    }

    $halfPoints = $basInt + $movInt + $dinInt + $comInt + $sapdInt + $gccInt + $difInt;
    $points = strval($halfPoints);
    return $a . $b . $points . $c . $d . $e . $sog . $pen;
}

// Main execution function
function main() {
    echo "Running style codes v2a test...\n";
    
    // Run test
    $count = 0;
    $dumpCodes = true;
    
    foreach ([0, 1, 10] as $pen) {
        for ($sog = 0; $sog < 4; $sog++) {
            echo "PEN: $pen, SOG: $sog\n";
            $codes = array();
            for ($sapd = 0; $sapd < 7; $sapd++) {
                for ($dif = 0; $dif < 7; $dif++) {
                    for ($com = 0; $com < 7; $com++) {
                        for ($din = 0; $din < 7; $din++) {
                            for ($gcc = 0; $gcc < 7; $gcc++) {
                                for ($mov = 0; $mov < 7; $mov++) {
                                    for ($bas = 0; $bas < 7; $bas++) {
                                        $sty = new StyleJudgementV2($bas / 2, $mov / 2, $din / 2, $com / 2, $sapd / 2, $gcc / 2, $dif / 2, $sog, $pen);
                                        $encoded = styleEncodeV2a($sty);
                                        if (array_key_exists($encoded, $codes)) {
                                            throw new Exception("Code collision: $encoded is already used");
                                        }
                                        $codes[$encoded] = strval($sty);
                                        $decoded = styleDecodeV2a($encoded);
                                        if (!$decoded->equals($sty)) {
                                            throw new Exception("Code $encoded decoded to " . strval($decoded) . ", expected " . strval($sty));
                                        }
                                        $count++;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            if ($dumpCodes) {
                if (!file_exists('out')) {
                    mkdir('out', 0777, true);
                }
                $fileName = "out/style_codes_v2a_php_pen={$pen}_sog={$sog}.json";
                file_put_contents($fileName, json_encode($codes, JSON_PRETTY_PRINT));
                echo "Codes dumped to $fileName\n";
            }
        }
    }

    $expected = pow(7, 7) * 3 * 4;
    if ($count !== $expected) {
        throw new Exception("Count is $count, expected $expected");
    }

    echo "Test passed. $count codes checked.\n";
}

// Run main if this is the entry point
if (basename(__FILE__) === basename($_SERVER['SCRIPT_NAME'])) {
    main();
}

?>
