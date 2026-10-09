# Stuck parcels check (Maya B test task)

Google Sheet (view): https://docs.google.com/spreadsheets/d/1j-qCsRdKpHl9rF1blK6gVyzYbV6dJ1wdOFeHYwliScU/edit?usp=sharing

Files:
- `tracking.csv`: source export (1000 rows).
- `stuck_parcels.py`: pure Python, no dependencies. Finds stuck parcels, prints counts per carrier, writes `stuck_parcels.json` and `stuck_parcels.csv` with reason, idle days and priority.
- `sheets_formulas.md`: same logic as Google Sheets formulas with a `today` cell.
- `stuck_parcels.xlsx` / `build_xlsx.py`: the workbook behind the Google Sheet and the script that builds it from the raw export.
- `part2.md`: decision, letter review, voice script, prompts, observations.

How to use:
```
python stuck_parcels.py tracking.csv                      # base rules
python stuck_parcels.py tracking.csv --customs-days 5     # customs rule on
python stuck_parcels.py tracking.csv --today 2026-10-20 --customs-days 5
```
Tomorrow: replace `tracking.csv` with the new export, run the same command. Rules live at the top of the script or in the flags.

Results, today = 15.10.2026:

| Carrier     | Base rules | Customs >= 5 |
|-------------|-----------:|-------------:|
| AndesCargo  | 61 | 65 |
| SwiftParcel | 58 | 64 |
| PostLink    | 19 | 19 |
| Total       | 138 | 148 |

Rule change added 10 parcels, all "Held at customs" 5 to 6 days old (AndesCargo +4, SwiftParcel +6).
