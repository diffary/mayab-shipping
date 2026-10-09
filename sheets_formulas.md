# Google Sheets variant

Sheet 1 `Data` = raw export, columns A:G (Order, Country, Carrier, Tracking, Ship date, Last event, Last event date), header in row 1.

Sheet 2 `Rules` = editable parameters.

| cell | label          | value       |
|------|----------------|-------------|
| B1   | today          | 15.10.2026  |
| B2   | idle_days      | 7           |
| B3   | customs_days   | 5 (leave empty to switch the customs rule off) |

Add to `Data` three helper columns. Paste in row 2, then fill down (or use ARRAYFORMULA).

H2 days idle
```
=IF(G2="","",Rules!$B$1-G2)
```

I2 reason (empty = not stuck)
```
=IF(F2="Address issue","address issue",
 IF(OR(F2="Delivered",F2="Returned to sender",G2=""),"",
 IF(AND(Rules!$B$3<>"",F2="Held at customs",H2>=Rules!$B$3),"customs >= "&Rules!$B$3&" days",
 IF(H2>=Rules!$B$2,"idle >= "&Rules!$B$2&" days",""))))
```

J2 priority (1 = first to handle, empty = not stuck)
```
=IF(I2="","",
 COUNTIF($I$2:$I$1001,"address issue")*(F2<>"Address issue")
 +COUNTIFS($I$2:$I$1001,"?*",$F$2:$F$1001,IF(F2="Address issue","Address issue","<>Address issue"),$H$2:$H$1001,">"&H2)
 +1)
```
Explanation: address-issue rows come first, inside each group the longest idle gets the lowest number. Ties share a number.

Sheet 3 `Summary`
```
A1 Carrier     B1 Stuck
A2 AndesCargo  B2 =COUNTIFS(Data!$C$2:$C$1001,A2,Data!$I$2:$I$1001,"?*")
A3 SwiftParcel B3 =COUNTIFS(Data!$C$2:$C$1001,A3,Data!$I$2:$I$1001,"?*")
A4 PostLink    B4 =COUNTIFS(Data!$C$2:$C$1001,A4,Data!$I$2:$I$1001,"?*")
A5 Total       B5 =SUM(B2:B4)
```

Prioritized list (new sheet `Stuck`):
```
=SORT(FILTER(Data!A2:J1001, Data!I2:I1001<>""), 10, TRUE)
```

Tomorrow: paste the new export into `Data` A:G, change `Rules!B1`, everything recalculates.
Rule change: type 5 into `Rules!B3`, clear it to go back.

Expected numbers (today 15.10.2026): customs off -> 138 (AndesCargo 61, SwiftParcel 58, PostLink 19); customs 5 -> 148 (65 / 64 / 19).
