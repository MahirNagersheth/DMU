tell application "Microsoft Excel"
activate object worksheet "Analysis on Q" of workbook "Recitation W6 Completed.xlsx"
set zoom of active window to 100
copy picture range "Q3:R14" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/q_inputs.png\""
tell application "Microsoft Excel"
copy picture range "T3:U44" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/q_table.png\""
tell application "Microsoft Excel"
copy picture chart of chart object 1 of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/q_chart.png\""
tell application "Microsoft Excel"
end tell