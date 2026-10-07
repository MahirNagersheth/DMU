from pathlib import Path
import json
p=Path(__file__).parent
(p/'captures').mkdir(exist_ok=True)
groups={
 'sampling':[('sampling_prob','range','B2:E7'),('sampling','range','G2:L17')],
 'fish':[('fish_prob','range','B2:E10'),('fish_summary','range','X4:Y9'),('fish_first','range','G3:O38'),('fish_last','range','G39:O73')],
 'n':[('n_rows','range','G3:T15'),('n_last','range','P494:T503'),('n_summary','range','V36:W40'),('n_chart','chart',1)],
 'q':[('q_inputs','range','Q3:R14'),('q_table','range','T3:U44'),('q_chart','chart',1)],
 'air_a':[('air_rows','range','B3:K16'),('air_summary','range','R2:S13')],
 'air_b':[('air_cumulative','range','L3:P15'),('air_last','range','L5094:P5103'),('air_n_chart','chart',1)],
 'air_c':[('air_limits','range','R2:S19'),('air_chart','chart',1)],
 'food':[('food_params','range','B4:F24'),('food_costs','range','H4:K10'),('food_decisions','range','C28:F32'),('food_constraints','range','C36:F53'),('food_objective','range','C55:G60')]
}
names={'sampling':'Sampling','fish':'Fishery operations','n':'N analysis','q':'Analysis on Q','air_a':'Airline (a)','air_b':'Airline (b)','air_c':'Airline (c)','food':'Food bank'}
manifest={}
for group,items in groups.items():
 lines=['tell application "Microsoft Excel"',f'activate object worksheet "{names[group]}" of workbook "Recitation W6 Completed.xlsx"','set zoom of active window to 100']
 for name,kind,obj in items:
  target=f'range "{obj}" of active sheet' if kind=='range' else f'chart of chart object {obj} of active sheet'
  dest=p/'captures'/(name+'.png')
  lines += [f'copy picture {target}','end tell', 'do shell script '+json.dumps(f'/usr/bin/swift -module-cache-path /tmp/w6-swift-cache "{p}/clipboard_image.swift" "{dest}"'), 'tell application "Microsoft Excel"']
  manifest[name]={'sheet':names[group],'kind':kind,'range':obj,'path':str(dest)}
 lines+=['end tell']
 (p/('capture_'+group+'.applescript')).write_text('\n'.join(lines))
(p/'captures'/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Capture scripts generated')
