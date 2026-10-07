tell application "Microsoft Excel"
activate object worksheet "Fishery operations" of workbook "Recitation W6 Completed.xlsx"
set zoom of active window to 100
copy picture range "B2:E10" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/fish_prob.png\""
tell application "Microsoft Excel"
copy picture range "X4:Y9" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/fish_summary.png\""
tell application "Microsoft Excel"
copy picture range "G3:O38" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/fish_first.png\""
tell application "Microsoft Excel"
copy picture range "G39:O73" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/fish_last.png\""
tell application "Microsoft Excel"
end tell