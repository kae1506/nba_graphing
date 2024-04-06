from p5 import *
from nba import plotter


xAxis = ''
yAxis = ''

f = None

class Button:
    def __init__(self, posn, text):
        self.posn = posn
        self.text = text
        self.size = 50
        self.c = False

    def render(self):
        text_pos = (i-self.size/3 for i in self.posn)

        push()
        stroke_weight(0)
        stroke(0)
        fill(255)
        ellipse_mode(CENTER)
        ellipse(self.posn, self.size,self.size)
        fill(0,0,0)
        
        text(self.text, text_pos)
        pop()

    def clicked(self):
        if dist((mouse_x, mouse_y), self.posn) < self.size and self.c is not True:
            self.c = True
            return f'{self.text}', True
        else: 
            return '', False



buttonsX = []
buttonsY = []


superstars = [
    "Stephen Curry", 
    # "Joel Embiid", 
     # "Kevin Durant",
    "Luka Doncic",
    "Shai Gilgeous-Alexander",
    # "Anthony Edwards", 
    # "Donovan Mitchell",
    # "Giannis Antetokounmpo",
    # "Devin Booker",
    # "De'Aaron Fox",
    "Nikola Jokic",

    "Trae Young", 
    # "Jalen Brunson", 
    # "Jayson Tatum",
    "LeBron James",
    # "Tyrese Maxey",
    "Damian Lillard",
    'Tyrese Haliburton',
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

pg_options= {'ppg': [], 'rpg': [], 'apg': [], \
    'fgapg': [], 'fgmpg': [], 'fgpt': [], 'fg3apg':[], 'fg3mpg':[], \
    'fg3pt': [], 'ftapg': [], 'ftmpg': [], 'spg': [], 'bpg': [], 'tpg': [], 'fpg': [], 'mpg': []}



z = 2023
m = 0

r = (0,0,0)
sub = None
isSubmitted = 'No'
def setup():
    global sub, f
    size(600,600)

    for i, key in enumerate(pg_options):
        yval = 50 + (60*(i//9))
        xval = 50 + (60*(i%9))
        buttonsX.append(Button((xval,yval), key))
    
    for i, key in enumerate(pg_options):
        yval = 400 + (60*(i//9))
        xval = 50 + (60*(i%9))
        buttonsY.append(Button((xval,yval), key))
        
    buttonsX.append(Button((275,170), 'seasons'))
    buttonsX.append(Button((340,170), 'years'))


    sub = Button((300,300), 'Submit')


    f = create_font("Montserrat-Regular.ttf", 16) 

def draw():
    global r, sub, xAxis, yAxis, isSubmitted, \
        pg_options, superstars, z, m, f
    background(255)
    fill(*r)

    text_font(f, 10)



    for b in buttonsX:
        b.render()
        if mouse_is_pressed:
            d = b.clicked()
            if d[1] == True:
                xAxis = d[0]
                print(xAxis)

    for b in buttonsY:
        b.render()
        if mouse_is_pressed:
            d = b.clicked()
            if d[1] == True:
                yAxis = d[0]
                print(yAxis)


    sub.render()
    if mouse_is_pressed:
        d = sub.clicked()
        if d[1] == True:
            isSubmitted = d[0]
        fill(255,0,0)
    ellipse(mouse_x, mouse_y, 5,5)

    if isSubmitted == 'Submit':
        print(xAxis, yAxis, z, m)
        plotter(superstars, pg_options, xAxis, yAxis, z, m)
        exit()
run()