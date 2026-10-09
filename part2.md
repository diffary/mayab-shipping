# Part 2

## 2.1 Which carrier to escalate first

Numbers after the rule change (today 15.10.2026, idle >= 7, customs >= 5):

| Carrier     | Stuck | Of total | Share | Address issue | Customs | Idle 7+ (transit / label / out for delivery) |
|-------------|-------|----------|-------|---------------|---------|------------------|
| AndesCargo  | 65    | 450      | 14%   | 14            | 20      | 31               |
| SwiftParcel | 64    | 300      | 21%   | 14            | 23      | 27               |
| PostLink    | 19    | 250      | 8%    | 6             | 2       | 11               |

Decision: escalate SwiftParcel first.

- Share of stuck parcels is the highest, 21% vs 14% at AndesCargo. Volume difference (65 vs 64) is one parcel, share difference is 1.5x.
- SwiftParcel has the most parcels stuck at customs (23), and the rule change added 6 of them, so the problem is growing there.
- Same count of Address issue as AndesCargo (14), but on a smaller base.

AndesCargo goes second, same week. PostLink is fine for now.

## 2.2 Draft letter review

Errors found:

1. AC17088206 is an AndesCargo parcel (prefix AC, order 100009). It must not be in a letter to SwiftParcel.
2. SP8115549 was delivered on 17.09 (order 100006). "No updates since 17.09" is wrong, the line must be removed.
3. SP7880704: draft says "no movement for 27 days", data says last event 25.09, that is 20 days.
4. "As agreed on our call last week" is invented. No such agreement exists in the data or the task.
5. "All delayed parcels will be delivered by 20.10" is an invented commitment.
6. Threatening tone ("unacceptable", "we will stop working with you") on a first request. Bad for the relationship and not needed.
7. "Reply by end of day" is not realistic for a carrier with 64 stuck parcels. Two business days is a normal ask.
8. The letter lists 5 parcels, but SwiftParcel has 64 stuck. Better to attach the full list and name the top ones in the body.
9. No order numbers, no total count, no clear ask per parcel type. Added.

Verified OK in draft: SP9283796 address issue since 05.10 (correct), SP6960980 label created 29.09 with no pickup scan (correct, 16 days).

Corrected letter:

---
Subject: SwiftParcel: 64 shipments without movement, status request

Hello SwiftParcel team,

We are reviewing our shipments as of 15 October and see 64 parcels with no tracking update for 7 days or more (5 days or more for parcels held at customs). The full list is attached (order, tracking number, last event, days without movement).

Could you please check these first:

1. SP9283796 (order 100537), "Address issue" since 05.10, 10 days. Please tell us which address details are missing so we can confirm them with the customer.
2. SP7880704 (order 100349), "In transit" since 25.09, 20 days with no scan. Please share the current location and status.
3. SP6960980 (order 100250), "Label created" on 29.09, no pickup scan for 16 days. Please confirm whether the parcel was collected.

For the rest of the list, please let us know which parcels are still moving, which are held at customs and what documents are needed, and which are lost so we can start claims.

We would appreciate a reply within two business days, by 17 October.

Thank you for your help.

Best regards,
[Name]
Shipping team, [Company]
---

## 2.3 Voice message script (60 to 90 seconds, B1 English)

Parcel: SP9283796, order 100537, Address issue since 05.10, 10 days, Brazil.

---
Hello, my name is [Name]. I am calling from [Company]. We are an online store and we ship with SwiftParcel.

I am calling about one parcel. The tracking number is S-P-9-2-8-3-7-9-6. I repeat, S-P, nine, two, eight, three, seven, nine, six. Our order number is 100537.

The parcel was shipped on 28 September to Brazil. On 5 October the status changed to "Address issue". Since then there is no update. That is ten days.

I have two questions. First, what exactly is wrong with the address? Is the street missing, the postal code, or the phone number? Second, what do you need from us to deliver the parcel? We can confirm the address with the customer today.

Please send the answer to our email, shipping at [company] dot com. If you need to call me back, my number is [phone].

Thank you very much. Goodbye.
---

Tips: read slowly, pause after the tracking number, about 75 seconds at normal pace. Record on phone, export mp3.

## 2.4 Prompts used and what was checked by hand

Prompts (Claude Code, in Russian, paraphrased):

1. Read the CSV and show stuck parcels per carrier under rules 1 and 2, today = 15.10.2026.
2. Explain the priority: is the top parcel the one with the most idle days? (clarified the two-level priority)
3. Write a pure Python script, no pandas, rules as parameters, editable today, JSON export.
4. Rule 1 in the original task means not delivered and not returned, recount. (after pasting the full task text)
5. Write Google Sheets formulas with a today cell and a rules sheet.
6. Check every tracking number from the draft letter against the data.
7. Rewrite the letter in a neutral tone, realistic deadline, no invented facts.
8. Write a 60 to 90 second phone script in simple English.

Checked by hand:

- Opened the CSV and confirmed 1000 rows and 7 columns, header names.
- Recounted stuck totals two ways. First pass with a narrower reading of rule 1 (only "In transit") gave 81 / 126, full rule gave 138 / 148. Kept the full rule, because the task says "not delivered and not returned".
- Looked up each of the 5 tracking numbers from the draft letter in the sheet: prefix, carrier, last event, date.
- Recomputed idle days for SP7880704 by hand: 15.10 minus 25.09 = 20, not 27.
- Ran the script with --today 2026-10-20 and checked that counts grow.
- Checked the three rows with empty tracking and the three duplicated tracking numbers in the sheet.

## 1.4 Observations beyond the rules

- 3 orders (100053, 100354, 100610) have no tracking number, no event and no date. Shipped 23 to 27.09. Rules skip them because there is no event date. Proposal: flag "no tracking" as its own stuck reason.
- 3 tracking numbers are used by two orders each: PL52352674, AC47947905, SP2128715. All marked Delivered. Looks like copy-paste in the export. Proposal: duplicate check on import.
- 2 AndesCargo rows have the event date before the ship date (100186, 100982). Data error or wrong column.
- 18 "Label created" parcels are 7+ days old. The carrier never picked them up. They count as stuck by rule 1, but the action is different (ask for pickup, not for tracing). Proposal: separate reason "not collected".
- 4 "Out for delivery" parcels at AndesCargo are 7+ days old. A failed delivery attempt usually gets its own status. Worth asking the carrier.
- Rule 2 does not look at the age of "Address issue". A 1-day and a 10-day address issue land in the same group. Fine for the list, but the customer contact should start on day 1.
- "Returned to sender" (18) is excluded by the rules, but each return costs money and needs a refund or reship decision.
- Country column is in Ukrainian, carriers and statuses in English. Not a problem for the formulas, but a lookup table would help if the export changes.
