tell application "Microsoft Excel"
 activate object worksheet "Problem 1"
 set calculation to calculation automatic
 set formula of range "K57:K60" to {{"=H57-I57"},{"=H58-I58"},{"=H59-I59"},{"=H60-I60"}}
 set formula of range "L57:L60" to {{"=J57-H57"},{"=J58-H58"},{"=J59-H59"},{"=J60-H60"}}
 set value of range "B57:B60" to {{0},{1},{1},{0}}
 set value of range "C57:G60" to {{0,0,0,0,0},{1000,3000,2000,1000,0},{0,0,1000,0,4000},{0,0,0,0,0}}
 run VB Macro "Solver.xlam!SolverReset"
 run VB Macro "Solver.xlam!SolverOk" arg1 "$B$66" arg2 2 arg3 0 arg4 "$B$57:$G$60" arg5 2
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$B$57:$B$60" arg2 5
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$57:$G$60" arg2 4
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$K$57:$L$60" arg2 3 arg3 "0"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$64:$G$64" arg2 2 arg3 "0"
 run VB Macro "Solver.xlam!SolverOptions" arg4 true arg6 1 arg9 0 arg10 true arg12 true arg20 false
 set beforeValue to value of range "B66"
 set solveStatus to run VB Macro "Solver.xlam!SolverSolve" arg1 true
 save active workbook
 return {beforeValue,solveStatus,value of range "B66",value of range "B57:L60"}
end tell
