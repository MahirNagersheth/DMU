tell application "Microsoft Excel"
 activate
 open POSIX file "/Users/mahir/Downloads/DMU/_support/w5/Recitation_W5_Solved.xlsx"
 set value of range "G4" of active sheet to "Link bound M"
 set value of range "G5:G14" of active sheet to 100
 clear contents range "B37:F47" of active sheet
 set value of range "B37:B43" of active sheet to {{"Planting space"}, {"Different food types"}, {"Herbs need fruit / vegetable"}, {"Tomato companion herbs"}, {"At least two named foods"}, {"Tomato / zucchini exclusion"}, {"Over 30 tomatoes needs lettuce"}}
 set formula of range "C37:C43" of active sheet to {{"=SUM(G21:G30)"}, {"=SUM(C21:C30)"}, {"=3*SUM(C21:C27)-SUM(C28:C30)"}, {"=SUM(C28:C30)-2*C21"}, {"=C21+C22+C27"}, {"=C21+C27"}, {"=D21-$C$16*C24"}}
 set value of range "D37:D43" of active sheet to {{"<="},{">="},{">="},{">="},{">="},{"<="},{"<="}}
 set formula of range "E37:E43" of active sheet to {{"=$C$16"},{"=4"},{"=0"},{"=0"},{"=2"},{"=1"},{"=30"}}
 set formula of range "F37:F43" of active sheet to {{"=E37-C37"},{"=C38-E38"},{"=C39-E39"},{"=C40-E40"},{"=C41-E41"},{"=E42-C42"},{"=E43-C43"}}
 clear contents range "B49:H52" of active sheet
 set value of range "B45" of active sheet to "Solver: Max D33; change C21:D30; Simplex LP; integer optimality 0%."
 set value of range "B46" of active sheet to "Linking: D21:D30 >= E21:E30 and D21:D30 <= F21:F30."
 set value of range "B47" of active sheet to "C21:C30 binary; D21:D30 nonnegative integers; M = 100."
 set value of range "B48" of active sheet to "Faculty model: tomatoes optional; at least two herbs if tomatoes selected."
 run VB Macro "Solver.xlam!SolverReset"
 run VB Macro "Solver.xlam!SolverOk" arg1 "$D$33" arg2 1 arg3 0 arg4 "$C$21:$D$30" arg5 2
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$21:$C$30" arg2 5
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$D$21:$D$30" arg2 4
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$D$21:$D$30" arg2 3 arg3 "$E$21:$E$30"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$D$21:$D$30" arg2 1 arg3 "$F$21:$F$30"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$37" arg2 1 arg3 "$E$37"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$38:$C$41" arg2 3 arg3 "$E$38:$E$41"
 run VB Macro "Solver.xlam!SolverAdd" arg1 "$C$42:$C$43" arg2 1 arg3 "$E$42:$E$43"
 run VB Macro "Solver.xlam!SolverOptions" arg4 true arg6 1 arg9 0 arg12 true
 set value of range "D22" of active sheet to 38
 set resultCode to run VB Macro "Solver.xlam!SolverSolve" arg1 true
 save active workbook
 set scroll row of active window to 1
 set zoom of active window to 80
 select range "A1" of active sheet
 return {resultCode,value of range "D33" of active sheet,value of range "C21:D30" of active sheet}
end tell
