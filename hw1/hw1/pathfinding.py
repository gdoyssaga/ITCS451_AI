"""This module contains classes and function to solve a pathfinding problem.

Author:
    -Sathita Intrachhote
    -Thanapron Khunprom
Student ID:
    -6288014
    -6288083
"""

# %%

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List, Callable, Union

from numpy.lib.nanfunctions import nanmedian
from hw1.envutil import render_maze,find_agent

import numpy as np

@dataclass(frozen=True, unsafe_hash=False)
class MazeState:

    # TODO 1: Add other state information here.
    grid: np.ndarray
    # If you need anything more than `grid`, please add here


    # TODO 2 Create a list of all possible actions.
    # Please replace it with your own actions
    # Note that an agent can only rotate and move forward.
    actions: Tuple[str] = ('up', 'right', 'down','left','move')

    def __eq__(self, o: object) -> bool:
        if isinstance(o, MazeState):
            return np.all(self.grid == o.grid)
        return False

    def __hash__(self) -> int:
        return render_maze(self.grid).__hash__()

    # TODO 3: Create a transition function
    @classmethod
    def transition(cls, state: MazeState, action: str) -> MazeState:
        """Return a new state after performing `action`.

        If the action is not possible, it should return None.

        The mud disappears as soon as the agent walk onto it.

        Note
        ---------------------
        Keep in mind that you should not modify the previous state
        If you need to clone a numpy's array, you can do so like this:
        >>> y = np.array(x)
        >>> y.flags.writeable = False
        This will create an array y as a copy of array x and then make
        array y immutable (cannot be changed, for safty).
        """
        #Current position of agent
        x,y = find_agent(state.grid)
        #print(x,y)
        clone_grid =  np.array(state.grid)       
        #print(clone_grid)
        
        #method that make agent move
        def forward(arr: np.ndarray):
            x,y = find_agent(state.grid)
            #print(arr[x][y])
            if (arr[x][y-1] == 0 or arr[x][y-1] == 7) and (arr[x][y] == 5 and arr[x][y-1] != 1) : # L
                arr[x][y-1] = 5
                arr[x][y] = 0
                
            elif (arr[x-1][y] == 0 or arr[x-1][y] == 7) and (arr[x][y] == 2 and arr[x-1][y] != 1) :   #U             
                arr[x-1][y] = 2
                arr[x][y] = 0
              
            elif (arr[x][y+1] == 0 or arr[x][y+1] == 7) and (arr[x][y] == 3 and arr[x][y+1] != 1) :  #R
                arr[x][y+1] = 3
                arr[x][y] = 0
                
            elif (arr[x+1][y] == 0 or arr[x+1][y] == 7) and (arr[x][y] == 4 and arr[x+1][y] != 1) :  #D  
                arr[x+1][y] = 4
                arr[x][y] = 0 

            return arr;   


        #check each action 
        if action == 'move': # move 
            clone_grid = forward(clone_grid)  
        elif action == 'up': # up
            clone_grid[x][y] = 2
           
        elif action == 'right': # right
            clone_grid[x][y] = 3
                
        elif action == 'down': # d
            clone_grid[x][y] = 4
            
        elif action == 'left': # l
            clone_grid[x][y] = 5  
                      
        else:
             return None

         
        clone_grid.flags.writeable = False
        new_state = MazeState(clone_grid)
        return new_state
 
       

    # TODO 4: Create a cost function
    @classmethod
    def cost(cls, state: MazeState, action: str) -> float:
        """Return the cost of `action` for a given `state`.

        If the action is not possible, the cost should be infinite.

        Note
        ------------------
        You may come up with your own cost for each action, but keep in mind
        that the cost must be positive and any walking into
        a mod position should cost more than walking into an empty position.
        """
        #0 1 2 3
        #cost L,R,D,U, move -> 1  -> mud->2
        copy_grid =  np.array(state.grid)
        x,y = find_agent(copy_grid)

        #now let assume cost of move is 1.5 // mud is 2
        #check the agent can move or not
        def moveornot(a: np.ndarray):
            x,y = find_agent(state.grid)
             
            if a[x-1][y] == 0 and (a[x][y] == 2 and a[x-1][y] != 1) :   #U             
                return float(1)
            elif  a[x-1][y] == 7 and (a[x][y] == 2 and a[x-1][y] != 1) : #U mud
                return float(2)
            elif a[x][y+1] == 0  and (a[x][y] == 3 and a[x][y+1] != 1) :  #R
                return float(1) 
            elif a[x][y+1] == 7 and (a[x][y] == 3 and a[x][y+1] != 1) :  #Rmud:
                return float(2)
            elif a[x+1][y] == 0 and (a[x][y] == 4 and a[x+1][y] != 1) :  #D  
                return float(1)
            elif a[x+1][y] == 7 and (a[x][y] == 4 and a[x+1][y] != 1) :  #Dmud
                return float(2)
            elif a[x][y-1] == 0  and (a[x][y] == 5 and a[x][y-1] != 1) : # L
                return float(1)
            elif a[x][y-1] == 7 and (a[x][y] == 5 and a[x][y-1] != 1) : # Lmud
                return float(2)
            
            else:
                return float('inf')  

        #C is a number of cost       
        c = 0             
        if (action == 'up' and state.grid[x][y] == 2) or (action == 'right' and state.grid[x][y] == 3) or (action == 'down' and state.grid[x][y] == 4) or (action == 'left' and state.grid[x][y] == 5)  :
            c+=0
        elif action == 'up' or action == 'right' or action == 'down' or action == 'left' :
            c+=1
        elif action == 'move':
            c = moveornot(copy_grid)    
        return float(c)


    # TODO 5: Create a goal test function
    @classmethod
    def is_goal(cls, state: MazeState) -> bool:
        """Return True if `state` is the goal."""
        #point of goal
        size = len(state.grid)
        x,y = find_agent(state.grid)
        #check
        if state.grid[size-2][size-2] == state.grid[x][y]:
            return True
        else:
            return False

    # TODO 6: Create a heuristic function
    @classmethod
    def heuristic(cls, state: MazeState) -> float:
        """Return a heuristic value for the state.
        
        Note
        ---------------
        You may come up with your own heuristic function.
        """
        #Manhattan
        size = len(state.grid)
        x,y = find_agent(state.grid)
        ##Agent -> start x1 y1  Goal -> x2 y2
        x1 = x
        y1 = y
        x2 = size-2      
        y2 = size-2

        hs = abs(x1-x2)+abs(y1-y2)

        #print(x1,x2,y1,y2)
        return float(hs)
# %%

@dataclass
class TreeNode:
    path_cost: float
    state: MazeState
    action: str
    depth: int
    parent: TreeNode = None


def dfs_priority(node: TreeNode) -> float:
    return -1.0 * node.depth


def bfs_priority(node: TreeNode) -> float:
    return 1.0 * node.depth


# TODO: 7 Create a priority function for the greedy search
def greedy_priority(node: TreeNode) -> float:

    return 0.0


# TODO: 8 Create a priority function for the A* search
def a_star_priority(node: TreeNode) -> float:
    return 0.0


# TODO: 9 Implement the graph search algorithm.
def graph_search(
        init_state: MazeState,
        priority_func: Callable[[TreeNode], float]) -> Tuple[List[str], float]:
    """Perform graph search on the initial state and return a list of actions.

    If the solution cannot be found, return None and infinite cost.
    """
    return None, float('inf')
