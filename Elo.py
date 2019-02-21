import random, os, math


class player:
    def __init__(self, fname, sname, elo):
        self.fn = fname
        self.sn = sname
        self.elo = elo

class team:
    def __init__(self, name, roster):
        self.nm = name
        self.rs = roster

    def addmember(self, member):
        self.rs.append(member)

    def removemember(self, fname, sname):
        self.fn = fname
        self.sn = sname

def elocalc(team):
    elo = 0
    tp = len(team.rs)
    for k in range(tp):
        elo += team.rs[k].elo
    elo = elo/tp
    if tp == 6:
        elo *= 1.068
    elif tp == 7:
        elo *= 1.122
    elif tp == 8:
        elo *= 1.166
    return elo

#Reading File
file = open("players.txt", "r")
length = len(file.readlines())
file.seek(0)

players = [0] * length
i = 0
for i in range(length):
    line = file.readline()
    fname = ""
    sname = ""
    elo = ""
    k = 0
    for j in line:
        if j == " ":
            k += 1
        if k == 0:
            fname += j
        if k == 1 and j != " ":
            sname += j
        if k == 2 and j != " ":
            elo += j
    players[i] = player(fname, sname, int(elo))
file.close()
        


#Presets
#teams = [team("a",[player("bil","by",400),player("jan","dee",400)]),team("b",[player("bil","by",350),player("jan","dee",350)])]
teams = []

#The code
i = 0 
while i != 5:
    i = int(input("Create New Player(1)\nCreate Team(2)\nEdit Team(3)\nEnter Match(4)\nExit(5)\n"))
    if i == 1:
        players.append(player(input("Player First Name\n"), input("Player Last Name\n"), input("Player starting Elo (default = 1000)\n")))  
    elif i == 2:
        teams.append(team(input("Team Name(one word)\n"),[]))
    elif i == 3:
        for j in range(len(teams)):
            print(teams[j].nm,"(",j,")")
        cteam = teams[int(input())]        
        j = 0
        while j != 3:
            print("\nCurrently editing team: ",cteam.nm)
            j = int(input("Add Player(1)\nRemove Player(2)\nLeave Team Edit(3)\n"))
            if j == 1:
                fname = input("Player Name\n")
                maybe = []
                while len(maybe) == 0:
                    for k in range(len(players)):
                        if players[k].fn == fname:
                            maybe.append(players[k])
                print("Which",fname,"?")
                for k in range(len(maybe)):
                    print(maybe[k].sn,"(",k,")")
                cteam.rs.append(maybe[int(input())])            
            if j == 2:
                for k in range(len(cteam.rs)):
                    print(cteam.rs[k].fn,cteam.rs[k].sn,"(",k,")")
                cteam.rs.remove(cteam.rs[int(input())])
                print("player removed")
    elif i == 4:
        print("Choose first team")
        for k in range(len(teams)):
            print(teams[k].nm,"(",k,")")
        team1 = teams[int(input())]
        team2 = teams[int(input("Choose second team\n"))]
#Calculating Elo
        print("How many goals where scored by team",team1.nm)
        g1 = int(input())
        print("How many goals where scored by team",team2.nm)
        g2 = int(input())
        g = abs(g1 - g2)
        if g < 2:
            g = 1
        elif g == 2:
            g = 3/2
        else:
            g = (11 + (g))/8
        if g1 > g2:
            w = 1
        elif g2 > g1:
            w = 0
        else:
            w = 0.5
        
        t1e = elocalc(team1)
        t2e = elocalc(team2)
        dr = abs(t1e-t2e)
        we = 1/(10**(((-1)*dr)/400)+1)
        if t1e > t2e:
            t1we = we
        else:
            t1we = 1 - we
        t2we = 1 - t1we
        p = round(50 * g * (w - t1we))
        for j in range(len(team1.rs)):
            team1.rs[j].elo += p
            for k in range(len(players)):
                if players[k].fn == team1.rs[j].fn and players[k].sn == team1.rs[j].sn:
                    players[k].elo = team1.rs[j].elo
        for j in range(len(team2.rs)):
            team2.rs[j].elo -= p
            for k in range(len(players)):
                if players[k].fn == team2.rs[j].fn and players[k].sn == team2.rs[j].sn:
                    players[k].elo = team2.rs[j].elo

        
        
#Saving to File        
file = open("players.txt", "w")

for i in range(len(players)):
    file.write(players[i].fn)
    file.write(" ")
    file.write(players[i].sn)
    file.write(" ")
    file.write(str(players[i].elo))
    file.write("\n")
  
file.close()

    
