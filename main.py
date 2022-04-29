# APP ID: 3Dcy6olE
# CLIENT ID: dj0yJmk9ZU16Q3V6MG9VSlk4JmQ9WVdrOU0wUmplVFp2YkVVbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTVm
# CLIENT SECRET: 8ac097e6930c68dfc0cecf8c51ed202de4c47b72
# SHARING CODE: czq2w7n
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa

oauth = OAuth2(None, None, from_file='credentials.json')
if not oauth.token_is_valid():
    oauth.refresh_access_token()

gm = yfa.Game(oauth, 'mlb')
print(gm.league_ids())
leagues = {100: '412.l.67355', 20: '412.l.89915', 101: '404.l.117086', 0: '404.l.123717'}
league = int(input('What League? '))
lg = gm.to_league(leagues[league])
stats = lg.stat_categories()
my_team = lg.to_team('412.l.89915.t.1')
test = lg.matchups(3)                                                         #0-7                          #0-1
test_matchups = test['fantasy_content']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['0']['team'][1]['team_stats']['stats']
categories = [x['display_name'] for x in stats]
categories.insert(0, 'H/AB')
categories.insert(len(categories)//2+1, 'IP')
    

                                                                     #0-6/7                        #0-1
# test['fantasy_content']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['1']['team'][0][2]['name']

def get_matchups(week):
    m = lg.matchups(week)   
    num_matchups = len(m['fantasy_content']['league'][1]['scoreboard']['0']['matchups'])-1
    teams_data = {}
    for i in range(num_matchups):
        for j in range(2):
            stats = []
            name = m['fantasy_content']['league'][1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams'][str(j)]['team'][0][2]['name']
            matchup = m['fantasy_content']['league'][1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams'][str(j)]['team'][1]['team_stats']['stats']
            for x in range(len(categories)):
                stat = matchup[x]['stat']['value']
                stats.append('{0:<4}: {1:<4}'.format(categories[x], stat))
            teams_data[name] = stats
    return teams_data

def compare_teams():
    data = get_matchups(3)
    names = [name for name in data.keys() if type(name) == str]
    for i in range(len(names)):
        print(f'{i}: {names[i]}')
    team1 = int(input('First Team: '))
    team2 = int(input('Second Team: '))
    team1_score = 0
    team2_score = 0
    ties = 0
    print('+{0}+'.format('-'*33))
    print('| {0:<14}{2:<4}{1:<14}|'.format(names[team1][0:13], names[team2][0:13], '|'))
    for i in range(len(data[names[team1]])):
        if 'IP' != data[names[team1]][i].strip()[0:2] and data[names[team1]][i].strip()[0:4] != 'H/AB':
            if float(data[names[team1]][i].split(':')[1].strip()) > float(data[names[team2]][i].split(':')[1].strip()):
                if data[names[team1]][i].strip()[0:4].strip() == 'WHIP' or data[names[team1]][i].strip()[0:4].strip() == 'ERA':
                    team2_score += 1
                else:
                    team1_score += 1
            elif float(data[names[team1]][i].split(':')[1].strip()) < float(data[names[team2]][i].split(':')[1].strip()):
                if data[names[team1]][i].strip()[0:4].strip() == 'WHIP' or data[names[team1]][i].strip()[0:4].strip() == 'ERA':
                    team1_score += 1
                else:
                    team2_score += 1
            else:
                ties += 1
        print('| {0:<14}{2:<4}{1:<14}|'.format(data[names[team1]][i], data[names[team2]][i], '|'))
    
    if team1_score > team2_score:
        winner = names[team1]
    elif team1_score < team2_score:
        winner = names[team2]
        temp = team1_score
        team1_score = team2_score
        team2_score = temp
    else:
        winner = 'Tie'
    score = f'({team1_score}-{team2_score}-{ties})'
    print('+{0}+'.format('-'*33))
    print('|{0:^33}|'.format(winner[0:25] + " " + score))
    print('+{0}+'.format('-'*33))


compare_teams()
