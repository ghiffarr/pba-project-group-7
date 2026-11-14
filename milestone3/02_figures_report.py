from pathlib import Path
import pandas as pd, numpy as np, json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Line, Rect, String, Circle
from reportlab.graphics import renderPDF, renderSVG
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
d=pd.read_csv(ROOT/'data/player_seasons.csv')
s=pd.read_csv(ROOT/'data/league_summary.csv').set_index('league')
pos=pd.read_csv(ROOT/'data/position_summary.csv')
navy='#18334B';teal='#087F8C';gray='#8094A5'
def txt(x,y,text,size=9,color=navy,anchor='start'):
 return String(x,y,text,fontName='Helvetica',fontSize=size,fillColor=colors.HexColor(color),textAnchor=anchor)
def fig1():
 f=Drawing(495,240)
 x=lambda v:140+np.log10(v)*175
 for t in [1,2,5,10,20,50,100]:
  xx=x(t);f.add(Line(xx,38,xx,220,strokeColor=colors.HexColor('#E1E7EB')));f.add(txt(xx,23,str(t),anchor='middle'))
 for i,name in enumerate(['Premier League','Bundesliga','Serie A','La Liga','Ligue 1']):
  y=200-i*35;r=s.loc[name];co=teal if i==0 else gray
  f.add(txt(0,y+3,name,10));f.add(txt(0,y-10,'n = '+format(int(r['n']),','),8,'#566876'))
  f.add(Line(x(r.p10/1e6),y,x(r.p90/1e6),y,strokeColor=colors.HexColor(co),strokeWidth=1.4))
  for val in [r.p10,r.p90]:f.add(Line(x(val/1e6),y-5,x(val/1e6),y+5,strokeColor=colors.HexColor(co)))
  f.add(Rect(x(r.q1/1e6),y-9,x(r.q3/1e6)-x(r.q1/1e6),18,fillColor=colors.HexColor(co),strokeColor=None))
  f.add(Line(x(r['median']/1e6),y-9,x(r['median']/1e6),y+9,strokeColor=colors.white,strokeWidth=2))
  f.add(txt(493,y-3,format(r['median']/1e6,'g')+'m',9,anchor='end'))
 f.add(txt(313,3,'Market value (EUR millions; logarithmic axis)',9,anchor='middle'))
 return f
