from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
import matplotlib.pyplot as plt
import matplotlib
from labellines import labelLines
import warnings
import math
warnings.filterwarnings("ignore")

'''
DOCUMENTATION:
TODO -> to implement later
REWORK -> to fix later
'''

# TODO make this inputtable
superstars = [
    "Stephen Curry", 
    # "Joel Embiid", 
    "Kevin Durant",
    "Luka Doncic",
    "Shai Gilgeous-Alexander",
    # "Anthony Edwards", 
    # "Donovan Mitchell",
    "Giannis Antetokounmpo",
    # "Devin Booker",
    # "De'Aaron Fox",
    "Nikola Jokic",

    # "Trae Young", 
    # "Jalen Brunson", 
    "Jayson Tatum",
    "LeBron James",
    # "Tyrese Maxey",
    "Damian Lillard",
    # 'Tyrese Haliburton',
    'James Harden',
    # 'Klay Thompson',
    # 'Paul George',
    # "Shaquille O'Neal",
    # "David Robinson",
    # "Hakeem Olajuwon",
    # "Tim Duncan", 
    # "Wilt Chamberlain",
    # "Patrick Ewing",
]

old = [
    "Shaquille O'Neal",
    "David Robinson",
    "Hakeem Olajuwon",
    "Tim Duncan", 
    "Wilt Chamberlain",
    "Patrick Ewing",
]

# if there are to be any players whch arent annotated
# then to_annotate will differ from superstars
to_annotate = superstars 


# all the data we will store
pg_options= {'ppg': [], 'rpg': [], 'apg': [], \
    'fgapg': [], 'fgmpg': [], 'fgpt': [], 'fg3apg':[], 'fg3mpg':[], \
    'fg3pt': [], 'ftapg': [], 'ftmpg': [], 'spg': [], 'bpg': [], 'tpg': [], 'fpg': [], 'mpg': []}







