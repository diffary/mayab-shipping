Subject: Re: Test task, Shipping Automation Manager

Hello [Name],

Thank you for the task. Please find my work below.

Links
- Google Sheet (view): https://docs.google.com/spreadsheets/d/1j-qCsRdKpHl9rF1blK6gVyzYbV6dJ1wdOFeHYwliScU/edit?usp=sharing
- Script, JSON export and all write-ups: https://github.com/diffary/mayab-stuck-parcels
- Voice message: [link to mp3]

Part 1

Stuck parcels, today = 15.10.2026:

| Carrier     | Base rules | After customs rule (5 days) |
|-------------|-----------:|----------------------------:|
| AndesCargo  | 61 | 65 |
| SwiftParcel | 58 | 64 |
| PostLink    | 19 | 19 |
| Total       | 138 | 148 |

The rule change added 10 parcels, all "Held at customs" for 5 or 6 days (AndesCargo +4, SwiftParcel +6). The full prioritized list after the change is in the sheet (Data tab, filter column "reason", sort by "priority") and in stuck_parcels.csv / stuck_parcels.json in the repository.

How to use: paste a new export into the Data tab (columns A to G), set the date in Rules!B1, and every row gets a reason, idle days and priority, while the Summary tab counts stuck parcels per carrier. Rules!B2 is the idle threshold, Rules!B3 is the customs threshold (leave it empty to switch that rule off). The Python script does the same from a CSV with no dependencies: python stuck_parcels.py tracking.csv --today 2026-10-15 --customs-days 5. I checked that the sheet and the script give the same 148 rows, reasons and priorities.

Observations beyond the rules, with proposals, are in part2.md, section 1.4. The main ones: 3 orders have no tracking number at all, 3 tracking numbers are shared by two orders each, 2 rows have the event date before the ship date, and 18 "Label created" parcels were never collected and need a pickup request rather than a trace.

Part 2

Escalate SwiftParcel first. After the rule change it has 64 stuck parcels out of 300 (21%) against 65 out of 450 at AndesCargo (14%). SwiftParcel also has the most parcels held at customs (23). Details in part2.md, section 2.1.

The corrected letter and the list of errors in the draft (9 points, including a wrong carrier, a delivered parcel listed as stuck, wrong day count, invented agreement and deadline, and tone) are in part2.md, section 2.2.

The voice message is about SP9283796 (order 100537), "Address issue" since 05.10, the SwiftParcel parcel with the highest priority. The script I read is in section 2.3.

Prompts and what I verified by hand are in section 2.4.

Assumptions: "still on the way" means any status except Delivered and Returned to sender. Rows without an event date are not counted as stuck by the rules, but are listed in the observations.

Happy to walk through any decision or change a rule live on the call.

Best regards,
[Your name]
