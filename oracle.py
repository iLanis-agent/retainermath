#!/usr/bin/env python3
# Retainer Math oracle - mirrors engine.js with Fractions and Decimal: hours are exact decimals, the run-out is found by spending a workday at a time, rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def hrs(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    m = re.fullmatch(r"([0-9]{1,4})(?:\.([0-9]))?", t)
    if not m: raise ValueError(err)
    v = F(m[1]) + (F(int(m[2]), 10) if m[2] else 0)
    if not F(str(lo)) <= v <= F(str(hi)): raise ValueError(err)
    return v
def whole(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def dec(fr):  # exact value with at most 2 decimals to text
    d = Decimal(fr.numerator) / Decimal(fr.denominator)
    assert d == d.quantize(Decimal("0.01"))
    s = format(d.quantize(Decimal("0.01")), "f").rstrip("0").rstrip(".")
    return s
def rnd2(fr): return F(int((Decimal(fr.numerator) / Decimal(fr.denominator) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)), 100)
def hours(v): return f"{dec(v)} hour" if v == 1 else f"{dec(v)} hours"
def days(n): return f"{n} workday" if n == 1 else f"{n} workdays"
HERR = "the hours must be a number from 0 to 9999.9 with up to one decimal"
PERR = "the hours a workday must be a number from 0.1 to 24 with up to one decimal"
BERR = "the hours bought must be a number from 0.1 to 9999.9 with up to one decimal"

def pace(b, u, n):
    b = hrs(b, BERR, F(1, 10), F("9999.9")); u = hrs(u, HERR, 0, F("9999.9")); n = whole(n, "the workdays left must be a whole number from 1 to 365", 1, 365)
    if u > b: return f"Hours used: {dec(u)} of {dec(b)} bought, which is {dec(u - b)} over. Nothing is left to spread over {days(n)}."
    if u == b: return f"Hours used: {dec(u)} of {dec(b)} bought, so nothing is left to spread over {days(n)}."
    per = rnd2((b - u) / n)
    return f"Hours left: {dec(b - u)} of {dec(b)} bought, with {dec(u)} used. Spread over {days(n)}, that is {hours(per)} a workday."
def runout(l, p):
    l = hrs(l, HERR, 0, F("9999.9")); p = hrs(p, PERR, F(1, 10), 24)
    head = f"Hours left: {dec(l)} at {hours(p)} a workday"
    if l == 0: return head + ". Nothing is left, so that covers no workdays."
    full = 0; left = l
    while left >= p: left -= p; full += 1
    if full == 0: return head + ": that covers less than one workday."
    if left == 0: return head + f": that covers exactly {days(full)}."
    return head + f": that covers {full} full {'workday' if full == 1 else 'workdays'} and {hours(left)} of the next one."
def rollover(b, u, p, nb):
    b = hrs(b, BERR, F(1, 10), F("9999.9")); u = hrs(u, HERR, 0, F("9999.9"))
    p = whole(p, "the rollover must be a whole number of percent from 0 to 100", 0, 100); nb = hrs(nb, HERR, 0, F("9999.9"))
    un = b - u if u < b else F(0)
    if un == 0: return f"Nothing is unused, so nothing rolls over. Next month has {hours(nb)}."
    carried = rnd2(un * p / 100)
    return f"Unused hours: {dec(un)}. With {p} percent rolling over, {hours(carried)} carry into next month. Added to the {dec(nb)} bought for next month, that makes {hours(nb + carried)}."

FNS = {"paceTruth": pace, "runoutTruth": runout, "rolloverTruth": rollover}

def cases():
    c = []
    for a in [("40","13.5","12"),("40","41","3"),("40","40","1"),("1","0","3"),("0.1","0","1"),("9999.9","0","365"),("9999.9","9999.9","1"),("40","0","7"),("40","39.9","365"),("100","33.3","7"),("10","0","3"),("10","0","6"),("2","1","3"),("2.5","0","8"),
              ("0","0","3"),("10000","0","3"),("40","-1","3"),("40","x","3"),("40","5","0"),("40","5","366"),("40","5","2.5"),("40","5",""),("","5","3"),(" 40 "," 5 "," 3 "),("40","5.55","3")]:
        c.append(("paceTruth", list(a)))
    for a in [("38","3.5"),("3","3.5"),("7","3.5"),("0","1"),("0.1","0.1"),("9999.9","0.1"),("9999.9","24"),("24","24"),("24.1","24"),("10","3"),("10","2.5"),("1","1"),("2","1"),("100","7.7"),("0.5","0.5"),
              ("10001","3"),("10","0"),("10","24.1"),("10","25"),("x","3"),("10",""),("-1","3"),("10","3.55"),(" 38 "," 3.5 ")]:
        c.append(("runoutTruth", list(a)))
    for a in [("40","30","50","40"),("40","39.9","50","0"),("40","40","50","40"),("40","45","50","40"),("40","0","100","0"),("40","0","0","40"),("40","0","100","40"),("40","10","33","40"),("40","10","67","12.5"),("0.1","0","50","0"),("9999.9","0","100","9999.9"),("7","3.3","25","1"),("7","3.4","25","1"),("1","0.9","50","0"),
              ("0","0","50","40"),("40","30","101","40"),("40","30","-1","40"),("40","30","5.5","40"),("40","30","x","40"),("40","30","50","10000"),("40","30","50",""),("40","x","50","40"),(" 40 "," 30 "," 50 "," 40 ")]:
        c.append(("rolloverTruth", list(a)))
    r = random.Random(705)
    def h(hi): return f"{r.randint(0, hi*10)/10:.1f}"
    for _ in range(35):
        b = r.randint(1, 20000) / 10
        c.append(("paceTruth", [f"{b:.1f}", f"{r.randint(0, int(b*10) + 5)/10:.1f}", str(r.randint(1, 365))]))
    for _ in range(35): c.append(("runoutTruth", [h(500), f"{r.randint(1, 240)/10:.1f}"]))
    for _ in range(35):
        b = r.randint(1, 4000) / 10
        c.append(("rolloverTruth", [f"{b:.1f}", f"{r.randint(0, int(b*10) + 5)/10:.1f}", str(r.randint(0, 100)), h(400)]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
