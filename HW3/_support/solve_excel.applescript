tell application "Microsoft Excel"
 activate
 open POSIX file "/Users/mahir/Downloads/DMU/HW3/HW3_Solved.xlsx"
 activate object worksheet "Problem 1"
 set calculation to calculation automatic
 run VB Macro "Solver.xlam!SolverReset"
 run VB Macro "Solver.xlam!SolverOk" arg1 "$B$27" arg2 2 arg3 0 arg4 "$B$22:$B$25" arg5 2
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$22:$B$25" arg2 5
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$28" arg2 3 arg3 "$D$28"
 run VB Macro "Solver.xlam!SolverOptions" arg4 true arg6 1 arg9 0 arg10 true arg12 true arg20 false
 set s1 to run VB Macro "Solver.xlam!SolverSolve" arg1 true
 run VB Macro "Solver.xlam!SolverFinish" arg1 1
 run VB Macro "Solver.xlam!SolverSave" arg1 "$M$20"
 set calculation to calculation automatic
 run VB Macro "Solver.xlam!SolverReset"
 run VB Macro "Solver.xlam!SolverOk" arg1 "$B$43" arg2 2 arg3 0 arg4 "$B$38:$C$41" arg5 2
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$38:$B$41" arg2 5
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$38:$C$41" arg2 4
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$38:$C$41" arg2 3 arg3 "$D$38:$D$41"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$38:$C$41" arg2 1 arg3 "$E$38:$E$41"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$46" arg2 3 arg3 "$D$46"
 run VB Macro "Solver.xlam!SolverOptions" arg4 true arg6 1 arg9 0 arg10 true arg12 true arg20 false
 set s2 to run VB Macro "Solver.xlam!SolverSolve" arg1 true
 run VB Macro "Solver.xlam!SolverFinish" arg1 1
 run VB Macro "Solver.xlam!SolverSave" arg1 "$M$48"
 set calculation to calculation automatic
 run VB Macro "Solver.xlam!SolverReset"
 run VB Macro "Solver.xlam!SolverOk" arg1 "$B$66" arg2 2 arg3 0 arg4 "$B$57:$G$60" arg5 2
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$57:$B$60" arg2 5
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$57:$G$60" arg2 4
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$H$57:$H$60" arg2 3 arg3 "$I$57:$I$60"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$H$57:$H$60" arg2 1 arg3 "$J$57:$J$60"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$62:$G$62" arg2 2 arg3 "$C$63:$G$63"
 run VB Macro "Solver.xlam!SolverOptions" arg4 true arg6 1 arg9 0 arg10 true arg12 true arg20 false
 set s3 to run VB Macro "Solver.xlam!SolverSolve" arg1 true
 run VB Macro "Solver.xlam!SolverFinish" arg1 1
 run VB Macro "Solver.xlam!SolverSave" arg1 "$M$82"
 save active workbook
 set p1Results to {value of range "B27", value of range "B43", value of range "B66:B69", value of range "B57:H60"}
 activate object worksheet "Problem 2"
 set calculation to calculation automatic
 run VB Macro "Solver.xlam!SolverReset"
 run VB Macro "Solver.xlam!SolverOk" arg1 "$B$43" arg2 1 arg3 0 arg4 "$B$24:$G$37" arg5 2
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$24:$G$37" arg2 5
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$39:$G$39" arg2 2 arg3 "1"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$H$24:$H$37" arg2 1 arg3 "2"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$I$24:$L$37" arg2 1 arg3 "1"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$H$37" arg2 2 arg3 "2"
 run VB Macro "Solver.xlam!SolverOptions" arg4 true arg6 1 arg9 0 arg10 true arg12 true arg20 false
 set s4 to run VB Macro "Solver.xlam!SolverSolve" arg1 true
 run VB Macro "Solver.xlam!SolverFinish" arg1 1
 run VB Macro "Solver.xlam!SolverSave" arg1 "$N$5"
 save active workbook
 return {{s1,s2,s3,s4},p1Results,value of range "B43",value of range "B40:G41"}
end tell
