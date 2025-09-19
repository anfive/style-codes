
import argparse
from style_codes_v2a import StyleJudgementV2, style_encode_v2a, style_decode_v2a
import random

CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789 '
LENGTH = 6

def check_invalid(valid, code_chars):
    code = ''.join(CHARS[i] for i in code_chars)
    if code not in valid:
        try:
            decoded = style_decode_v2a(code)
        except Exception as e:
            return
        # Code might have been decoded as having SOG or PEN, check if it is valid after all
        try:
            encoded = style_encode_v2a(decoded)
            if encoded == code and (decoded.sog != 0 or decoded.pen != 0):
                return
        except Exception as e:
            pass
        raise Exception(f'Invalid code {code} was erroneously decoded to {decoded}')

def monte_carlo_loop(valid, id):
    count = 0
    while True:
        code_chars = [random.randint(0, len(CHARS) - 1) for _ in range(LENGTH)]
        check_invalid(valid, code_chars)
        count += 1
        if count % 100000 == 0:
            print(f'Process {id}: {count} checked')

def test_invalid(exhaustive):

    print('Generating all valid codes with zero SOG and PEN...')
    valid = set()
    for sapd in range(0, 7):
        for dif in range(0, 7):
            for com in range(0, 7):
                for din in range(0, 7):
                    for gcc in range(0, 7):
                        for mov in range(0, 7):
                            for bas in range(0, 7):
                                sty = StyleJudgementV2(bas / 2, mov / 2, din / 2, com / 2, sapd / 2, gcc / 2, dif / 2, 0, 0)
                                encoded = style_encode_v2a(sty)
                                valid.add(encoded)
 
    expected = (7 ** 7)
    print(f'Generated {len(valid)} valid codes.')
    if len(valid) != expected:
        raise Exception(f'Count is {len(valid)}, expected {expected}')

    if exhaustive:
        print ('Running exhaustive test')
        current_code = [0] * LENGTH
        count = 0
        total = len(CHARS) ** LENGTH
        while True:
            check_invalid(valid, current_code)
            count += 1
            if count % 100000 == 0:
                print(f'{count}/{total} checked')
            current_digit = LENGTH - 1
            while current_digit >= 0:
                current_code[current_digit] += 1
                if current_code[current_digit] == len(CHARS):
                    current_code[current_digit] = 0
                    current_digit -= 1
                else:
                    break
            
            if current_digit < 0:
                print('Test passed')
                break
    else:
        print ('Running Monte Carlo test')

        import multiprocessing
        processes = []
        for i in range(8):
            process = multiprocessing.Process(target=monte_carlo_loop, args=(valid, i))
            processes.append(process)
            process.start()

        # install signal handler to join processes on SIGINT
        def signal_handler(signum, frame):
            for process in processes:
                process.terminate()
            exit(0)
        import signal
        signal.signal(signal.SIGINT, signal_handler)

        for process in processes:
            process.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run invalid style codes tests')
    parser.add_argument('--exhaustive', action='store_true', 
                       help='Run exhaustive test (Monte Carlo otherwise)')
    
    args = parser.parse_args()
    
    test_invalid(args.exhaustive)