# Tauha Imran 22i1239 cs-g AI-A1
#edit driver code at end of file to run specific test cases...

# -*- coding: utf-8 -*-
"""AIA1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lh8NhpnkuL1xpQ11dvmErsGW18v8lJVo
"""

# Tauha Imran 22i1239 cs-g AI-A1
import os
import re
import math
import numpy as np

##################################### GRID #####################################
class GRID:
    def __init__(self,file_path):
        self.grid = self.read_file_grid(file_path)
        self.m = len(self.grid)
        self.n = len(self.grid[0])

    def read_file_grid2(self,file_path):
      line_num = -1
      size = 0
      # Initialize temp_grid as a list of lists
      temp_grid = [[] for _ in range(10)]
      with open(file_path, 'r') as file:
          for line in file:
              if(line_num<0):
                  size = int(line.strip())
                  # Re-initialize temp_grid with the correct size
                  temp_grid = [[] for _ in range(size)]
              if(line_num>=0):
                  # Append each character as a string to the current row
                  temp_grid[line_num].extend(list(line.strip()))
              line_num+=1
      return temp_grid

    def read_file_grid(self,file_path):
        line_num = -1
        size = 0
        temp_grid = np.zeros((10,10), dtype=str)
        with open(file_path, 'r') as file:
            for line in file:
                if(line_num<0):
                    size = int(line.strip())
                    temp_grid = np.zeros((size,size), dtype=str)
                if(line_num>=0):
                    for i in range(0,size):
                        temp_grid[line_num][i] = line[i] #changing it to a str..
                line_num+=1
        return temp_grid

    def get_grid(self):
        return self.grid

    def get_val(self,x,y):
      # Check if x and y are within the grid boundaries
      if 0 <= x < self.m and 0 <= y < self.n:
          return self.grid[x][y]
      else:
          # Return a default value or raise an exception if out of bounds
          print(f"Warning: Accessing grid out of bounds at ({x}, {y}). Returning None")
          return None #returning None to avoid any future errors

    def update_grid(self,x,y,val):
        self.grid[x][y] = val

    def print_grid(self):
        print( "M x N = " , self.m ,  " x " , self.n )
        for i in range(0,self.m):
            row = self.grid[i]
            print(row)

    def get_surrounding_stats(self,x,y,robot):
      surrounding = []
      OBSTACLE =['A','R','X']
      if 0 <= x < self.m and 0 < y < self.n:
        if self.get_val(x,y-1) not in OBSTACLE :
          #print( f">>U ( {x},{y-1}) :" , self.get_val(x,y-1) , " or " ,self.grid[x][y-1] , " <<" )
          surrounding.append((x,y-1)) #up
      if 0 <= x < self.m and 0 <= y < self.n-1:
        #print( f">>D ( {x},{y+1}) :" , self.get_val(x,y+1) , " or " , self.grid[x][y+1] , " <<" )
        if self.get_val(x,y+1) not in OBSTACLE :
          surrounding.append((x,y+1)) #down
      if 0 < x < self.m and 0 <= y < self.n:
        #print( f">>L ( {x-1},{y}) :" , self.get_val(x-1,y) , " or " ,self.grid[x-1][y] , " <<" )
        if self.get_val(x-1,y) not in OBSTACLE :
          surrounding.append((x-1,y)) #left
      if 0 <= x < self.m-1 and 0 <= y < self.n:
        #print( f">>R ( {x+1},{y}) :" , self.get_val(x+1,y) , " or " ,self.grid[x+1][y] , " <<" )
        if self.get_val(x+1,y) not in OBSTACLE :
          surrounding.append((x+1,y)) #right
      #return robot.heuristic_stats(surrounding)
      return surrounding




