import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
A="Arial"; H=Font(name=A,bold=True,color="FFFFFF"); HF=PatternFill("solid",fgColor="15171A")
B=Font(name=A,bold=True); N=Font(name=A); IN=Font(name=A,color="0000FF"); Y=PatternFill("solid",fgColor="FFF4B8")
T=Font(name=A,bold=True,size=15); G=Font(name=A,color="666666",italic=True,size=9); thin=Side(style="thin",color="DDDDDD")
AED='"AED" #,##0.00;("AED" #,##0.00);-'
def setw(ws,w):
    for c,x in w.items(): ws.column_dimensions[c].width=x
def font_all(ws):
    for r in ws.iter_rows():
        for c in r:
            if c.value is not None and c.font.name!=A: c.font=Font(name=A,bold=c.font.bold,color=c.font.color,italic=c.font.italic,size=c.font.size)

# ---------- 1. UAE final settlement ----------
wb=Workbook(); ws=wb.active; ws.title="How to use"
lines=["UAE Final Settlement Workbook","by CalcSouq · calcsouq.com","",
"1. Go to the 'Inputs' sheet and replace the yellow cells (blue text) with your own figures. The values there are an example.",
"2. The 'Statement' sheet builds your settlement line by line: gratuity, unused leave, unpaid salary, notice, other amounts and deductions.",
"3. 'Leave log' lets you record leave taken during the year; its total feeds unpaid leave automatically if you choose.",
"4. Compare the Statement with the settlement sheet from your employer before you sign.","",
"Rules used (UAE Federal Decree-Law 33/2021, Article 51, private sector):",
"• Gratuity: 21 days' basic pay per year for the first 5 years, 30 days per year after that; nothing under 1 year of continuous service.",
"• Total gratuity is capped at 2 years' basic salary. Daily wage = monthly basic ÷ 30.",
"• Unpaid leave days are not counted as service. Unused leave is paid on basic salary.",
"• Final dues are due within 14 days of the contract ending.","",
"General information only, not legal advice. Free-zone and government contracts may follow different rules; check with MOHRE (mohre.gov.ae) or your free zone."]
for i,l in enumerate(lines,1):
    c=ws.cell(i,1,l); c.font=T if i==1 else (G if i==2 else (B if l.startswith("Rules") else N))
ws.column_dimensions["A"].width=120
for r in range(4,16): ws.cell(r,1).alignment=Alignment(wrap_text=True)

wi=wb.create_sheet("Inputs"); setw(wi,{"A":42,"B":20,"C":60})
wi["A1"]="Your details"; wi["A1"].font=T
wi["A2"]="Edit the yellow cells only. Example values are shown."; wi["A2"].font=G
inp=[("Employee name","Example: A. Kumar",None,"Text"),
("Basic monthly salary (AED)",8000,"#,##0.00","From your contract / MOHRE offer letter"),
("Total monthly salary (AED)",13000,"#,##0.00","Basic + housing + transport + other fixed allowances"),
("Joining date",dt.date(2021,3,1),"dd-mmm-yyyy",""),
("Last working day",dt.date(2026,11,20),"dd-mmm-yyyy",""),
("Unpaid leave days (whole service)",0,"0","Not counted as service"),
("Use Leave log total for unpaid leave? (Yes/No)","No",None,"Yes = take unpaid days from the Leave log sheet"),
("Unused annual leave days",18,"0",""),
("Unpaid salary days (final month)",20,"0","Days worked but not yet paid"),
("Notice days not served",0,"0",""),
("Who cut the notice short? (Employer/Employee)","Employer",None,"Employer: paid to you. Employee: deducted from you."),
("Other amounts owed to you (AED)",0,"#,##0.00","Bonus, air ticket, expense claims"),
("Deductions (AED)",0,"#,##0.00","Loans, advances")]
for i,(a,v,f,n) in enumerate(inp,4):
    wi.cell(i,1,a).font=N; c=wi.cell(i,2,v); c.font=IN; c.fill=Y
    if f: c.number_format=f
    wi.cell(i,3,n).font=G
dv=DataValidation(type="list",formula1='"Yes,No"'); wi.add_data_validation(dv); dv.add("B10")
dv2=DataValidation(type="list",formula1='"Employer,Employee"'); wi.add_data_validation(dv2); dv2.add("B14")

