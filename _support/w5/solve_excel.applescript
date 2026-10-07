tell application "Microsoft Excel"
 activate
 open POSIX file "/Users/mahir/Downloads/DMU/_support/w5/Recitation_W5_Solved.xlsx"
 run VB Macro "Solver.xlam!SolverReset"
 run VB Macro "Solver.xlam!SolverOk" arg1 "$D$33" arg2 1 arg3 0 arg4 "$C$21:$D$30" arg5 2
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$21:$C$30" arg2 5
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$D$21:$D$30" arg2 4
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$D$21:$D$30" arg2 3 arg3 "$E$21:$E$30"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$D$21:$D$30" arg2 1 arg3 "$F$21:$F$30"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$37" arg2 1 arg3 "$E$37"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$38" arg2 3 arg3 "$E$38"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$39" arg2 2 arg3 "$E$39"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$40:$C$41" arg2 3 arg3 "$E$40:$E$41"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$42" arg2 1 arg3 "$E$42"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$43:$C$45" arg2 3 arg3 "$E$43:$E$45"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$46" arg2 1 arg3 "$E$46"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$47" arg2 3 arg3 "$E$47"
 run VB Macro "Solver.xlam!SolverOptions" arg6 0 arg13 true
 set solveStatus to run VB Macro "Solver.xlam!SolverSolve" arg1 true
 run VB Macro "Solver.xlam!SolverFinish" arg1 1
 save active workbook
 return {solveStatus, value of range "C21:H30" of active sheet, value of range "D33" of active sheet, value of range "C37:F47" of active sheet}
end tell
