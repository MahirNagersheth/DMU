from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT=Path('/Users/mahir/Downloads/DMU')
P=ROOT/'_support/w5'
d=Document()
sec=d.sections[0]
sec.page_width=Inches(8.5); sec.page_height=Inches(11)
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Inches(1)
sec.header_distance=sec.footer_distance=Inches(.492)
for name,size,color,before,after in [('Normal',11,'202B33',0,6),('Title',24,'24465B',0,8),('Subtitle',11,'555555',0,8),('Heading 1',16,'2E74B5',18,10),('Heading 2',13,'2E74B5',14,7),('Heading 3',12,'1F4D78',10,5),('Caption',9,'555555',3,6)]:
 s=d.styles[name]; s.font.name='Calibri'; s.font.size=Pt(size); s.font.color.rgb=RGBColor.from_string(color)
 s.paragraph_format.space_before=Pt(before); s.paragraph_format.space_after=Pt(after); s.paragraph_format.line_spacing=1.25
for name in ['Heading 1','Heading 2','Heading 3']: d.styles[name].font.bold=True
# Named overrides: compact equations, compact table cells and top-of-page headings.
for name,size,after in [('Equation',11,5),('Table Text',10,0),('Screenshot Caption',8,3)]:
 s=d.styles.add_style(name,1); s.base_style=d.styles['Normal']; s.font.size=Pt(size)
 s.paragraph_format.space_after=Pt(after); s.paragraph_format.line_spacing=1.0
 s.paragraph_format.space_before=Pt(0)
h=sec.header.paragraphs[0]; h.text='95-760  |  Decision Making Under Uncertainty'; h.style='Caption'
f=sec.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
f.add_run('Recitation W5  |  ')
field=OxmlElement('w:fldSimple'); field.set(qn('w:instr'),'PAGE'); f._p.append(field)
for run in f.runs: run.font.size=Pt(9); run.font.color.rgb=RGBColor.from_string('555555')

def para(text='',style=None):
 assert '\u2014' not in text
 return d.add_paragraph(text,style)
def heading(text):
 p=d.add_paragraph(text,'Heading 1'); p.paragraph_format.space_before=Pt(0); return p
def eq(text): return para(text,'Equation')
def table(headers,rows,widths):
 t=d.add_table(rows=1,cols=len(headers)); t.autofit=False
 t.style='Table Grid'
 pr=t._tbl.tblPr
 tw=pr.find(qn('w:tblW')); tw.set(qn('w:type'),'dxa'); tw.set(qn('w:w'),'9360')
 ind=OxmlElement('w:tblInd'); ind.set(qn('w:w'),'120'); ind.set(qn('w:type'),'dxa'); pr.append(ind)
 margins=OxmlElement('w:tblCellMar')
 for k,v in [('top',65),('bottom',65),('start',120),('end',120)]:
  el=OxmlElement('w:'+k); el.set(qn('w:w'),str(v)); el.set(qn('w:type'),'dxa'); margins.append(el)
 pr.append(margins)
 for gc,width in zip(t._tbl.tblGrid.gridCol_lst,widths): gc.set(qn('w:w'),str(width))
 for values in [headers]+rows:
  cells=t.rows[0].cells if values is headers else t.add_row().cells
  for c,v,width in zip(cells,values,widths):
   c.width=Inches(width/1440); c.text=str(v); c.paragraphs[0].style='Table Text'
   c._tc.get_or_add_tcPr().find(qn('w:tcW')).set(qn('w:w'),str(width))
   if values is headers:
    c.paragraphs[0].runs[0].bold=True
    sh=OxmlElement('w:shd'); sh.set(qn('w:fill'),'E8EEF5'); c._tc.get_or_add_tcPr().append(sh)
  trpr=cells[0]._tc.getparent().get_or_add_trPr(); trpr.append(OxmlElement('w:cantSplit'))
 return t
def picture(name,width):
 p=d.add_paragraph(); p.paragraph_format.space_after=Pt(3); p.paragraph_format.line_spacing=1
 p.add_run().add_picture(str(P/name),width=Inches(width)); return p
