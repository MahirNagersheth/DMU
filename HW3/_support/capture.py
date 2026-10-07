import subprocess,time
from pathlib import Path
P=Path(__file__).parent; O=P.parent/'Screenshots';O.mkdir(exist_ok=True)
def osa(s):
 r=subprocess.run(['osascript','-e',s],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr)
 return r.stdout.strip()
def capture_window(name,out):
 x=osa(f'tell application "System Events" to tell process "Microsoft Excel" to get {{position,size}} of window "{name}"')
 nums=[int(v.strip()) for v in x.split(',')]
 subprocess.run(['screencapture','-x','-R'+','.join(map(str,nums)),str(O/out)],check=True)
def ui(s):return osa('tell application "System Events" to tell process "Microsoft Excel"\n'+s+'\nend tell')
osa('''tell application "Microsoft Excel"
activate
activate object worksheet "Problem 1"
set value of range "A50" to "Simplex LP; integer optimality 0%; ignore integer constraints OFF. Saved model: M48:M55."
set value of range "A73" to "Simplex LP; nonnegative variables; integer optimality 0%; ignore integer constraints OFF. Saved model: M82:M89."
set number format of range "B38:C41" to "0"
set number format of range "B57:L60" to "#,##0"
set number format of range "H38:I41" to "#,##0"
set freeze panes of active window to false
save active workbook
end tell''')
ui('set position of window "HW3_Solved" to {20,30}\nset size of window "HW3_Solved" to {1400,840}')
models=[('P1_Construction','Problem 1','M20:M25',20,95),('P1_Production','Problem 1','M48:M55',36,85),('P1_Transport','Problem 1','M82:M89',55,75),('P2_Schedule','Problem 2','N5:N13',22,85)]
for key,sheet,model,start,zoom in models[-1:]:
 osa(f'''tell application "Microsoft Excel"
 activate object worksheet "{sheet}"
 set calculation to calculation automatic
 set freeze panes of active window to false
 set zoom of active window to {zoom}
 set scroll row of active window to {start}
 set scroll column of active window to 1
 select range "A{start}"
 run VB Macro "Solver.xlam!SolverLoad" arg1 "${model.replace(':',':$')}"
 end tell''')
 time.sleep(.3)
 capture_window('HW3_Solved',key+'_Sheet.png')
 ui('click menu item "Solver..." of menu "Tools" of menu bar item "Tools" of menu bar 1')
 time.sleep(.4)
 capture_window('Solver Parameters',key+'_Solver.png')
 ui('click button 8 of UI element 4 of window "Solver Parameters"')
 time.sleep(1)
 names=ui('get name of every window')
 if 'Solver Results' not in names:raise RuntimeError('Unexpected solver window: '+names)
 message=ui('get description of static text 1 of UI element 4 of window "Solver Results"')
 print(key,message,flush=True)
 capture_window('Solver Results',key+'_Result.png')
 ui('click button 3 of UI element 4 of window "Solver Results"')
 time.sleep(.2)
 osa('tell application "Microsoft Excel" to save active workbook')
 if key=='P2_Schedule':
  ui('click menu item "Solver..." of menu "Tools" of menu bar item "Tools" of menu bar 1')
  time.sleep(.3)
  ui('click button 6 of UI element 4 of window "Solver Parameters"')
  time.sleep(.3)
  capture_window('Options','Solver_Options.png')
  ui('click button 2 of UI element 4 of window "Options"')
  ui('click button 7 of UI element 4 of window "Solver Parameters"')
osa('''tell application "Microsoft Excel"
activate object worksheet "Problem 1"
set scroll row of active window to 1
set zoom of active window to 85
save active workbook
end tell''')
