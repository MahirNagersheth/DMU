tell application "Microsoft Excel"
activate object worksheet "N analysis" of active workbook
set value of range "V36:V40" of active sheet to {{"Final n"},{"Mean profit"},{"Sample SD"},{"Lower 95% CI"},{"Upper 95% CI"}}
set formula of range "W36:W40" of active sheet to {{"=P503"},{"=Q503"},{"=R503"},{"=S503"},{"=T503"}}
set column width of range "V:V" of active sheet to 22
set column width of range "W:W" of active sheet to 20
set number format of range "W37:W40" of active sheet to "$#,##0.00"
activate object worksheet "Airline (b)" of active workbook
set formula of series 1 of chart of chart object 1 of active sheet to "=SERIES('Airline (b)'!$M$3,'Airline (b)'!$L$5:$L$5103,'Airline (b)'!$M$5:$M$5103,1)"
set formula of series 2 of chart of chart object 1 of active sheet to "=SERIES('Airline (b)'!$O$3,'Airline (b)'!$L$5:$L$5103,'Airline (b)'!$O$5:$O$5103,2)"
set formula of series 3 of chart of chart object 1 of active sheet to "=SERIES('Airline (b)'!$P$3,'Airline (b)'!$L$5:$L$5103,'Airline (b)'!$P$5:$P$5103,3)"
activate object worksheet "Airline (c)" of active workbook
set name of series 1 of chart of chart object 1 of active sheet to "Mean profit"
repeat with sheetName in {"Fishery operations", "N analysis", "Analysis on Q", "Airline (b)", "Airline (c)"}
set s to worksheet sheetName of active workbook
repeat with ch in every chart object of s
set indexNumber to 0
repeat with ser in every series of chart of ch
set indexNumber to indexNumber + 1
if indexNumber is 1 then
set color of border of ser to {35,35,35}
else
set color of border of ser to {145,145,145}
end if
end repeat
end repeat
end repeat
save active workbook
end tell
