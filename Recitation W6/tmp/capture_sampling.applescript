tell application "Microsoft Excel"
activate object worksheet "Sampling" of workbook "Recitation W6 Completed.xlsx"
set zoom of active window to 100
copy picture range "B2:E7" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/sampling_prob.png\""
tell application "Microsoft Excel"
copy picture range "G2:L17" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/sampling.png\""
tell application "Microsoft Excel"
end tell