##################################### ROBOT #####################################
class ROBOT: #single robot
    def __init__(self,id,start,end):
        self.id = id
        self.start = start
        self.end = end
        self.curr = self.start
        self.percept_sequence = []
        self.avoid = []
        self.path_found = False
        self.time = 0

    def robot_stats(self):
      if self:
        print(f'Robot ID: {self.id}')
        print(f'Start Position: {self.start}')
        print(f'End Position: {self.end}')
        print(f'Curr Position: {self.curr}')
      else:
        print("Robot not found.")

    def update_percept_sequence(self,percept):
      self.percept_sequence.append(percept)
      self.time+=1
      self.curr = percept

    def get_percept_sequence(self):
      return self.percept_sequence

    def print_sequence(self):
      if self.percept_sequence:
        print(self.percept_sequence)
      else:
        print("[ No Valid Path Possible ]")

    def print_time(self):
      print("Total Time: ",self.time)

    def move_robot(self,percept):
      if self.path_found == False:
        self.update_percept_sequence(self.curr)
        self.curr = percept
        if self.curr == self.end:
          self.update_percept_sequence(self.curr)
          self.path_found = True

    def move_robot_back(self):
      if self.path_found == False:
        to_avoid = self.percept_sequence[-1]
        self.percept_sequence.remove(to_avoid)
        self.avoid.append(to_avoid)
        self.time-=1
        self.curr = self.percept_sequence[-1]
        #if self.curr == self.start:
          #self.path_found = True
        if self.percept_sequence is None:
          self.path_found = True
        #self.update_percept_sequence(self.curr)
        #if len(self.percept_sequence) > 1:
        #  self.curr = self.percept_sequence[-2]
        #else:
        #  self.path_found = True
        # self.percept_sequence = []
        # self.curr = self.start

    def heuristic_stats(self,surrounding):
      H_stats = []
      for s in surrounding:
        H_stats.append((self.h(s[1][0],s[1][1]),s))
      return H_stats

    def h(self,x,y):
      # d = sqrt( (abs(x_end - x)^2 + (abs(y_end - y)^2 )
      distance = (abs(self.end[0]-x)**2 +abs(self.end[1]-y)**2)**0.5
      # h(x) = d(x,y) + time
      return distance + self.time



##################################### Rset #####################################
class Rset: # set of all robots
  def __init__(self,file_path):
    self.robots = self.read_file_robots(file_path)

  def read_file_robots(self,file_path):
    robots = []
    if os.path.exists(file_path):
      with open(file_path, 'r') as file:
        for line in file:
          line = line.strip()
          parts = line.split()
          pattern = r'\((\d+),\s*(\d+)\)'
          matches = re.findall(pattern, line)
          # Convert matches to a list of tuples of integers
          numbers = [(int(x), int(y)) for x, y in matches] #using regular expressions...
          #print(numbers)
          id = 'R'+parts[1][0]
          start = numbers[0]
          end = numbers[1]
          robots.append(ROBOT(id,start,end))
        return robots
    else:
        print("File not found.")
        return None

  def rset_stats(self):
    if self.robots:
      for r in self.robots:
        r.robot_stats()
        print('--------')
    else:
      print("Robots not found.")


##################################### AGENT #####################################
class AGENT:
    def __init__(self, id, positions, times):
        self.id = f"A{id}"
        self.positions = positions
        self.times = times
        self.ordered = self.order_positions()
        self.curr = 0
        self.curr_pos = self.ordered[self.curr]
        self.forward = True

    def order_positions(self):
        q = []
        for time, xy in zip(self.times, self.positions):
            q.append((time, xy))
        q.sort()
        return q

    def agent_move(self):
        if self.forward:
            self.curr += 1
            if self.curr >= len(self.ordered):
                self.forward = False
                self.curr = len(self.ordered) - 2
            self.curr_pos = self.ordered[self.curr]
        else:
            self.curr -= 1
            if self.curr < 0:
                self.forward = True
                self.curr = 1
            self.curr_pos = self.ordered[self.curr]


##################################### Aset #####################################

