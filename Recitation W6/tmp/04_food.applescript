tell application "Microsoft Excel"
set display alerts to false
set calculation to calculation manual
activate object worksheet "Food bank" of active workbook
set value of range "D29:F32" of active sheet to {{210.0,250.0,240.0},{90.0,0.0,20.0},{70.0,130.0,30.0},{80.0,10.0,0.0}}
set number format of range "D57:D60" of active sheet to "\"$\"#,##0.00"
set number format of range "G57" of active sheet to "\"$\"#,##0.00"
set calculation to calculation automatic
calculate full
save active workbook
end tell
