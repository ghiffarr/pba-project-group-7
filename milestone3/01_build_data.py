from pathlib import Path
import pandas as pd, numpy as np, json, hashlib
ROOT=Path(__file__).resolve().parent
RAW=ROOT/'raw'; OUT=ROOT/'data'; OUT.mkdir(exist_ok=True)
LEAGUES={'GB1':'Premier League','ES1':'La Liga','IT1':'Serie A','L1':'Bundesliga','FR1':'Ligue 1'}
def build():
 p=pd.read_csv(RAW/'players.csv.gz',low_memory=False)
 g=pd.read_csv(RAW/'games.csv.gz')
 a=pd.read_csv(RAW/'appearances.csv.gz')
 v=pd.read_csv(RAW/'player_valuations.csv.gz')
 assert not g.game_id.duplicated().any()
 assert not p.player_id.duplicated().any()
 assert not a.appearance_id.duplicated().any()
 g=g[g.competition_id.isin(LEAGUES)&g.season.between(2015,2024)]
 a=a.drop(columns=['competition_id']).merge(g[['game_id','competition_id','season']],on='game_id',validate='many_to_one')
 s=a.groupby(['player_id','season','competition_id'],as_index=False).agg(minutes=('minutes_played','sum'),goals=('goals','sum'),assists=('assists','sum'))
 s=s.sort_values(['player_id','season','minutes','competition_id'],ascending=[True,True,False,True]).drop_duplicates(['player_id','season'])
 counts={'dominant_league_player_seasons':len(s)}
 s=s[s.minutes>=900];counts['at_least_900_minutes']=len(s)
 v['date']=pd.to_datetime(v.date);v['season']=v.date.dt.year-1
 v=v[v.date.dt.month.between(1,7)&v.season.between(2015,2024)]
 assert not v.duplicated(['player_id','date']).any()
 v=v.sort_values('date').drop_duplicates(['player_id','season'],keep='last').rename(columns={'date':'valuation_date','market_value_in_eur':'market_value_eur'})
 s=s.merge(v[['player_id','season','valuation_date','market_value_eur']],on=['player_id','season'],how='left',validate='one_to_one')
 counts['missing_or_nonpositive_valuation']=int((s.market_value_eur.isna()|(s.market_value_eur<=0)).sum())
 s=s[s.market_value_eur.gt(0)].merge(p[['player_id','name','date_of_birth','position']],on='player_id',how='left',validate='many_to_one')
 dob=pd.to_datetime(s.date_of_birth)
 ref=pd.to_datetime((s.season+1).astype(str)+'-01-01')
 s['age']=ref.dt.year-dob.dt.year-((dob.dt.month>1)|((dob.dt.month==1)&(dob.dt.day>1))).astype(int)
 s.loc[~s.position.isin(['Attack','Defender','Midfield','Goalkeeper']),'position']=np.nan
 counts['missing_demographics']=int(s[['age','position']].isna().any(axis=1).sum())
 s=s.dropna(subset=['age','position'])
 s['league']=s.competition_id.map(LEAGUES);s['premier_league']=s.competition_id.eq('GB1').astype(int)
 s['log_value']=np.log(s.market_value_eur)
 s['goals_per90']=90*s.goals/s.minutes;s['assists_per90']=90*s.assists/s.minutes
 s=s.sort_values(['season','league','player_id'])
 assert not s.duplicated(['player_id','season']).any()
 assert s.minutes.ge(900).all() and s.market_value_eur.gt(0).all()
 s.to_csv(OUT/'player_seasons.csv',index=False)
 counts.update(final=len(s),players=s.player_id.nunique())
 summary=s.groupby('league').agg(n=('player_id','size'),median=('market_value_eur','median'),q1=('market_value_eur',lambda x:x.quantile(.25)),q3=('market_value_eur',lambda x:x.quantile(.75)),p10=('market_value_eur',lambda x:x.quantile(.1)),p90=('market_value_eur',lambda x:x.quantile(.9)))
 summary.to_csv(OUT/'league_summary.csv')
 pos=s.groupby(['position','premier_league']).market_value_eur.agg(['median','size']).reset_index()
 pos.to_csv(OUT/'position_summary.csv',index=False)
 (OUT/'audit.json').write_text(json.dumps(counts,indent=2))
 print(json.dumps(counts));print(summary.to_string());print(pos.to_string(index=False))
if __name__=='__main__':build()