class Aset:
  def __init__(self,file_path):
    self.agents = self.read_agents_from_file(file_path)

  def read_agents_from_file(self,file_path):
      agents = []
      if os.path.exists(file_path):
          with open(file_path, 'r') as file:
              for line in file:
                  id, positions, times = self.extract_agent_data(line.strip())
                  agent = AGENT(id, positions, times)
                  agents.append(agent)
      else:
          print("File not found.")
      return agents

  def extract_agent_data(self, line):
      # Regular expression to find tuples of positions and list of times
      pattern_positions = r'\((\d+),\s*(\d+)\)'#r'\((\d+),\s*(\d+)\)'
      #pattern_positions = r'\((\d+),\s*(\d+)\)'
      #pattern_positions = r'\(\(([\d\s,]+)\)\)'
      pattern_times = r'\[(\d[\d\s,]*)\]'

      id = line.split()[1][:-1]  # Extracting the agent ID

      # Extracting the positions
      positions_match = re.findall(pattern_positions, line)
      #print(positions_match)
      positions = []
      if positions_match:
        #x, y = positions_match.groups()
        #positions = [(int(x), int(y)) for x, y in positions_match.group()] #using regular expressions...
        positions = [(int(x), int(y)) for x,y in positions_match]
        # Convert matches to a list of tuples of integers
        #positions = [(int(x), int(y)) for x, y in positions_match.group()] #using regular expressions...
        #positions_str = positions_match.group(2)
        #positions = [tuple(map(int, pos.split(','))) for pos in positions_str.split('), (')]

      # Extracting the times
      times_match = re.search(pattern_times, line)
      times = []
      if times_match:
          times_str = times_match.group(1)
          times = list(map(int, times_str.split(', ')))

      return id, positions, times

  def Aset_stats(self):
    if self.agents:
      for a in self.agents:
        print(f'Agent ID: {a.id}')
        print(f'Positions: {a.positions}')
        print(f'Times: {a.times}')
        print('--------')

  def agent_paths(self):
    if self.agents:
      for a in self.agents:
        print(f'Agent ID: {a.id}')
        print(f'Ordered Positions: {a.ordered}')
        print('--------')

