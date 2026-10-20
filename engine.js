// Retainer Math engine: hours-bank arithmetic. Hours left spread over workdays, how long the hours last at a daily rate, and what rolls over. Hours in exact tenths, results to hundredths.
function _hrs(t, err, lo, hi) { // hours text with up to one decimal, returned as tenths
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,4})(?:\.([0-9]))?$/.exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * 10 + (m[2] ? parseInt(m[2], 10) : 0);
  if (v < lo * 10 || v > hi * 10) throw new Error(err);
  return v;
}
function _int(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,4}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _d(h, places) { // integer in 10^places units to text, trailing zeros dropped
  var base = places === 1 ? 10 : 100, s = String(Math.floor(h / base)), f = h % base;
  if (f === 0) return s;
  var fs = places === 1 ? String(f) : (f < 10 ? "0" + f : String(f)).replace(/0$/, "");
  return s + "." + fs;
}
function _hours(v, places) { return _d(v, places) + (v === (places === 1 ? 10 : 100) ? " hour" : " hours"); }
function _days(n) { return n + (n === 1 ? " workday" : " workdays"); }
var _HERR = "the hours must be a number from 0 to 9999.9 with up to one decimal";
var _PERR = "the hours a workday must be a number from 0.1 to 24 with up to one decimal";

function paceTruth(bought, used, workdaysLeft) {
  var b = _hrs(bought, "the hours bought must be a number from 0.1 to 9999.9 with up to one decimal", 0.1, 9999.9);
  var u = _hrs(used, _HERR, 0, 9999.9);
  var n = _int(workdaysLeft, "the workdays left must be a whole number from 1 to 365", 1, 365);
  if (u > b) return "Hours used: " + _d(u, 1) + " of " + _d(b, 1) + " bought, which is " + _d(u - b, 1) + " over. Nothing is left to spread over " + _days(n) + ".";
  if (u === b) return "Hours used: " + _d(u, 1) + " of " + _d(b, 1) + " bought, so nothing is left to spread over " + _days(n) + ".";
  var rem = b - u, per = Math.floor((2 * rem * 10 + n) / (2 * n));
  return "Hours left: " + _d(rem, 1) + " of " + _d(b, 1) + " bought, with " + _d(u, 1) + " used. Spread over " + _days(n) + ", that is " + _hours(per, 2) + " a workday.";
}
function runoutTruth(hoursLeft, perDay) {
  var l = _hrs(hoursLeft, _HERR, 0, 9999.9);
  var p = _hrs(perDay, _PERR, 0.1, 24);
  var full = Math.floor(l / p), rest = l - full * p;
  var head = "Hours left: " + _d(l, 1) + " at " + _hours(p, 1) + " a workday";
  if (l === 0) return head + ". Nothing is left, so that covers no workdays.";
  if (full === 0) return head + ": that covers less than one workday.";
  if (rest === 0) return head + ": that covers exactly " + _days(full) + ".";
  return head + ": that covers " + full + " full " + (full === 1 ? "workday" : "workdays") + " and " + _hours(rest, 1) + " of the next one.";
}
function rolloverTruth(bought, used, rollPct, nextBought) {
  var b = _hrs(bought, "the hours bought must be a number from 0.1 to 9999.9 with up to one decimal", 0.1, 9999.9);
  var u = _hrs(used, _HERR, 0, 9999.9);
  var p = _int(rollPct, "the rollover must be a whole number of percent from 0 to 100", 0, 100);
  var nb = _hrs(nextBought, _HERR, 0, 9999.9);
  var un = u >= b ? 0 : b - u;
  if (un === 0) return "Nothing is unused, so nothing rolls over. Next month has " + _hours(nb * 10, 2) + ".";
  var carried = Math.floor((2 * un * p + 10) / 20), total = nb * 10 + carried;
  return "Unused hours: " + _d(un, 1) + ". With " + p + " percent rolling over, " + _hours(carried, 2) + " carry into next month. Added to the " + _d(nb, 1) + " bought for next month, that makes " + _hours(total, 2) + ".";
}