wl=wb.create_sheet("Leave log"); setw(wl,{"A":14,"B":14,"C":18,"D":10,"E":40})
for j,h in enumerate(["From","To","Type","Days","Note"],1):
    c=wl.cell(1,j,h); c.font=H; c.fill=HF
wl["A2"]=dt.date(2025,6,1); wl["B2"]=dt.date(2025,6,5); wl["C2"]="Unpaid"; wl["E2"]="Example row: replace or delete"
for r in range(2,102):
    for col in "ABCE": wl[f"{col}{r}"].font=IN
    wl[f"A{r}"].number_format=wl[f"B{r}"].number_format="dd-mmm-yyyy"
    wl[f"D{r}"]=f'=IF(OR(A{r}="",B{r}=""),"",B{r}-A{r}+1)'
dv3=DataValidation(type="list",formula1='"Annual,Unpaid,Sick,Other"'); wl.add_data_validation(dv3); dv3.add("C2:C101")
wl["G1"]="Unpaid days total"; wl["G1"].font=B; wl["H1"]='=SUMIFS(D2:D101,C2:C101,"Unpaid")'
wl["G2"]="Annual leave taken"; wl["G2"].font=B; wl["H2"]='=SUMIFS(D2:D101,C2:C101,"Annual")'
setw(wl,{"G":20,"H":10})

st=wb.create_sheet("Statement"); setw(st,{"A":44,"B":22,"C":56})
st["A1"]="Final settlement statement"; st["A1"].font=T
st["A2"]='="Employee: "&Inputs!B4'; st["A2"].font=G
rows=[("Unpaid days used","=IF(Inputs!B10=\"Yes\",'Leave log'!H1,Inputs!B9)","0","Working: from Inputs or Leave log"),
("Service counted (days)","=MAX(0,Inputs!B8-Inputs!B7+1-B4)","#,##0",""),
("Service counted (years)","=B5/365","0.00",""),
("Daily basic wage","=Inputs!B5/30",AED,"Basic ÷ 30"),
("Daily total wage","=Inputs!B6/30",AED,"Total ÷ 30"),
(None,None,None,None),
("Gratuity: first 5 years","=IF(B6<1,0,21*B7*MIN(B6,5))",AED,"21 days × daily basic × years (max 5)"),
("Gratuity: after 5 years","=IF(B6<1,0,30*B7*MAX(B6-5,0))",AED,"30 days × daily basic × years beyond 5"),
("Gratuity cap (24 × basic)","=24*Inputs!B5",AED,""),
("Gratuity","=MIN(B10+B11,B12)",AED,""),
("Unused leave","=Inputs!B11*B7",AED,"Leave days × daily basic"),
("Unpaid salary","=Inputs!B12*B8",AED,"Days × daily total wage"),
("Notice","=IF(Inputs!B14=\"Employee\",-1,1)*Inputs!B13*B8",AED,"+ paid to you, − deducted"),
("Other amounts owed","=Inputs!B15",AED,""),
("Deductions","=-Inputs!B16",AED,""),
(None,None,None,None),
("TOTAL FINAL SETTLEMENT","=SUM(B13:B18)",AED,"")]
for i,(a,f,fmt,n) in enumerate(rows,4):
    if a is None: continue
    st.cell(i,1,a).font=B if i in (13,20) else N
    c=st.cell(i,2,f); c.number_format=fmt; c.font=B if i in (13,20) else N
    st.cell(i,3,n).font=G
for c in ("A20","B20"): st[c].fill=PatternFill("solid",fgColor="F5C300"); st[c].font=Font(name=A,bold=True,size=13)
st["A22"]="Under 1 year of service: no gratuity. Estimate only; confirm with your employer or MOHRE."; st["A22"].font=G
st["A23"]="Free online version: calcsouq.com/uae-final-settlement-calculator"; st["A23"].font=G
wb.move_sheet("Statement",offset=-1)
for s in wb: font_all(s)
wb.save("CalcSouq-UAE-Final-Settlement-Workbook.xlsx")