##################################### SIMULATOR #####################################
class SIMULATOR:
  def __init__(self,grid,rset,aset):
    self.grid = grid
    self.robots = rset.robots
    self.agents = aset.agents
    self.prev_agents = self.get_defaults_agents()
    self.prev_robots = self.get_defaults_robots()
    self.time = 0
    self.count = 0


  def print_grid(self):
    self.grid.print_grid()

  def reset_grid(self):
    for pos in self.prev_agents:
      xy = pos[1]
      self.grid.update_grid(xy[0],xy[1],pos[0])
    for pos in self.prev_robots:
      xy = pos[1]
      self.grid.update_grid(xy[0],xy[1],pos[0])
    #self.prev_agents = []
    #self.prev_robots = []


  def get_defaults_agents(self):
    prev_agents = []
    if self.agents:
      for a in self.agents:
        for p in a.positions:
          prev_agents.append((self.grid.get_val(p[0],p[1]),p))
    return prev_agents

  def get_defaults_robots(self):
    prev_robots = []
    if self.robots:
      for r in self.robots:
        prev_robots.append((self.grid.get_val(r.curr[0],r.curr[1]),r.curr))
    return prev_robots

  def init_agents(self):
    for a in self.agents:
      curr_pos = a.ordered[a.curr][1]
      self.prev_agents.append((self.grid.get_val(curr_pos[0],curr_pos[1]),curr_pos))
      self.grid.update_grid(curr_pos[0],curr_pos[1],a.id)
      #a.agent_move()
      #print(a.id,'-',curr_pos)
    #self.grid.print_grid()

  def init_robots(self):
    for r in self.robots:
      curr_pos = r.curr
      self.prev_robots.append((self.grid.get_val(curr_pos[0],curr_pos[1]),curr_pos))
      if self.grid.get_val(curr_pos[0],curr_pos[1]) == 'X':
        r.path_found = True
      if self.grid.get_val(r.end[0],r.end[1]) == 'X':
        r.path_found = True
      self.grid.update_grid(curr_pos[0],curr_pos[1],r.id)
      #print(r.id,'-',curr_pos)
    #self.grid.print_grid()

  def move_agents(self):
    #print("Moving Agents")
    for a in self.agents:
      a.agent_move()
      curr_pos = a.curr_pos[1]
      self.grid.update_grid(curr_pos[0],curr_pos[1],a.id)
    #self.grid.print_grid()
    #self.reset_grid()
    #self.grid.print_grid()

  def move_robots(self):
    #print("Moving Robots")
    robot_moves = [] #[ (x,y) , .... ]
    for r in self.robots:
      if r.path_found == False:
        surrounding = self.grid.get_surrounding_stats(r.curr[0],r.curr[1],r)
        h_val = math.inf
        final_move = None
        for s in surrounding:
          H = r.h(s[0],s[1])
          if H < h_val:
            h_val = H
            final_move = s

        #print(final_move)
        if final_move is not None:
          if final_move not in r.percept_sequence:
            r.move_robot(final_move)
          else:
            for i in range(len(self.prev_robots)):
              if self.prev_robots[i][1] == r.curr:
                self.prev_robots.pop(i)
                break  # Exit loop after removing
            r.move_robot_back()

        else:
          for i in range(len(self.prev_robots)):
              if self.prev_robots[i][1] == r.curr:
                self.prev_robots.pop(i)
                break  # Exit loop after removing
          r.move_robot_back()

        self.prev_robots.append((self.grid.get_val(r.curr[0],r.curr[1]),r.curr))
        self.grid.update_grid(r.curr[0],r.curr[1],r.id)

        if r.path_found:
          self.count += 1
          #self.prev_robots.remove((self.grid.get_val(r.curr[0],r.curr[1]),r.curr))
          #for i in range(len(self.prev_robots)):
            #if self.prev_robots[i][1] == r.curr:
              #self.prev_robots.pop(i)
              #break  # Exit loop after removing
          #self.robots.remove(r)

        #print(r.id,'-',r.curr)
      #self.grid.print_grid()
      #self.reset_grid()


  def start(self):
    self.init_agents()
    self.init_robots()
    #self.grid.print_grid()
    pass

  def run(self):
    time_out  = self.grid.n*self.grid.m
    max_itr = 10000
    time_spent = 0
    if time_out <= 250 :
      time_out*=time_out
    #print(len(self.robots))
    while(self.count < len(self.robots) and time_spent <= max_itr ):
    #while(self.time < 11):
      #self.print_grid()
      #print("time = ",self.time)
      self.move_agents()
      self.move_robots()
      #print('>>>>>>')
      #self.print_grid()
      #print('<<<<<<')
      self.reset_grid()
      self.time+=1
      time_spent+=1
      #print(time_spent)

    for r in self.robots:
      print("Robot ",r.id[1]," Path: ", end='')
      r.print_sequence()
      print("Robot ",r.id[1]," ", end='')
      r.print_time()
      #r.robot_stats()

    pass

##################################### MAIN #####################################

# Example usage:
# EDIT THIS DRIVER TO RUN CODE ON SPECIFIC FILES!!!!
#folder = 'Data'
#filename = '/data1.txt'
#file_path = os.path.join(folder, filename)
myGrid = GRID("Data/data0.txt")
#myGrid.print_grid() #testing value setup
#folder = 'Data'
#filename = "/Robots1.txt"
#file_path = os.path.join(folder, filename)
myRobots = Rset("Data/Robots0.txt")
#myRobots.rset_stats() #testing value setup
#folder = 'Data'
#filename = "/Agent1.txt"
#file_path = os.path.join(folder, filename)
myAgents = Aset("Data/Agent0.txt")
#myAgents.agent_paths() #testing value setup
#myAgents.Aset_stats() #testing value setup
mySimulator = SIMULATOR(myGrid,myRobots,myAgents)

#myGrid.print_grid()
#print('-------')
mySimulator.start()
#print('********')
#myGrid.print_grid()
mySimulator.run()