def fig2():
 f=Drawing(495,250);x=lambda v:100+v*17.5
 for t in range(0,21,5):
  f.add(Line(x(t),40,x(t),222,strokeColor=colors.HexColor('#E1E7EB')));f.add(txt(x(t),25,str(t),anchor='middle'))
 for i,p in enumerate(['Attack','Midfield','Defender','Goalkeeper']):
  y=201-i*43;f.add(txt(0,y-2,p,10))
  for pl,dy,co in [(1,3,teal),(0,-12,gray)]:
   r=pos[(pos.position==p)&(pos.premier_league==pl)].iloc[0];m=r['median']/1e6
   f.add(Rect(100,y+dy,x(m)-100,11,fillColor=colors.HexColor(co),strokeColor=None))
   f.add(txt(x(m)+5,y+dy+2,format(m,'g'),9))
 f.add(txt(275,5,'Median market value (EUR millions)',9,anchor='middle'))
 f.add(Rect(105,237,9,9,fillColor=colors.HexColor(teal),strokeColor=None));f.add(txt(120,238,'Premier League',9))
 f.add(Rect(245,237,9,9,fillColor=colors.HexColor(gray),strokeColor=None));f.add(txt(260,238,'Other four leagues pooled',9))
 return f
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8,textColor=colors.HexColor(navy)))
styles.add(ParagraphStyle(name='SmallNote',parent=styles['Body'],fontSize=8,leading=11,spaceAfter=7))
styles.add(ParagraphStyle(name='Heading',parent=styles['Body'],fontName='Helvetica-Bold',fontSize=14,leading=18,spaceBefore=10,spaceAfter=8))
styles.add(ParagraphStyle(name='BigTitle',parent=styles['Body'],fontName='Helvetica-Bold',fontSize=23,leading=28,spaceAfter=8))
story=[]
def p(t,style='Body'):story.append(Paragraph(t,styles[style]))
p('Milestone 3 | The Premier League Tax','BigTitle')
p('Group 7 - A first look at player market values','Heading')
p('Ghiffar 111006223 (leader) | Kelvin Claudio 112006266 | Kenzion Ciang 112006228<br/>Jevann Alden Lioe 112006438 | Ryosei Inagaki 112006263','SmallNote')
p('<b>Research question.</b> Do Premier League players have higher estimated market values than comparable players in La Liga, Serie A, the Bundesliga and Ligue 1, after accounting for age, position and on-pitch performance?')
p('<b>Verified sample.</b> '+format(len(d),',')+' player-seasons from '+format(d.player_id.nunique(),',')+' players, covering 2015/16-2024/25. Each observation represents one player in one season, assigned to their top-five league with the most minutes; at least 900 minutes in that league are required.')
p('Figure 1. Market-value distributions by league','Heading')
story.append(fig1())
p('Boxes show the 25th-75th percentiles; white lines mark medians; whiskers show the 10th-90th percentiles, not minima/maxima. Right labels give median values. All seasons are pooled; values are nominal euros. Source for both figures: dcaribou/transfermarkt-datasets, downloaded 13 November 2026; calculations from the rebuilt sample.','SmallNote')
p('<b>What stands out.</b> The Premier League median is EUR 15m, compared with EUR 6.5m in the Bundesliga, EUR 6m in Serie A, EUR 5m in La Liga and EUR 4.5m in Ligue 1. Its middle half spans EUR 7m-28m, versus EUR 2m-10m in Ligue 1. Nevertheless, the league distributions overlap substantially: high-valued players also appear outside England.')
p('<b>Why it matters.</b> The median gap is not driven solely by a handful of superstars. The wide upper ranges also motivate using log market value in the planned analysis. These are unadjusted differences; age, performance, position and season composition could still account for them.')
story.append(PageBreak())
p('Figure 2. Does the gap remain within positions?','Heading')
story.append(fig2())
p('Each bar is a player-season median within a broad position. The comparison pools all observations from the other four leagues, rather than averaging their league medians. Counts (Premier League / other leagues): Attack 826 / 3,007; Midfield 965 / 3,871; Defender 1,224 / 4,861; Goalkeeper 248 / 943.','SmallNote')
p('<b>What stands out.</b> Premier League medians are higher in all four positions: EUR 18m versus EUR 7m for attackers, EUR 16m versus EUR 6m for midfielders, EUR 12m versus EUR 4.5m for defenders, and EUR 10m versus EUR 4.5m for goalkeepers. The ratios range from about 2.2 to 2.7. Goalkeepers have the smallest samples, so their comparison deserves particular caution.')
p('<b>Why it matters.</b> The raw gap is visible within positions, so differences in the proportion of attackers versus defenders cannot by themselves explain the entire pattern. This motivates the planned regression of log value on Premier League participation, controlling for age, position, minutes, goals per 90, assists per 90 and season. No regression, significance test or causal claim is made here.')
p('Data preparation and interpretation','Heading')
p('<b>Reproducible rules.</b> League games are selected using GB1, ES1, IT1, L1 and FR1. Minutes, goals and assists are summed within player-season-league. Cross-league movers retain the league with the most minutes (ties use the competition code). Age is measured on 1 January of the season-ending year. The valuation is the latest recorded in January-July of that year; only positive values and valid ages/positions are retained. Of 16,037 player-seasons meeting the minutes rule, 82 lack a usable valuation and 10 lack valid age or position data.')
p('<b>Update to Milestone 2.</b> This report replaces the proposal\'s unverified counts and summaries with calculations from downloaded records. The source valuations stop on 12 June 2026; 2025/26 is excluded because its January-July valuation window is incomplete. The resulting sample covers ten seasons, not eleven.')
p('<b>Limits.</b> These are community/editor estimates, not actual transfer fees. The January-July window is a seasonal proxy, not a guaranteed post-season valuation; this matters especially for the delayed 2019/20 season. Broad positions come from player profiles and may not reflect historical roles. Repeated player-seasons are not independent; later inference should account for player clustering. Selection into England and unobserved ability prevent a causal interpretation. Goals and assists also measure defensive contributions poorly.')
p('<b>Sources and reproducibility.</b> <link href="https://github.com/dcaribou/transfermarkt-datasets" color="#087F8C">github.com/dcaribou/transfermarkt-datasets</link> (CC0 source collection): players, games, appearances and player_valuations. The companion ZIP contains the cleaned sample, codebook, download/build/plot scripts, audit counts and source checksums. AI assistance: ChatGPT helped prepare code, figures and this write-up.','SmallNote')
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#D9E2E8'));c.line(48,38,547,38)
 c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#566876'));c.drawString(48,25,'Group 7 | Descriptive visualization | 13 November 2026');c.drawRightString(547,25,str(doc.page))
doc=SimpleDocTemplate(str(OUT/'Group7_Milestone3.pdf'),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=35,bottomMargin=48)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
for name,f in [('figure1',fig1()),('figure2',fig2())]:
 renderPDF.drawToFile(f,str(OUT/(name+'.pdf')))
 renderSVG.drawToFile(f,str(OUT/(name+'.svg')))
print(OUT/'Group7_Milestone3.pdf')
