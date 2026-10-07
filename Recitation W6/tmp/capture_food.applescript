tell application "Microsoft Excel"
activate object worksheet "Food bank" of workbook "Recitation W6 Completed.xlsx"
set zoom of active window to 100
copy picture range "B4:F24" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/food_params.png\""
tell application "Microsoft Excel"
copy picture range "H4:K10" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/food_costs.png\""
tell application "Microsoft Excel"
copy picture range "C28:F32" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/food_decisions.png\""
tell application "Microsoft Excel"
copy picture range "C36:F53" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/food_constraints.png\""
tell application "Microsoft Excel"
copy picture range "C55:G60" of active sheet
end tell
do shell script "/usr/bin/swift -module-cache-path /tmp/w6-swift-cache \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/clipboard_image.swift\" \"/Users/mahir/Downloads/DMU/Recitation W6/tmp/captures/food_objective.png\""
tell application "Microsoft Excel"
end tell