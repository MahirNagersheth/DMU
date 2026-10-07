tell application "Microsoft Excel"
 activate object worksheet "Problem 1"
 set calculation to calculation automatic
 set value of range "H37:I37" to {{"Min slack","Capacity slack"}}
 set formula of range "H38:I41" to {{"=C38-D38","=E38-C38"},{"=C39-D39","=E39-C39"},{"=C40-D40","=E40-C40"},{"=C41-D41","=E41-C41"}}
 set value of range "A47" to "Demand slack"
 set formula of range "B47" to "=B46-D46"
 set value of range "B38:C41" to {{1,3000},{1,3000},{1,4000},{1,2500}}
 set value of range "A48" to "Solver: Min $B$43; change $B$38:$C$41; $B$47 >= 0; $B$38:$B$41 binary; $C$38:$C$41 integer."
 set value of range "A49" to "Linking: $H$38:$I$41 >= 0, where H=C-D and I=E-C. Nonnegative variables."
 set value of range "A50" to "Simplex LP; integer optimality 0%; ignore integer constraints OFF. Saved model: M48:M55."
 run VB Macro "Solver.xlam!SolverReset"
 run VB Macro "Solver.xlam!SolverOk" arg1 "$B$43" arg2 2 arg3 0 arg4 "$B$38:$C$41" arg5 2
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$38:$B$41" arg2 5
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$38:$C$41" arg2 4
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$H$38:$I$41" arg2 3 arg3 "0"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$47" arg2 3 arg3 "0"
 run VB Macro "Solver.xlam!SolverOptions" arg4 true arg6 1 arg9 0 arg10 true arg12 true arg20 false
 set dStatus to run VB Macro "Solver.xlam!SolverSolve" arg1 true
 run VB Macro "Solver.xlam!SolverFinish" arg1 1
 run VB Macro "Solver.xlam!SolverSave" arg1 "$M$48"
 set value of range "K56:L56" to {{"Min slack","Capacity slack"}}
 set value of range "A72" to "Constraints: $K$57:$L$60 >= 0; $C$64:$G$64 = 0. K=H-I; L=J-H; city residuals=delivered-demand."
 set value of range "A73" to "Simplex LP; nonnegative variables; integer optimality 0%; ignore integer constraints OFF. Saved model: M82:M89."
 set value of range "B57:B60" to 1
 set value of range "C57:G60" to 100
 run VB Macro "Solver.xlam!SolverReset"
 run VB Macro "Solver.xlam!SolverOk" arg1 "$B$66" arg2 2 arg3 0 arg4 "$B$57:$G$60" arg5 2
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$57:$B$60" arg2 5
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$57:$G$60" arg2 4
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$K$57:$L$60" arg2 3 arg3 "0"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$64:$G$64" arg2 2 arg3 "0"
 run VB Macro "Solver.xlam!SolverOptions" arg4 true arg6 1 arg9 0 arg10 true arg12 true arg20 false
 set gStatus to run VB Macro "Solver.xlam!SolverSolve" arg1 true
 run VB Macro "Solver.xlam!SolverFinish" arg1 1
 run VB Macro "Solver.xlam!SolverSave" arg1 "$M$82"
 set value of range "A32" to "Simplex LP; nonnegative variables; integer optimality 0%. Saved Solver model: M20:M25."
 save active workbook
 return {dStatus,gStatus,value of range "B43",value of range "B66:B69",value of range "B38:C41",value of range "B57:G60"}
end tell