def plotter(superstars, pg_options, x, y, z, m):

    # get the ids for each player
    player_ids = []
    for i in superstars:
        player_ids.append(players.find_players_by_full_name(i)[0]['id'])

    # # initialise the size of the figure
    aspect_ratio = (19,9)
    scale = 0.8
    plt.figure(figsize=(aspect_ratio[0]*scale, aspect_ratio[1]*scale))

    plt.xlabel(x)
    plt.ylabel(y)


    points = False
    # defining axis of the line
    line='#'
    if x not in pg_options:
        line='x'
    elif y not in pg_options:
        line='y'

    # determining the season or max for which stat
    zdir = -1
    if y in pg_options.keys() and x in pg_options.keys():
        # z = int(input('which season?(2023, 1999, -1 for max): '))
        if z == -1:
            # m = input('max for which stat?(from above chosen stat): ')
            if m == x:
                # find max over x, use that index as Z
                zdir = 0
            elif m == y:
                # find max over y, use that index as Z
                zdir = 1
            else:
                print('ERROR ERROR ERROR')
        points=True

    toDoSeasons = False
    if 'seasons' in [x,y]:
        toDoSeasons = True

    years = False
    if 'years' in [x, y]:

        years = True
        
        
    pointsX = []
    pointsY = []
    # storing the max seasons played for x axis scale
    mx_seasons = 0
    earliest_yr = 2025
    latest_yr = 1944

    # beginning to plot
    for f in range(len(player_ids)):

        # obtain all data and rework in a readable dict
        player_id = player_ids[f]
        career = playercareerstats.PlayerCareerStats(player_id=f'{player_id}') 
        c = career.get_dict()
        headers = c['resultSets'][0]['headers'] # contains header
        values = c['resultSets'][0]['rowSet'] # contains values
        data = {headers[i]: [values[j][i] for j in range(len(values))] for i in range(len(headers))}

        # segregate necessary data and calculat per game stats
        sIds = data['SEASON_ID']
        seasons = [int(s[0:2] + s[-2:]) for s in sIds]

        gp = data['GP']
        pts = data['PTS']
        ppg = [pts[i]/gp[i] for i in range(len(gp))]

        fta = data['FTA']
        ftapg = [fta[i]/gp[i] for i in range(len(gp))]

        rpg = [data['REB'][i]/gp[i] for i in range(len(gp))]
        apg = [data['AST'][i]/gp[i] for i in range(len(gp))]

        fgapg = [data['FGA'][i]/gp[i] for i in range(len(gp))]
        fgmpg = [data['FGM'][i]/gp[i] for i in range(len(gp))]
        fgpt = [fgmpg[i]/fgapg[i] for i in range(len(gp))]
        fg3apg = [data['FG3A'][i]/gp[i] for i in range(len(gp))]
        fg3mpg = [data['FG3M'][i]/gp[i] for i in range(len(gp))]
        fg3pt = [fg3mpg[i]/fg3apg[i] for i in range(len(gp))]
        ftmpg = [data['FTM'][i]/gp[i] for i in range(len(gp))]

        spg = [data['STL'][i]/gp[i] for i in range(len(gp))]
        bpg = [data['BLK'][i]/gp[i] for i in range(len(gp))]
        tpg = [data['TOV'][i]/gp[i] for i in range(len(gp))]
        fpg = [data['PF'][i]/gp[i] for i in range(len(gp))]
        mpg = [data['MIN'][i]/gp[i] for i in range(len(gp))]

        # updating max seasons played
        if len(gp) > mx_seasons:
            mx_seasons = len(gp)

        if seasons[0] < earliest_yr:
            earliest_yr = seasons[0]
        if seasons[-1] > latest_yr:
            latest_yr = seasons[-1]

        # defining the options for each axis
        pg_options= {'ppg': ppg, 'rpg': rpg, 'apg': apg, \
        'fgapg': fgapg, 'fgmpg': fgmpg, 'fgpt': fgpt, 'fg3apg':fg3apg, 'fg3mpg':fg3mpg, \
        'fg3pt': fg3pt, 'ftapg': ftapg, 'ftmpg': ftmpg, 'spg': spg, 'bpg': bpg, 'tpg': tpg, 'fpg': fpg, 'mpg': mpg,
        }


        
        # we need to remove the interim seasons if the player got traded
        i = 0
        while i < len(seasons):
            season = seasons[i]
            flag = 0
            while seasons.count(season) > 1:
                flag = 1
                for key in pg_options:
                    pg_options[key].pop(i)
                seasons.pop(i)
            if flag == 0:
                i += 1


        # if per player, a point is to be plotted
        # that is, when both x axis and y axis have a stat
        if points:
            X = pg_options[x]
            Y = pg_options[y]
            if z == -1:
                # here we are doing the MAX from one stat
                # the year where so and so averaged the MOST of this stat
                if zdir == 0:
                    yr = X.index(max(X))

                else:
                    yr = Y.index(max(Y)) 
            else:
                # here we are doing a specific year (like 2016)
                try:
                    yr = seasons.index(z)
                except:
                    print(f'no data for {superstars[f]} for year {z}')
                    continue

            # get the data for that year

            Y = Y[yr]
            X = X[yr]

            pointsX.append(X)
            pointsY.append(Y)

            # plot the point, with an annotation of their name
            # TODO: make the text look better
            plt.plot(X, Y, 'bo', label=f'{superstars[f]}')
            plt.annotate(superstars[f], (X, Y), ha="center")

        if toDoSeasons:

            # here we're doing lines.
            # whichever axis has seasons thats where the range will go
            if line == 'y':
                plt.plot(pg_options[x], [i for i in range(len(ppg))], label=f'{superstars[f]}')
            if line == 'x':
                plt.plot([i for i in range(len(ppg))], pg_options[y], label=f'{superstars[f]}')
        
        if years:
            if line == 'y':
                plt.plot(pg_options[x], seasons, label=f'{superstars[f]}')
            if line == 'x':
                plt.plot(seasons, pg_options[y], label=f'{superstars[f]}')


    if not points:
        # if we're making a line, then we want to label the lines
        # we also want to label the lines
        if toDoSeasons:
            plt.xticks(range(mx_seasons + math.floor(mx_seasons*0.2)))
            plt.legend(loc='lower right')

        else:
            print(earliest_yr, latest_yr)
            plt.xticks(range(earliest_yr-math.floor((latest_yr-earliest_yr)*0.3), latest_yr))
            plt.legend(loc='lower left')
        labelLines(plt.gca().get_lines(), zorder=2.5)
        
    average = False

    if average:
        plt.plot(sum(pointsX)/len(pointsX), sum(pointsY)/len(pointsY), 'ro')
        plt.annotate('AVERAGE', (sum(pointsX)/len(pointsX), sum(pointsY)/len(pointsY)), ha="center")
    plt.title(f'{x} vs {y}')
    plt.savefig(f'{name}.png')
    plt.show()



if __name__ == '__main__':

    # get the inputs
    name = input("name the graph: ")
    print(f'counting stats options: {pg_options.keys()}')
    print(f'time options: seasons, or above stats')
    x = input('choose for X axis: ')
    y = input('choose for Y axis: ')

    z = 2023
    m = 0
    plotter(superstars, pg_options, x, y, z, m)