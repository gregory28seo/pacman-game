# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from pacman import Directions
from game import Agent
import random
import math
from Queue import PriorityQueue

class CompetitionAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.goalPosition = None
        self.whiteGhost = False
        self.capsulesDone = False
        self.currentState = None
        return;
    
    def calculateDistance(self, start, end):
        x1 = start[0]
        y1 = start[1]
        x2 = end[0]
        y2 = end[1]
        return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    
    def getNearestPowerPellet(self, state):
        rankingQueue = PriorityQueue()
        powerPelletArray = state.getCapsules()
        for pp in powerPelletArray:
            dist = self.calculateDistance(state.getPacmanPosition(), pp)
            rankingQueue.put(( 1 * dist, pp))
        nearestPower = rankingQueue.get()
        if nearestPower!= None:
            return nearestPower[1]
        else:
            return self.findNearestPellets(state)
        
    def evaluationOfStep(self, childState):
        score =  childState.getScore() - self.currentState.getScore()
        dist = 40 - self.calculateDistance(childState.getPacmanPosition(), self.goalPosition)
        return dist * 30 + score * 70
    
    def evaluationOfGame(self, state):
        score =  state.getScore() - self.currentState.getScore()
        dist = 40 - self.calculateDistance(state.getPacmanPosition(), self.goalPosition)
        return dist * 50 + score * 50
    
    def getNextBestState(self, st):
        #print "iin best State"
        rankingQueue = PriorityQueue()
        actions = st.getLegalPacmanActions()
        if len(actions) == 0:
            return None
        for act in actions:
            childState = st.generatePacmanSuccessor(act)
            if childState == None:
                return None
            else:
                if childState.isWin() or childState.getPacmanPosition() == self.goalPosition:
                    return childState
                else:
                    if childState.isLose():
                        return None
                    else:
                        eval = self.evaluationOfStep(childState)
                        rankingQueue.put((eval * -1, childState))
        bestState = rankingQueue.get()
        if bestState != None:
            return bestState[1]
        else:
            return None
        #print "best stae end", bestState
    
    def getBestAction(self, state, actions):
        #print "in best action"
        rankingQueue = PriorityQueue()
        stateArray = []
        for action in actions:
            stateArray.append(state.generatePacmanSuccessor(action))
        possible = True
        arrayLength = len(stateArray)
        while(possible and (arrayLength > 0)):
            for st in range(arrayLength):
                childState = self.getNextBestState(stateArray[st])
                if childState != None:
                    #print "in if"
                    if childState != "Loss":
                        stateArray[st] = childState
                    else:
                        stateArray.pop(st)
                        actions.pop(st)
                        arrayLength = arrayLength - 1
                        
                    if childState.getPacmanPosition() == self.goalPosition:
                        #print "new pacman postiion"
                        self.capsulesDone = True
                        self.goalPosition = self.findNearestPellets(childState)
                else:
                    possible = False
        
        for st in range(len(stateArray)):
            eval = self.evaluationOfGame(stateArray[st])
            rankingQueue.put((eval * -1, actions[st]))
        bestAction = rankingQueue.get()
        if bestAction != None:
            return bestAction[1]
        else:
            return Directions.stop
        #print "bestAction", bestAction
    
    def makeMove(self, state):
        actions = state.getLegalPacmanActions()
        act = self.getBestAction(state, actions)
        #return Directions.EAST
        return act
    
    def findNearestPellets(self, state):
        rankingQueue = PriorityQueue()
        mat = state.getFood()
        for i in range(len(mat[0])):
            for j in range(len(mat[i])):
                if mat[i][j] == True:
                    #print "in"
                    #return (i,j)
                    dist = self.calculateDistance(state.getPacmanPosition(), (i,j))
                    rankingQueue.put(( 1 * dist, (i,j)))
        nearestPellet = rankingQueue.get()
        #print nearestPellet
        if nearestPellet != None:
            #return nearestPellet[1]
            return state.getFood()[0]
        else:
            return state.getFood()[0]
        
    # GetAction Function: Called with every frame
    def getAction(self, state):
        #print "start"
        self.currentState = state
        if len(state.getCapsules()) > 0:
            self.capsulesDone = False
        if not self.capsulesDone:
            self.goalPosition = self.getNearestPowerPellet(state)
        else:
            self.goalPosition = self.findNearestPellets(state)
        #print "goal", self.goalPosition
        action = self.makeMove(state)
        #print "final", action
        return action
