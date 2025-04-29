import random
import csv
import json
import time

random.seed(time.time())

class Problem:
    def __init__(self, name: str, year: int, day: int, problemNumber: int, problemLetter: str, averageScore: str, averageRatio: str, maxScore: str, acCnt: str, acRatio: str, dmojLink: str, ojuzLink: str):
        self.name = name
        self.year = year
        self.day = day
        self.problemNumber = problemNumber
        self.problemLetter = problemLetter
        self.averageScore = averageScore
        self.averageRatio = averageRatio
        self.maxScore = maxScore
        self.acCnt = acCnt
        self.acRatio = acRatio
        self.dmojLink = dmojLink
        self.ojuzLink = ojuzLink
    
    def disp(self):        
        return f"IOI{str(self.year)[::-1][:2][::-1]}/{self.problemNumber}, {self.name}"
        
    def getCode(self):
        return str(self.year) + "_" + self.name.lower().replace(' ', '').replace('\'', '')
    
    def getStats(self) -> str:
        return f"Average score: **{self.averageScore}/{self.maxScore}**\nIn-contest AC Count: **{self.acCnt}**\nIn-contest AC ratio: **{self.acRatio}**"

    def getLinks(self) -> str:
        return f"DMOJ: {self.dmojLink}\nOJ.uz: {self.ojuzLink}"
        

problems = []
codeToProb = {}

# shit to keep track of
# year,day,dayLetter,problem,properName,maxScore,avgScore,avgRatio,acCnt,acRatio,dmojLink,ojuzLink,ojCode
# name: str
# year: int
# day: int
# problemNumber: int
# problemLetter: str
# averageScore: float
# averageRatio: float
# acCnt: int
# acRatio: float
# dmojLink: str
# ojuzLink: str

def reset(resetConfirmation: str):
    if(resetConfirmation != "I AM WILLINGLY RESETTING THE DATA."): return
    thing = {0: []}

    jsonObj = json.dumps(thing, indent=3)

    with open("ioi_solve.json", "w") as out:
        out.write(jsonObj)
    
    with open("ioi_pending.json", "w") as out:
        out.write(jsonObj)

def init():
    problemFile = open('ioi.csv', newline='')
    reader = csv.DictReader(problemFile)

    for row in reader:
        prob = Problem(row["properName"], 
                                int(row["year"]), 
                                int(row["day"]), 
                                int(row['problem']), 
                                row["dayLetter"],
                                row["avgScore"], 
                                row["avgRatio"],
                                row["maxScore"],
                                row["acCnt"],
                                row["acRatio"],
                                row['dmojLink'],
                                row['ojuzLink'])
        problems.append(prob)
        codeToProb[prob.getCode()] = prob

def solveProblem(usercode: str | int, prob: Problem, force_solved: bool = False):
    usercode = str(usercode)
    fl = open("ioi_solve.json", "r")
    fl2 = open("ioi_pending.json", "r")
    solved = json.load(fl)
    pend = json.load(fl2)
    fl.close()
    fl2.close()
    probCode = prob.getCode()

    if usercode not in list(solved.keys()):
        print(f"added {usercode} to json")
        solved[usercode] = []
        pend[usercode] = []
    
    if probCode in solved[usercode]:
        return "bro you've already solved that LMAO"
    else:
        if probCode in pend[usercode]:
            pend[usercode].remove(probCode)
        elif not force_solved:
            return "not in pending."
        print("added")
        solved[usercode].append(probCode)
    
    fl = open("ioi_solve.json", "w")
    fl2 = open("ioi_pending.json", "w")
    fl.write('')
    fl2.write('')
    fl.close()
    fl2.close()
    
    fl = open("ioi_solve.json", "w")
    fl2 = open("ioi_pending.json", "w")
    json.dump(obj = solved, fp = fl)
    json.dump(obj = pend, fp = fl2)
    
    fl.close()
    fl2.close()
    
    
def pendProblem(usercode: str | int, prob: Problem):
    usercode = str(usercode)
    fl = open("ioi_solve.json", "r")
    fl2 = open("ioi_pending.json", "r")
    solved = json.load(fl)
    pend = json.load(fl2)
    fl.close()
    fl2.close()
    probCode = prob.getCode()
    
    print(usercode, probCode)
    
    if usercode not in list(solved.keys()):
        print(f"added {usercode} to json")
        solved[usercode] = []
        pend[usercode] = []
    
    if probCode in solved[usercode]:
        return "bro you've already solved that."
    elif probCode in pend[usercode]:
        return "already in pending."
    else:        
        pend[usercode].append(probCode)
    
        fl = open("ioi_solve.json", "w")
    fl2 = open("ioi_pending.json", "w")
    fl.write('')
    fl2.write('')
    fl.close()
    fl2.close()
    
    fl = open("ioi_solve.json", "w")
    fl2 = open("ioi_pending.json", "w")
    json.dump(obj = solved, fp = fl)
    json.dump(obj = pend, fp = fl2)
    
    fl.close()
    fl2.close()

        
def challenge(usercode: str | int) -> Problem | int:
    usercode = str(usercode)
    fl = open("ioi_solve.json", "r")
    fl2 = open("ioi_pending.json", "r")
    solved = json.load(fl)
    pend = json.load(fl2)
    fl.close()
    fl2.close()
    randArr = []
    
    if usercode not in list(solved.keys()):
        print(f"added {usercode} to json")
        solved[usercode] = []
        pend[usercode] = []

    for problem in problems:
        if problem in solved[usercode]: continue
        if problem in pend[usercode]: continue
        randArr.append(problem)

    fl = open("ioi_solve.json", "w")
    fl2 = open("ioi_pending.json", "w")
    fl.write('')
    fl2.write('')
    json.dump(solved, fl)
    json.dump(pend, fl2)
    
    fl.close()
    fl2.close()
    
    return [random.choice(randArr), le  (randArr)]

init()