def page(): d.add_page_break()

para('Recitation W5','Title')
para('Problem 1: Community garden planning','Subtitle')
heading('(a) Integer programming formulation')
para('Let F be the 10 foods below, H = {basil, cilantro, parsley}, and V = F \\ H (all fruits and vegetables, using the categories in the assignment).')
para('For each food i, let xᵢ = 1 if it is planted and 0 otherwise. Let yᵢ be the number of plants. Thus xᵢ ∈ {0, 1} and yᵢ ∈ ℤ≥₀.')
para('Parameters: sᵢ is square feet per plant, mᵢ is the minimum quantity if selected, and eᵢ is expected harvest in pounds per plant. Following the faculty model, use M = 100 in the selection linking constraints.')
table(['Food','Category','sᵢ','mᵢ','eᵢ','M'],[
 ['Tomato','Vegetable',4,4,10,100],['Bell pepper','Vegetable',2,6,5,100],['Carrot','Vegetable',.5,20,.25,100],['Lettuce','Vegetable',1,10,1.5,100],['Strawberry','Fruit',1,12,1,100],['Cucumber','Fruit',4,3,8,100],['Zucchini','Vegetable',9,2,12,100],['Basil','Herb',1,4,1,100],['Cilantro','Herb',.5,6,.5,100],['Parsley','Herb',.5,4,.6,100]], [2400,2000,1240,1240,1240,1240])
d.add_paragraph('Objective','Heading 2')
eq('Maximize Z = ∑ᵢ∈F eᵢyᵢ')
para('Equivalently, maximize 10y_T + 5y_B + 0.25y_Ca + 1.5y_L + y_S + 8y_Cu + 12y_Z + y_Ba + 0.5y_Ci + 0.6y_P. Subscripts follow the food names in the table.')
para('The faculty solution is the primary reference for the formulation. Tomatoes are optional. If tomatoes are selected, at least two herb types must also be selected; no separate constraint forces tomatoes to be planted.')

page(); heading('(a) Constraints')
for title,formula,explanation in [
 ('Space','∑ᵢ∈F sᵢyᵢ ≤ 100','Total planting area cannot exceed 100 square feet.'),
 ('Selection and minimum quantities','mᵢxᵢ ≤ yᵢ ≤ 100xᵢ     for every i ∈ F','Unselected foods have zero plants. Selected foods meet their minimum quantities.'),
 ('Variety','∑ᵢ∈F xᵢ ≥ 4','Plant at least four different types of food.'),
 ('Herbs require another category','3∑ᵢ∈V xᵢ − ∑ₕ∈H xₕ ≥ 0','Whenever an herb is selected, at least one fruit or vegetable is selected.'),
 ('Tomatoes and companion herbs','x_Ba + x_Ci + x_P ≥ 2x_T','If tomatoes are selected, include at least two distinct herb types.'),
 ('At least two specified foods','x_T + x_B + x_Z ≥ 2','Choose at least two of tomato, bell pepper, and zucchini.'),
 ('Zucchini excludes tomatoes','x_T + x_Z ≤ 1','Zucchini and tomatoes cannot both be selected.'),
 ('Tomato threshold and lettuce','y_T ≤ 30 + 100x_L;     y_L ≥ 10x_L','If y_T > 30, the first inequality forces x_L = 1; the second then requires at least 10 lettuce plants.'),
 ('Variable domains','xᵢ ∈ {0, 1};     yᵢ ∈ ℤ≥₀     for every i ∈ F','Plant counts are nonnegative integers; selections are binary.')]:
 p=para(); p.paragraph_format.space_after=Pt(2); p.add_run(title+'. ').bold=True; p.add_run(explanation)
 eq(formula)
para('The tomato threshold is redundant for this garden: 4y_T ≤ 100 implies y_T ≤ 25. Consequently, more than 30 tomato plants is impossible. The threshold constraint is retained to explicitly represent the stated rule; the lettuce minimum also appears in the general linking constraints.')