# ---------- 2. Trading journal ----------
wb=Workbook(); ws=wb.active; ws.title="How to use"
lines=["Trading Journal & R-Multiple Tracker","by CalcSouq · calcsouq.com","",
"1. 'Settings': enter your starting balance and your usual risk per trade (yellow cells).",
"2. 'Journal': one row per closed trade. Fill the blue columns; grey columns calculate themselves.",
"   Risk = the amount you would have lost at your stop. P&L = the actual result in account currency.",
"3. 'Stats': win rate, average win and loss in R, expectancy, profit factor, largest drawdown and results by setup.",
"4. The first journal row is an example. Replace it with your own trade.","",
"R-multiple = P&L ÷ risk. A trade that made twice what you risked is +2R. Expectancy is the average R per trade:",
"if it stays above zero over a large sample, the method has an edge at your current execution.","",
"For record-keeping only. Not investment advice. Leveraged trading carries a high risk of loss."]
for i,l in enumerate(lines,1):
    c=ws.cell(i,1,l); c.font=T if i==1 else (G if i==2 else N)
ws.column_dimensions["A"].width=110
se=wb.create_sheet("Settings"); setw(se,{"A":34,"B":16,"C":44})
se["A1"]="Settings"; se["A1"].font=T
for i,(a,v,f,n) in enumerate([("Starting balance",10000,"#,##0.00","Account currency"),("Planned risk per trade",0.01,"0.0%","Fraction of balance, e.g. 1%"),("Account currency","USD",None,"Label only")],3):
    se.cell(i,1,a).font=N; c=se.cell(i,2,v); c.font=IN; c.fill=Y
    if f: c.number_format=f
    se.cell(i,3,n).font=G
se["A7"]="Setups (used for the dropdown and Stats)"; se["A7"].font=B
setups=["Breakout","Pullback","Range","News","Other"]
for i,s in enumerate(setups,8): c=se.cell(i,1,s); c.font=IN; c.fill=Y

j=wb.create_sheet("Journal")
hd=["#","Date","Instrument","Long/Short","Setup","Entry","Stop","Exit","Size","Risk","P&L","R","Result","Balance","Peak","Drawdown","Planned risk","Risk vs plan","Notes"]
wd=[5,12,12,11,12,11,11,11,9,11,11,8,9,13,13,10,12,11,36]
inputs={"B","C","D","E","F","G","H","I","J","K","S"}
for k,(h,w_) in enumerate(zip(hd,wd),1):
    c=j.cell(1,k,h); c.font=H; c.fill=HF; c.alignment=Alignment(horizontal="center",wrap_text=True)
    j.column_dimensions[c.column_letter].width=w_
j.freeze_panes="C2"
ex=[dt.date(2026,11,3),"EURUSD","Long","Pullback",1.0850,1.0820,1.0910,0.33,99,198]
for k,v in enumerate(ex,2): j.cell(2,k,v)
j["S2"]="Example row: replace with your own trade"
NR=500; gray=PatternFill("solid",fgColor="F2F2F2")
for r in range(2,NR+2):
    j[f"A{r}"]=f'=IF(B{r}="","",ROW()-1)'
    j[f"L{r}"]=f'=IF(OR(J{r}="",K{r}="",J{r}=0),"",K{r}/J{r})'
    j[f"M{r}"]=f'=IF(K{r}="","",IF(K{r}>0,"Win",IF(K{r}<0,"Loss","Flat")))'
    prev="Settings!$B$3" if r==2 else f"N{r-1}"
    j[f"N{r}"]=f'=IF(K{r}="",{prev},{prev}+K{r})'
    pk="Settings!$B$3" if r==2 else f"O{r-1}"
    j[f"O{r}"]=f'=MAX({pk},N{r})'
    j[f"P{r}"]=f'=IF(O{r}=0,0,N{r}/O{r}-1)'
    j[f"Q{r}"]=f'=IF(K{r}="","",{prev}*Settings!$B$4)'
    j[f"R{r}"]=f'=IF(OR(J{r}="",Q{r}="",Q{r}=0),"",J{r}/Q{r})'
    j[f"B{r}"].number_format="dd-mmm-yy"
    for col in "FGH": j[f"{col}{r}"].number_format="0.00000"
    for col in "JKNOQ": j[f"{col}{r}"].number_format="#,##0.00;(#,##0.00);-"
    j[f"L{r}"].number_format='0.00"R";-0.00"R"'; j[f"P{r}"].number_format="0.0%;-0.0%;-"; j[f"R{r}"].number_format="0.00x"
    for col in "ABCDEFGHIJKLMNOPQRS":
        c=j[f"{col}{r}"]; c.font=IN if col in inputs else N
        if col not in inputs: c.fill=gray
