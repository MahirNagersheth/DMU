tell application "Microsoft Excel"
activate object worksheet "N analysis" of workbook "Recitation W6 Completed.xlsx"
set zoom of active window to 100
copy picture range "G3:T15" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/n_rows.png\""
tell application "Microsoft Excel"
copy picture range "P494:T503" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/n_last.png\""
tell application "Microsoft Excel"
copy picture range "V36:W40" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/n_summary.png\""
tell application "Microsoft Excel"
copy picture chart of chart object 1 of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/n_chart.png\""
tell application "Microsoft Excel"
end tell