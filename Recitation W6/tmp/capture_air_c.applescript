tell application "Microsoft Excel"
activate object worksheet "Airline (c)" of workbook "Recitation W6 Completed.xlsx"
set zoom of active window to 100
copy picture range "R2:S19" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/air_limits.png\""
tell application "Microsoft Excel"
copy picture chart of chart object 1 of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/air_chart.png\""
tell application "Microsoft Excel"
end tell