dv=DataValidation(type="list",formula1='"Long,Short"'); j.add_data_validation(dv); dv.add(f"D2:D{NR+1}")
dv2=DataValidation(type="list",formula1="=Settings!$A$8:$A$12"); j.add_data_validation(dv2); dv2.add(f"E2:E{NR+1}")
j.conditional_formatting.add(f"K2:K{NR+1}",CellIsRule(operator="greaterThan",formula=["0"],font=Font(name=A,color="0A7D32")))
j.conditional_formatting.add(f"K2:K{NR+1}",CellIsRule(operator="lessThan",formula=["0"],font=Font(name=A,color="C0392B")))

s=wb.create_sheet("Stats"); setw(s,{"A":32,"B":16,"C":4,"D":14,"E":10,"F":12,"G":12,"H":14})
s["A1"]="Performance"; s["A1"].font=T
R=f"Journal!$K$2:$K${NR+1}"; L=f"Journal!$L$2:$L${NR+1}"; M=f"Journal!$M$2:$M${NR+1}"
st=[("Closed trades",f'=COUNT({R})',"0"),
("Wins",f'=COUNTIF({M},"Win")',"0"),("Losses",f'=COUNTIF({M},"Loss")',"0"),
("Win rate","=IF(B3=0,0,B4/B3)","0.0%"),
("Net P&L",f"=SUM({R})","#,##0.00;(#,##0.00);-"),
("Average win (R)",f'=IFERROR(AVERAGEIF({L},">0"),0)','0.00"R"'),
("Average loss (R)",f'=IFERROR(AVERAGEIF({L},"<0"),0)','0.00"R";-0.00"R"'),
("Expectancy per trade (R)",f"=IFERROR(AVERAGE({L}),0)",'0.00"R";-0.00"R"'),
("Profit factor",f'=IFERROR(SUMIF({R},">0")/-SUMIF({R},"<0"),0)',"0.00"),
("Largest drawdown",f"=MIN(Journal!$P$2:$P${NR+1})","0.0%;-0.0%;-"),
("Current balance",f"=Settings!B3+B7","#,##0.00"),
("Return on starting balance","=IF(Settings!B3=0,0,B7/Settings!B3)","0.0%;-0.0%;-")]
for i,(a,f,fmt) in enumerate(st,3):
    s.cell(i,1,a).font=N; c=s.cell(i,2,f); c.number_format=fmt; c.font=B
s["D2"]="By setup"; s["D2"].font=B
for k,h in enumerate(["Setup","Trades","Win rate","Net P&L","Avg R"],4):
    c=s.cell(3,k,h); c.font=H; c.fill=HF
E=f"Journal!$E$2:$E${NR+1}"
for i in range(5):
    r=4+i
    s[f"D{r}"]=f"=Settings!A{8+i}"
    s[f"E{r}"]=f'=COUNTIFS({E},D{r},{R},"<>")'
    s[f"F{r}"]=f'=IF(E{r}=0,0,COUNTIFS({E},D{r},{M},"Win")/E{r})'; s[f"F{r}"].number_format="0.0%"
    s[f"G{r}"]=f'=SUMIFS({R},{E},D{r})'; s[f"G{r}"].number_format="#,##0.00;(#,##0.00);-"
    s[f"H{r}"]=f'=IFERROR(AVERAGEIFS({L},{E},D{r}),0)'; s[f"H{r}"].number_format='0.00"R";-0.00"R"'
s["A17"]="Free position-size and strategy simulator: calcsouq.com/trading-strategy-simulator"; s["A17"].font=G
wb.move_sheet("Stats",offset=-2)
for x in wb: font_all(x)
wb.save("CalcSouq-Trading-Journal.xlsx")
