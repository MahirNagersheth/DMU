tell application "Microsoft Excel"
set ch to chart of chart object 1 of worksheet "Airline (c)" of active workbook
set formula of series 1 of ch to "=SERIES(\"Mean profit\",'Airline (c)'!$R$13:$R$19,'Airline (c)'!$S$13:$S$19,1)"
delete series 2 of ch
set ax to get axis ch axis type category axis
set minimum scale of ax to 19
set maximum scale of ax to 25
set ch to chart of chart object 1 of worksheet "Airline (b)" of active workbook
set ax to get axis ch axis type category axis
set minimum scale of ax to 0
set maximum scale of ax to 5100
save active workbook
end tell
