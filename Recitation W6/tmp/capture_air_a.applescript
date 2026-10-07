tell application "Microsoft Excel"
activate object worksheet "Airline (a)" of workbook "Recitation W6 Completed.xlsx"
set zoom of active window to 100
copy picture range "B3:K16" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/air_rows.png\""
tell application "Microsoft Excel"
copy picture range "R2:S13" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/air_summary.png\""
tell application "Microsoft Excel"
end tell