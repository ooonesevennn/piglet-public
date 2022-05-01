# baselineTeam.py
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


# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from typing import List, Tuple
from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys, os
from capture import GameState, noisyDistance
from game import Directions, Actions, AgentState, Agent
from util import nearestPoint
import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
base_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_folder+"/../") # make sure we can import pddl solver from piglet
from lib_piglet.utils.pddl_solver import pddl_solver

CLOSE_DISTANCE = 4
MEDIUM_DISTANCE = 15
LONG_DISTANCE = 25

#################
# Team creation #
#################


def createTeam(firstIndex, secondIndex, isRed,
                             first = 'MixedAgent', second = 'MixedAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

############################################################
# Exchange Information Between Agents with Global Variables#
############################################################

CURRENT_ACTION = {}

##########
# Agents #
##########                                       

class MixedAgent(CaptureAgent):
    """
    This is an agent that use pddl to guide the high level actions of Pacman
    """

    def registerInitialState(self, gameState: GameState):
        self.pddl_solver = pddl_solver(base_folder+'/pacman_bool.pddl')
        self.plan = None # list of actions
        self.currentActionIndex = 0 # index of action in self.plan should be execute next

        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

        self.epsilon = 0.0 #exploration prob
        self.alpha = 0.2 #learning rate
        self.discountRate = 0.8
        self.offensiveWeights = {'closest-food': -1, 
                                        'bias': 1, 
                                        '#-of-ghosts-1-step-away': -100, 
                                        'successorScore': 100, 
                                        'eats-food': 10}
        self.defensiveWeights = {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}	
        self.escapeWeights = {'onDefense': 1000, 'enemyDistance': 30, 'stop': -100, 'distanceToHome': -20}
        CURRENT_ACTION[self.index]={}
        """
        Open weights file if it exists, otherwise start with empty weights.
        NEEDS TO BE CHANGED BEFORE SUBMISSION

        """
        # if os.path.exists(base_folder+'/offensiveWeights.txt'):
        #     with open(base_folder+'/offensiveWeights.txt', "r") as file:
        #         self.offensiveWeights = eval(file.read())
        
        # if os.path.exists(base_folder + '/defensiveWeights.txt'):
        #     with open(base_folder+'/defensiveWeights.txt', "r") as file:
        #         self.defensiveWeights = eval(file.read())
        
        # if os.path.exists(base_folder+'/escapeWeights.txt'):
        #     with open(base_folder+'/escapeWeights.txt', "r") as file:
        #         self.escapeWeights = eval(file.read())
    
    def final(self, gameState : GameState):
        """
        This function write weights into files after the game is over. 
        You may want to comment (disallow) this function when submit to contest server.
        """
        file = open('offensiveWeights.txt', 'w')
        file.write(str(self.offensiveWeights))
        file.close()

        file = open('defensiveWeights.txt', 'w')
        file.write(str(self.defensiveWeights))
        file.close()

        file = open('escapeWeights.txt', 'w')
        file.write(str(self.escapeWeights))
        file.close()
    

    def chooseAction(self, gameState: GameState):
        """
        Picks among the actions with the highest Q(s,a).
        """

        # get high level action from pddl plan
        highLevelAction: str = self.getHighLevelAction(gameState)

        # get exact low level plan to achieve the high level action. 
        if highLevelAction == "go_to_enemy_land" or highLevelAction == "eat_food":
            action = self.getOffensiveAction(gameState)
        elif highLevelAction == "go_home" or highLevelAction == "unpack_food":
            action = self.getEscapeAction(gameState)
        else:
            action = self.getDefensiveAction(gameState)
        return action

    #------------------------------- PDDL and High-Level Action Functions ------------------------------- 
    
    def getHighLevelAction(self,gameState: GameState):
        # Get high level action from a pddl plan.

        # Collect objects and init states from gameState
        objects, initState = self.get_pddl_state(gameState)

        # Check if we can stick to current plan 
        if not self.stateSatisfyCurrentPlan(initState):
            # Cannot stick to current plan, prepare goals and replan
            positiveGoal, negtiveGoal = self.getGoals(objects,initState)
            print("Agnet:",self.index,"compute plan:")
            print("\tOBJ:"+str(objects),"\tINIT:"+str(initState), "\tPOSITIVE_GOAL:"+str(positiveGoal), "\tNEGTIVE_GOAL:"+str(negtiveGoal),sep="\n")
            self.plan = self.getPlan(objects, initState,positiveGoal, negtiveGoal)
            self.currentActionIndex = 0
            print("\tPLAN:",self.plan)
        if len(self.plan)==0:
            raise Exception("Solver retuned empty plan, you need to think how you handle this situation or how you modify your model ")
        
        # Get next action from the plan
        highLevelAction = self.plan[self.currentActionIndex][0]
        CURRENT_ACTION[self.index] = highLevelAction.name
        print("Agent:", self.index, highLevelAction.name)
        return highLevelAction.name
    
    def getPlan(self, objects, initState, positiveGoal, negtiveGoal):
        # Prepare pddl problem
        self.pddl_solver.parser_.reset_problem()
        self.pddl_solver.parser_.set_objects(objects)
        self.pddl_solver.parser_.set_state(initState)
        self.pddl_solver.parser_.set_negative_goals(negtiveGoal)
        self.pddl_solver.parser_.set_positive_goals(positiveGoal)
        
        # Solve the problem and return the plan
        return self.pddl_solver.solve()

    def get_pddl_state(self,gameState:GameState) -> Tuple[List[Tuple],List[Tuple]]:
        # Collect objects and states from the gameState

        states = []
        objects = []


        # Collect available foods on the map
        foodLeft = self.getFood(gameState).asList()
        if len(foodLeft) > 0:
            states.append(("food_available",))
        myPos = gameState.getAgentPosition(self.index)
        myObj = "a{}".format(self.index)
        cloestFoodDist = self.closestFood(myPos,self.getFood(gameState), gameState.getWalls())
        if cloestFoodDist <=CLOSE_DISTANCE:
            states.append(("near_food",myObj))

        # Collect capsule states
        capsules = self.getCapsules(gameState)
        if len(capsules) > 0 :
            states.append(("capsule_available",))
        for cap in capsules:
            if self.getMazeDistance(cap,myPos) <=CLOSE_DISTANCE:
                states.append(("near_capsule",myObj))
                break
        
        # Collect winning states
        currentScore = gameState.data.score
        if gameState.isOnRedTeam(self.index):
            if currentScore > 0:
                states.append(("winning",))
            if currentScore> 3:
                states.append(("winning_gt3",))
            if currentScore> 5:
                states.append(("winning_gt5",))
            if currentScore> 10:
                states.append(("winning_gt10",))
            if currentScore> 20:
                states.append(("winning_gt20",))
        else:
            if currentScore < 0:
                states.append(("winning",))
            if currentScore < -3:
                states.append(("winning_gt3",))
            if currentScore < -5:
                states.append(("winning_gt5",))
            if currentScore < -10:
                states.append(("winning_gt10",))
            if currentScore < -20:
                states.append(("winning_gt20",))

        # Collect team agents states
        agents : List[Tuple[int,AgentState]] = [(i,gameState.getAgentState(i)) for i in self.getTeam(gameState)]
        for agent_index, agent_state in agents :
            agent_object = "a{}".format(agent_index)
            agent_type = "current_agent" if agent_index == self.index else "ally"
            objects += [(agent_object, agent_type)]

            if agent_index != self.index and self.getMazeDistance(gameState.getAgentPosition(self.index), gameState.getAgentPosition(agent_index)) <= CLOSE_DISTANCE:
                states.append(("near_ally",))
            
            if agent_state.scaredTimer>0:
                states.append(("is_scared",agent_object))

            if agent_state.numCarrying>0:
                states.append(("food_in_backpack",agent_object))
                if agent_state.numCarrying >=20 :
                    states.append(("20_food_in_backpack",agent_object))
                if agent_state.numCarrying >=10 :
                    states.append(("10_food_in_backpack",agent_object))
                if agent_state.numCarrying >=5 :
                    states.append(("5_food_in_backpack",agent_object))
                if agent_state.numCarrying >=3 :
                    states.append(("3_food_in_backpack",agent_object))
                
            if agent_state.isPacman:
                states.append(("is_pacman",agent_object))
            
            

        # Collect enemy agents states
        enemies : List[Tuple[int,AgentState]] = [(i,gameState.getAgentState(i)) for i in self.getOpponents(gameState)]
        noisyDistance = gameState.getAgentDistances()
        typeIndex = 1
        for enemy_index, enemy_state in enemies:
            enemy_position = enemy_state.getPosition()
            enemy_object = "e{}".format(enemy_index)
            objects += [(enemy_object, "enemy{}".format(typeIndex))]

            if enemy_state.scaredTimer>0:
                states.append(("is_scared",enemy_object))

            if enemy_position != None:
                for agent_index, agent_state in agents:
                    if self.getMazeDistance(agent_state.getPosition(), enemy_position) <= CLOSE_DISTANCE:
                        states.append(("enemy_around",enemy_object, "a{}".format(agent_index)))
            else:
                if noisyDistance[enemy_index] >=LONG_DISTANCE :
                    states.append(("enemy_long_distance",enemy_object, "a{}".format(self.index)))
                elif noisyDistance[enemy_index] >=MEDIUM_DISTANCE :
                    states.append(("enemy_medium_distance",enemy_object, "a{}".format(self.index)))
                else:
                    states.append(("enemy_short_distance",enemy_object, "a{}".format(self.index)))                                                                                                                                                                                                 


            if enemy_state.isPacman:
                states.append(("is_pacman",enemy_object))
            typeIndex += 1
            

        
        return objects, states
    
    def stateSatisfyCurrentPlan(self, init_state: List[Tuple]):
        if self.plan is None:
            # No plan, need a new plan
            return False
        
        if self.pddl_solver.matchEffect(init_state, self.plan[self.currentActionIndex][0] ):
            # The current state match the effect of current action, current action action done, move to next action
            if self.currentActionIndex < len(self.plan) -1 and self.pddl_solver.satisfyPrecondition(init_state, self.plan[self.currentActionIndex+1][0]):
                # Current action finished and next action is applicable
                self.currentActionIndex += 1
                return True
            else:
                # Current action finished, next action is not applicable or finish last action in the plan
                return False

        if self.pddl_solver.satisfyPrecondition(init_state, self.plan[self.currentActionIndex][0]):
            # Current action precondition satisfied, continue executing current action of the plan
            return True
        
        # Current action precondition not satisfied anymore, need new plan
        return False
    
    def getGoals(self, objects: List[Tuple], initState: List[Tuple]):
        # Check a list of goal functions from high priority to low priority if the goal is applicable
        # Return the pddl goal states for selected goal function
        if (("winning_gt5",) in initState):
            return self.goalDefWinning(objects, initState)
        else:
            return self.goalScoring(objects, initState)

    def goalScoring(self,objects: List[Tuple], initState: List[Tuple]):
        # If we are not winning more than 5 points,
        # we invate enemy land and eat foods, and bring then back.

        positiveGoal = []
        negtiveGoal = [("food_available",)] # no food avaliable means eat all the food

        for obj in objects:
            agent_obj = obj[0]
            agent_type = obj[1]
            if agent_type == "current_agent":
                negtiveGoal += [("food_in_backpack", agent_obj)] # we have to unpack food at home to gain score.
            
            if agent_type == "enemy1" or agent_type == "enemy2":
                negtiveGoal += [("is_pacman", agent_obj)] # no enemy should standing on our land.
        
        return positiveGoal, negtiveGoal

    def goalDefWinning(self,objects: List[Tuple], initState: List[Tuple]):
        # If winning greater than 5 points,
        # this example want defend foods only, and let agents patrol on our ground.
        # The "win_the_game" pddl state is only reachable by the "patrol" action in pddl,
        # using it as goal, pddl will generate plan eliminate invading enemy and patrol on our ground.

        positiveGoal = [("win_the_game",)]
        negtiveGoal = []
        
        return positiveGoal, negtiveGoal

    #------------------------------- Q-learning and low level action Functions -------------------------------

    """
    Iterate through all features (closest food, bias, ghost dist),
    multiply each of the features' value to the feature's weight,
    and return the sum of all these values to get the q-value.
    """
    def getQValue(self, gameState, action):
        #############
        # Implement your code to calculate and return Q value
        #############

        q_value = 0
        return q_value

    """
    Iterate through all q-values that we get from all
    possible actions, and return the highest q-value
    """
    def getValue(self, gameState):
        legalActions = gameState.getLegalActions(self.index)
        if len(legalActions) == 0:
                return 0.0
        else:
                #############
                # Implement your return max Q value from all legalActions for a given state
                #############
                maxQvalue = 0
                return maxQvalue

    """
    Iterate through all q-values that we get from all
    possible actions, and return the action associated
    with the highest q-value.
    """
    def getPolicy(self, gameState):
        values = []
        legalActions = gameState.getLegalActions(self.index)
        legalActions.remove(Directions.STOP)
        if len(legalActions) == 0:
                return None
        else:
                for action in legalActions:
                        self.updateWeights(gameState, action)
                        values.append((self.getQValue(gameState, action), action))
        return max(values)[1]
    
    """
    Iterate through all features and for each feature, update
    its weight values using the following formula:
    w(i) = w(i) + alpha((reward + discount*value(nextState)) - Q(s,a)) * f(i)(s,a)
    """
    def updateWeights(self, gameState, action):
        features = self.getFeatures(gameState, action)
        nextState = self.getSuccessor(gameState, action)

        # Calculate the reward. NEEDS WORK
        reward = nextState.getScore() - gameState.getScore()

        for feature in features:
            ####################
            # Impletement your codes to perform Approximate Q-learning update on each weight in self.weights.
            ####################
            pass 

    #------------------------------- Low Level Action Functions -------------------------------

    def getOffensiveAction(self, gameState: GameState):
        actions = gameState.getLegalActions(self.index)

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.getOffensiveEvaluate(gameState, a) for a in actions]
        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        foodLeft = len(self.getFood(gameState).asList())
        
        if foodLeft <= 2:
            bestDist = 9999
            for action in actions:
                successor = self.getSuccessor(gameState, action)
                pos2 = successor.getAgentPosition(self.index)
                dist = self.getMazeDistance(self.start,pos2)
                if dist < bestDist:
                    bestAction = action
                    bestDist = dist
            return bestAction

        return random.choice(bestActions)
    
    """
    Calculate probability of 0.1.
    If probability is < 0.1, then choose a random action from
    a list of legal actions.
    Otherwise use the policy defined above to get an action.
    """
    def chooseOffensiveQLearningAction(self, gameState):
        # This function is not using at this stage. you need to complete this function and replace the old chooseOffensiveAction function.
        # Pick Action
        legalActions = gameState.getLegalActions(self.index)
        action = None

        if len(legalActions) != 0:
                ############
                # At here, current code only returns actions through calculate Q value.
                # Change the codes here to have a probability of self.epsilon to return random action.
                ###########

                action = self.getPolicy(gameState)
        return action
    
    def getOffensiveEvaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getOffensiveFeatures(gameState, action)
        weights = self.getOffensiveWeights(gameState, action)
        return features * weights
    
    def getOffensiveFeatures(self, gameState, action):
        food = self.getFood(gameState) 
        walls = gameState.getWalls()
        ghosts = []
        opAgents = CaptureAgent.getOpponents(self, gameState)
        # Get ghost locations and states if observable
        if opAgents:
                for opponent in opAgents:
                        opPos = gameState.getAgentPosition(opponent)
                        opIsPacman = gameState.getAgentState(opponent).isPacman
                        if opPos and not opIsPacman: 
                                ghosts.append(opPos)
        
        # Initialize features
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        # Successor Score
        features['successorScore'] = self.getScore(successor)

        # Bias
        features["bias"] = 1.0
        
        # compute the location of pacman after he takes the action
        x, y = gameState.getAgentPosition(self.index)
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)
        
        # Number of Ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)
        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
                features["eats-food"] = 1.0

        # Number of Ghosts scared
        #features['#-of-scared-ghosts'] = sum(gameState.getAgentState(opponent).scaredTimer != 0 for opponent in opAgents)
        
        # Closest food
        dist = self.closestFood((next_x, next_y), food, walls)
        if dist is not None:
                # make the distance a number less than one otherwise the update
                # will diverge wildly
                features["closest-food"] = float(dist) / (walls.width * walls.height) 

        # Normalize and return
        features.divideAll(10.0)
        return features

    def getOffensiveWeights(self, gameState, action):
        return self.offensiveWeights
    
    def getEscapeAction(self, gameState):
        actions = gameState.getLegalActions(self.index)

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.getEscapeEvaluate(gameState, a) for a in actions]
        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        return random.choice(bestActions)

    def getEscapeEvaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getEscapeFeatures(gameState, action)
        weights = self.getEscapeWeights(gameState, action)
        return features * weights

    def getEscapeFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0)
        features['onDefense'] = 1
        if myState.isPacman: features['onDefense'] = 0

        # Computes distance to invaders we can see
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        enemiesAround = [a for a in enemies if not a.isPacman and a.getPosition() != None]
        if len(enemiesAround) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in enemiesAround]
            features['enemyDistance'] = min(dists)

        if action == Directions.STOP: features['stop'] = 1
        features["distanceToHome"] = self.getMazeDistance(myPos,myState.start.getPosition())

        return features

    def getEscapeWeights(self, gameState, action):
        return self.escapeWeights
    
    def getDefensiveAction(self, gameState):
        actions = gameState.getLegalActions(self.index)

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.getDefensiveEvaluate(gameState, a) for a in actions]
        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        return random.choice(bestActions)

    def getDefensiveEvaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getDefensiveFeatures(gameState, action)
        weights = self.getDefensiveWeights(gameState, action)
        return features * weights

    def getDefensiveFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0)
        features['onDefense'] = 1
        if myState.isPacman: features['onDefense'] = 0

        # Computes distance to invaders we can see
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        features['numInvaders'] = len(invaders)
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if action == Directions.STOP: features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: features['reverse'] = 1

        return features

    def getDefensiveWeights(self, gameState, action):
        return self.defensiveWeights
    
    def closestFood(self, pos, food, walls):
        fringe = [(pos[0], pos[1], 0)]
        expanded = set()
        while fringe:
            pos_x, pos_y, dist = fringe.pop(0)
            if (pos_x, pos_y) in expanded:
                continue
            expanded.add((pos_x, pos_y))
            # if we find a food at this location then exit
            if food[pos_x][pos_y]:
                return dist
            # otherwise spread out from the location to its neighbours
            nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
            for nbr_x, nbr_y in nbrs:
                fringe.append((nbr_x, nbr_y, dist+1))
        # no food found
        return None
    
    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor
    

