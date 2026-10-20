# Retainer Math

Hours bank arithmetic. With 40 hours bought and 13.5 used, 26.5 hours are left, which is 2.21 hours a workday over the next 12 workdays.

## What it computes

Hours are typed with up to one decimal (0 to 9999.9). Workdays and percents are whole numbers.

- **The pace truth** - hours left of those bought, spread over 1 to 365 workdays, to hundredths of an hour; or how far over if more was used.
- **The run-out truth** - how many full workdays the hours left cover at 0.1 to 24 hours a workday, and the hours spilling into the next one.
- **The rollover truth** - unused hours this month, the share (0 to 100 percent, your own entry) that carries over, and the total with next month's hours.

## Boundary

Arithmetic only. It has not seen any contract, time record or invoice. It does not know what counts as billable, how time is rounded, what the terms say about rollover or overage, or who owes what, and it gives no verdict on any of that. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact tenths of an hour).
- `oracle.py` - the Python mirror (Fractions and Decimal, spends a workday at a time) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (177 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/retainermath/
Repo: https://github.com/iLanis-agent/retainermath
