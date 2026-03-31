import json
import mpmath
from datetime import datetime

mpmath.mp.dps = 100  # 100 decimal places

def ramanujan_pi(terms=10):
    total = mpmath.mpf(0)
    for k in range(terms):
        num = mpmath.fac(4*k) * (1103 + 26390*k)
        den = (mpmath.fac(k)**4) * (396**(4*k))
        total += num/den
    pi = 1 / (total * (2*mpmath.sqrt(2)/9801))
    return pi

if __name__ == "__main__":
    pi = ramanujan_pi(10)
    print(f"Pi calculated: {pi}")
    print(f"Time: {datetime.now()}")
    import json

def save_pi_digits(pi_value, filename="pi_state.json"):
    digits = str(pi_value)[2:]  # remove "3."
    with open(filename, "w") as f:
        json.dump({
            "digits": digits,
            "computed_at": datetime.now().isoformat(),
            "terms": 10
        }, f)
    print(f"Saved {len(digits)} digits to {filename}")

if __name__ == "__main__":
    pi = ramanujan_pi(10)
    print(f"Pi: {pi}")
    save_pi_digits(pi)