"""Find stuck parcels. Pure Python, no pandas.

Usage:
    python stuck_parcels.py tracking.csv
    python stuck_parcels.py tracking.csv --today 2026-10-15 --customs-days 5
"""
import csv
import json
import sys
from datetime import date, datetime

# ---- rules (parameters) -------------------------------------------------
TODAY = date(2026, 10, 15)      # editable "today"
IDLE_DAYS = 7                   # parcel still on the way is stuck after N idle days
FINAL_STATUSES = {"Delivered", "Returned to sender"}  # not on the way anymore
ALWAYS_STUCK = {"Address issue"}  # stuck regardless of days
CUSTOMS_DAYS = None             # "Held at customs" is stuck after N days, None = rule off
# -------------------------------------------------------------------------


def parse_date(text):
    """'25.09.2026' -> date. Empty -> None."""
    text = text.strip()
    if not text:
        return None
    return datetime.strptime(text, "%d.%m.%Y").date()


def days_idle(row, today):
    event_date = parse_date(row["Last event date"])
    if event_date is None:
        return None
    return (today - event_date).days


def stuck_reason(row, today, idle_days, customs_days, final_statuses, always_stuck):
    """Return the rule that fired, or None if the parcel is fine."""
    status = row["Last event"].strip()
    if status in always_stuck:
        return f"always stuck: {status}"
    if status in final_statuses:
        return None
    idle = days_idle(row, today)
    if idle is None:
        return None
    if customs_days is not None and status == "Held at customs" and idle >= customs_days:
        return f"customs >= {customs_days} days"
    if idle >= idle_days:
        return f"idle >= {idle_days} days"
    return None


def priority_key(row):
    """Address issue first, then longest idle."""
    is_address = row["Last event"] in ALWAYS_STUCK
    return (0 if is_address else 1, -(row["days_idle"] or 0))


def main():
    args = sys.argv[1:]
    path = args[0] if args else "tracking.csv"
    today = TODAY
    customs_days = CUSTOMS_DAYS
    if "--today" in args:
        today = date.fromisoformat(args[args.index("--today") + 1])
    if "--customs-days" in args:
        customs_days = int(args[args.index("--customs-days") + 1])

    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    stuck = []
    for row in rows:
        reason = stuck_reason(row, today, IDLE_DAYS, customs_days, FINAL_STATUSES, ALWAYS_STUCK)
        if reason:
            row["days_idle"] = days_idle(row, today)
            row["reason"] = reason
            stuck.append(row)
    stuck.sort(key=priority_key)
    for number, row in enumerate(stuck, start=1):
        row["priority"] = number

    per_carrier = {}
    for row in stuck:
        per_carrier[row["Carrier"]] = per_carrier.get(row["Carrier"], 0) + 1

    print(f"today = {today}, idle >= {IDLE_DAYS} days, customs >= {customs_days}")
    print(f"stuck total: {len(stuck)} of {len(rows)}")
    for carrier, count in sorted(per_carrier.items(), key=lambda x: -x[1]):
        print(f"  {carrier}: {count}")
    print("top 5 by priority:")
    for row in stuck[:5]:
        print(f"  #{row['priority']} {row['Order']} {row['Carrier']} {row['Tracking']} {row['Last event']} {row['days_idle']} d ({row['reason']})")

    result = {
        "today": today.isoformat(),
        "rules": {"idle_days": IDLE_DAYS, "customs_days": customs_days, "final_statuses": sorted(FINAL_STATUSES),
                  "always_stuck": sorted(ALWAYS_STUCK)},
        "total_rows": len(rows),
        "stuck_total": len(stuck),
        "stuck_per_carrier": per_carrier,
        "stuck_parcels": stuck,
    }
    out = "stuck_parcels.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    with open("stuck_parcels.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(stuck[0].keys()))
        writer.writeheader()
        writer.writerows(stuck)
    print(f"saved {out} and stuck_parcels.csv")


if __name__ == "__main__":
    main()