page(); heading('(b) Excel Solver solution')
para('In the Harvest worksheet, maximize D33 by changing C21:D30. Set C21:C30 to binary and D21:D30 to integer. Use Simplex LP, retain nonnegativity, and set Integer Optimality (%) to 0. Apply the linking constraints and the LHS/RHS checks shown in the screenshots.')
para('Excel Solver returned: “Solver found a solution. All constraints and optimality conditions are satisfied.” An independent integer optimization check gives the same objective value. The table reports the faculty’s selected optimal plan.')
table(['Food','Plant? xᵢ','Plants yᵢ','Area (sq. ft.)','Harvest (lb.)'],[
 ['Tomato',1,4,16,40],['Bell pepper',1,39,78,195],['Cilantro',1,6,3,3],['Parsley',1,6,3,3.6],['Other six foods',0,0,0,0],['Total',4,55,100,241.6]], [2560,1300,1400,2050,2050])
picture('solver_results.png',3.8)
para('Figure 1. Actual Excel Solver completion dialog for the final model.','Screenshot Caption')
d.add_paragraph('(c) Recommendation to the gardening club','Heading 2')
para('Plant 4 tomatoes, 39 bell peppers, 6 cilantro, and 6 parsley. This plan uses all 100 square feet and produces an expected harvest of 241.6 pounds. It includes four food types, supplies the two herbs required by tomatoes, and selects two of the specified foods. Every selected food meets its minimum quantity. Zucchini is excluded, and the lettuce condition is not triggered.')
para('Alternative optima exist. Our rerun also found 20 tomatoes, 7 bell peppers, 6 cilantro, and 6 parsley, yielding the same 241.6 lb. The table and worksheet display the faculty’s plan.')

page(); heading('Spreadsheet evidence: parameters and solution')
para('Actual Excel screenshot showing all parameters, both decision-variable columns, the quantity bounds, and the maximized objective value. Space is measured in square feet; expected harvest is in pounds.')
picture('model_values.png',6.5)
para('Figure 2. Harvest worksheet, rows 1 through 33.','Caption')
d.add_paragraph('Key spreadsheet formulas','Heading 2')
para('G5:G14 contains M = 100, matching the faculty’s linking bound. For the tomato row, E21 = E5*C21 and F21 = G5*C21 give the selected minimum and maximum. G21 = D5*D21 calculates area; H21 = F5*D21 calculates harvest. Copy these formulas through row 30. D33 = SUM(H21:H30) is the objective.')
para('The template label “Minimize cost” was corrected to “Maximize expected harvest (lb)” to match the assignment.')

page(); heading('Spreadsheet evidence: constraints and Solver')
picture('constraints.png',6.5)
para('Figure 3. Every displayed constraint is satisfied. The rowwise quantity bounds appear in Figure 2.','Screenshot Caption')
p=d.add_paragraph(); p.paragraph_format.line_spacing=1; p.paragraph_format.space_after=Pt(3)
p.add_run().add_picture(str(P/'solver_settings.png'),width=Inches(3.25))
p.add_run('  ')
p.add_run().add_picture(str(P/'solver_options.png'),width=Inches(2.85))
para('Figure 4. Actual Solver Parameters and Options dialogs. Integer Optimality is 0%. Tomatoes are optional; the conditional companion-herb requirement is retained.','Screenshot Caption')
para('Primary reference: faculty Recitation W5 Sol.xlsx, Harvest worksheet. Additional sources: RS W5.pdf, Problem 1, and Recitation W5.xlsx.','Screenshot Caption')

for element in [d._element,d.styles.element]:
 for border in list(element.iter(qn('w:pBdr'))): border.getparent().remove(border)
out=ROOT/'Recitation_W5_Solved.docx'
d.save(out)
from zipfile import ZipFile
with ZipFile(out) as z:
 assert all('\u2014' not in z.read(n).decode('utf-8') for n in z.namelist() if n.endswith('.xml'))
print(out)
