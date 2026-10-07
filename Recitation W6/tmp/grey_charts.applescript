with timeout of 20 seconds
tell application "Microsoft Excel"
set fore color of line format of chart format of series 1 of chart of chart object 1 of worksheet "N analysis" of active workbook to {35,35,35}
set fore color of line format of chart format of series 2 of chart of chart object 1 of worksheet "N analysis" of active workbook to {120,120,120}
set fore color of line format of chart format of series 3 of chart of chart object 1 of worksheet "N analysis" of active workbook to {175,175,175}
set fore color of line format of chart format of series 1 of chart of chart object 1 of worksheet "Analysis on Q" of active workbook to {35,35,35}
set fore color of line format of chart format of series 1 of chart of chart object 1 of worksheet "Airline (b)" of active workbook to {35,35,35}
set fore color of line format of chart format of series 2 of chart of chart object 1 of worksheet "Airline (b)" of active workbook to {120,120,120}
set fore color of line format of chart format of series 3 of chart of chart object 1 of worksheet "Airline (b)" of active workbook to {175,175,175}
set fore color of line format of chart format of series 1 of chart of chart object 1 of worksheet "Airline (c)" of active workbook to {35,35,35}
set fore color of line format of chart format of series 1 of chart of chart object 1 of worksheet "Fishery operations" of active workbook to {35,35,35}
set fore color of line format of chart format of series 1 of chart of chart object 2 of worksheet "Fishery operations" of active workbook to {35,35,35}
save active workbook
end tell
end timeout