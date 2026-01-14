# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 09:49:31 2013

@author: Byron
"""

# Door Maze Builder version 3.2: redesigned code with fewer classes
# build_maze32.py


import sys
#import shelve
import pickle
from PyQt5 import QtWidgets
from maze_builder4 import Ui_Form
import random

def create_room(location, room_id):
    return Room(location, room_id)
    
def create_maze(dimensions):
    return Maze(dimensions)
    
def display_maze(maze):
    lines = []
    disp_rooms = []
    flr = maze.get_current_flr()
    f = flr - 1
    (flrs, rows, cols) = maze.get_dimensions()
    for r in range(rows):
        line_sections1 = []
        line_sections2 = []
        line_sections3 = []
        line_sections4 = []
        for c in range(cols):
            location = (f, r, c)
            room = maze.get_room2(location)
            room_lines = []
            doors = room.get_doors()
            disp_str = room.get_disp_str()
            if 'N' in doors:
                door = doors['N']
                if door['locked']:
                    line1 = ' __@__'
                else:
                    line1 = ' __/__'
            else:
                line1 = ' _____'
            room_lines.append(line1)
            line_sections1.append(line1)
            line2 = '|     '
            room_lines.append(line2)
            line_sections2.append(line2)
            if 'W' in doors:
                door = doors['W']
                if door['locked']:
                    line3 = '@' + disp_str + ' '
                else:
                    line3 = "'" + disp_str + ' '
            else:
                line3 = '|' + disp_str + ' '
            room_lines.append(line3)
            line_sections3.append(line3)
            line4 = line2
            room_lines.append(line4)
            line_sections4.append(line4)
            disp_rooms.append(room_lines)
        lineStr1 = ''.join(line_sections1)
        lineStr2 = ''.join(line_sections2)
        lineStr3 = ''.join(line_sections3)
        lineStr4 = ''.join(line_sections4)
        lines.append(lineStr1 + ' ')
        lines.append(lineStr2 + '|')
        lines.append(lineStr3 + '|')
        lines.append(lineStr4 + '|')
    n=6*cols-1
    lines.append(' '+'_'*n+' ')
    return lines

class Room():
    """A room within the maze.  Can contain doors, ramps, and levers."""
    def __init__(self, location, room_id):
        self.location = location
        self.room_id = room_id
        self.clear()
        
    def clear(self):
        self.doors = {}
        self.ramp = None
        self.lever = None
        self.properties = {}
    
    def set_property(self, name, value):
        self.properties[name] = value
        
    def add_door(self, door_loc):
        door = {}
        is_locked = False
        assigned_lever = None
        room1_loc = self.location
        (f, r, c) = room1_loc
        if door_loc == 'N':
            room2_loc = (f, r - 1, c)
        elif door_loc == 'W':
            room2_loc = (f, r, c - 1)
        elif door_loc == 'E':
            room2_loc = (f, r, c + 1)
        elif door_loc == 'S':
            room2_loc = (f, r + 1, c)
        else:
            room2_loc = None
        # set values
        door['locked'] = is_locked
        door['lever'] = assigned_lever
        door['rooms'] = (room1_loc, room2_loc)
        self.doors[door_loc] = door
    
    def add_ramp(self):
        room1_loc = self.location
        (f, r, c) = room1_loc
        if f == 0:
            room2_loc = (1, r, c)
        elif f == 1:
            room2_loc = (0, r, c)
        else:
            room2_loc = None
        self.ramp = (room1_loc, room2_loc)
        
    def add_lever(self, lever_id):
        lever = {}
        room_found_loc = self.location
        room_ctrl_loc = (None, None)
        door_loc = (None, None)
        # set_values
        lever['room_found'] = room_found_loc
        lever['room_ctrl'] = room_ctrl_loc
        lever['door_loc'] = door_loc
        lever['id'] = lever_id
        self.lever = lever
        
    def get_disp_str(self):
        props = self.properties
        is_start = False
        is_finish = False
        current_room = False
        if 'start' in props:
            if props['start']:
                is_start = True
        elif 'finish' in props:
            if props['finish']:
                is_finish = True
        else:
            pass
        if 'active' in props:
            if props['active']:
                current_room = True
        if self.room_id < 10:
            id_str = '0' + str(self.room_id)
        else:
            id_str = str(self.room_id)
        if self.ramp:
            spec = 'r'
        elif is_start:
            spec = 's'
        elif is_finish:
            spec = 'f'
        elif self.lever:
            spec = 'k'
        else:
            spec = 'a'
        if current_room:
            disp_str = '*' + id_str + spec
        else:
            disp_str = ' ' + id_str + spec
        return disp_str
        
    def get_location(self):
        return self.location
        
    def get_room_id(self):
        return self.room_id
        
    def get_doors(self):
        return self.doors
        
    def get_ramp(self):
        return self.ramp
        
    def get_lever(self):
        return self.lever
        
    def get_property(self, name):
        return self.properties[name]
        
    def get_properties(self):
        return self.properties
        
    def set_lever(self, lever):
        self.lever = lever
        
    def set_door(self, door_loc, door):
        self.doors[door_loc] = door
        
#    def use_ramp(self):
#        ramp = self.ramp
#        if ramp:
#            room2_loc = ramp[1]
#            return room2_loc
#        else:
#            return None

class Maze():
    """A maze of rooms"""
    def __init__(self, dimensions):
        self.rooms = []
        self.rooms_list = []
        self.start_room = None
        self.finish_room = None
        self.dimensions = dimensions
        self.current_loc = (0, 0, 0)
        self.current_flr = 1
        self.active_lever = None
        self.current_lever_id = 0
    
    def build(self):
        (flrs, rows, cols) = self.dimensions
        rooms = []
        rooms_list = []
        room_id = 1
        for f in range(flrs):
            flr_rooms = []
            for r in range(rows):
                row_rooms = []
                for c in range(cols):
                    location = (f, r, c)
                    room = create_room(location, room_id)
                    row_rooms.append(room)
                    rooms_list.append(room)
                    room_id += 1
                flr_rooms.append(row_rooms)
            rooms.append(flr_rooms)
        self.rooms = rooms
        self.rooms_list = rooms_list
        
    def reset(self):
        current_room = self.get_current_room()
        current_room.set_property('active', True)
        
    def get_dimensions(self):
        return self.dimensions
        
    def set_clues(self):
        roomsyms = ['!', '@', '#', '$', '%', '^', '&', '*', '+']
        alphStr = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
        alphs = alphStr.split(' ')
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        for room in self.rooms_list:
            sym_i = random.randrange(0, len(roomsyms))
            rsym = roomsyms[sym_i]
            alph_i = random.randrange(0, len(alphs))
            ralph = alphs[alph_i]
            num_i = random.randrange(0, len(nums))
            rnum = nums[num_i]
            clues = (rsym, ralph, rnum)
            room.set_property('code', clues)
            
    def get_clues(self):
        current_room = self.get_current_room()
        clues = current_room.get_property('code')
        return clues
        
    def get_room1(self, room_id):
        return self.rooms_list[room_id - 1]
        
    def get_room2(self, location):
        (f, r, c) = location
        return self.rooms[f][r][c]
        
    def get_border_room(self, direction):
        (f1, r1, c1) = self.current_loc
        if direction == 'N':
            next_loc = (f1, r1 - 1, c1)
        elif direction == 'W':
            next_loc = (f1, r1, c1 - 1)
        elif direction == 'E':
            next_loc = (f1, r1, c1 + 1)
        elif direction == 'S':
            next_loc = (f1, r1 + 1, c1)
        elif direction == 'U':
            next_loc = (f1 + 1, r1, c1)
        elif direction == 'D':
            next_loc = (f1 - 1, r1, c1)
        else:
            return None
        try:
            next_room = self.get_room2(next_loc)
            return next_room
        except IndexError:
            return None
        
    def get_current_flr(self):
        return self.current_flr
        
    def go_to_start(self):
        start_room = self.start_room
        location = start_room.get_location()
        self.current_loc = location
        
    def get_current_room(self):
        return self.get_room2(self.current_loc)
        
    def get_lever_id(self):
        return self.current_lever_id
        
    def next_room(self, direction):
        (f1, r1, c1) = self.current_loc
        current_room = self.get_current_room()
        if direction == 'N':
            next_loc = (f1, r1 - 1, c1)
        elif direction == 'W':
            next_loc = (f1, r1, c1 - 1)
        elif direction == 'E':
            next_loc = (f1, r1, c1 + 1)
        elif direction == 'S':
            next_loc = (f1, r1 + 1, c1)
        else:
            next_loc = self.current_loc
        try:
            next_room = self.get_room2(next_loc)
            current_room.set_property('active', False)
            next_room.set_property('active', True)
            self.current_loc = next_loc
            return next_room
        except IndexError:
            same_room = self.get_current_room()
            return same_room
            
    def change_floor(self):
        (f1, r1, c1) = self.current_loc
        current_room = self.get_current_room()
        if self.current_flr == 1:
            f2 = 1
            next_loc = (f2, r1, c1)
        elif self.current_flr == 2:
            f2 = 0
            next_loc = (f2, r1, c1)
        else:
            f2 = 0
            next_loc = self.current_loc
        try:
            next_room = self.get_room2(next_loc)
            current_room.set_property('active', False)
            next_room.set_property('active', True)
            self.current_flr = f2 + 1
            self.current_loc = next_loc
            return next_room
        except IndexError:
            same_room = self.get_current_room()
            return same_room
            
    def set_start(self):
        old_start = self.start_room
        start_room = self.get_current_room()
        start_room.set_property('start', True)
        if old_start:
            old_start.set_property('start', False)
        self.start_room = start_room
    
    def set_finish(self):
        old_finish = self.finish_room
        finish_room = self.get_current_room()
        finish_room.set_property('finish', True)
        if old_finish:
            old_finish.set_property('finish', False)
        self.finish_room = finish_room
        
    def place_door(self, door_loc):
        current_room = self.get_current_room()
        border_room = self.get_border_room(door_loc)
        if border_room:
            current_room.add_door(door_loc)
            if door_loc == 'N':
                door_loc2 = 'S'
            elif door_loc == 'S':
                door_loc2 = 'N'
            elif door_loc == 'W':
                door_loc2 = 'E'
            else:
                door_loc2 = 'W'
            border_room.add_door(door_loc2)
        else:
            pass
        
    def place_ramp(self):
        current_room = self.get_current_room()
        current_room.add_ramp()
        if self.current_flr == 1:
            border_room = self.get_border_room('U')
        else:
            border_room = self.get_border_room('D')
        border_room.add_ramp()
        
    def place_lever(self):
        current_room = self.get_current_room()
        lever_id = self.current_lever_id
        current_room.add_lever(lever_id)
        self.current_lever_id += 1
        return current_room
        
    def assign_lever(self, src_room, door_loc):
        lever = src_room.get_lever()
        current_room = self.get_current_room()
        room1_loc = current_room.get_location()
        room2 = self.get_border_room(door_loc)
        room2_loc = room2.get_location()
        lever['room_ctrl'] = (room1_loc, room2_loc)
        swap_dict = {'N':'S', 'W':'E', 'S':'N', 'E':'W'}
        door_loc1 = door_loc
        door_loc2 = swap_dict[door_loc]
        lever['door_loc'] = (door_loc1, door_loc2)
        src_room.set_lever(lever)
        doors = current_room.get_doors()
        door1 = doors[door_loc1]
        door1['locked'] = True
        current_room.set_door(door_loc, door1)
        border_room = room2
        doors = border_room.get_doors()
        door2 = doors[door_loc2]
        door2['locked'] = True
        border_room.set_door(door_loc2, door2)
        
class MyForm(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.currentDir = sys.path[0]
        # Connections go here
        self.ui.pushButton_12.clicked.connect(self.build_maze)
        self.ui.pushButton_13.clicked.connect(self.clear)
        self.ui.pushButton.clicked.connect(self.north)
        self.ui.pushButton_4.clicked.connect(self.south)
        self.ui.pushButton_3.clicked.connect(self.east)
        self.ui.pushButton_2.clicked.connect(self.west)
        self.ui.pushButton_9.clicked.connect(self.northD)
        self.ui.pushButton_18.clicked.connect(self.southD)
        self.ui.pushButton_6.clicked.connect(self.eastD)
        self.ui.pushButton_17.clicked.connect(self.westD)
        self.ui.pushButton_5.clicked.connect(self.place_lever)
        self.ui.pushButton_10.clicked.connect(self.set_start)
        self.ui.pushButton_11.clicked.connect(self.set_finish)
        self.ui.pushButton_14.clicked.connect(self.load)
        self.ui.pushButton_15.clicked.connect(self.save)
        self.ui.comboBox_4.currentIndexChanged.connect(self.change_floor)
        self.ui.pushButton_7.clicked.connect(self.place_ramp)
        self.ui.pushButton_20.clicked.connect(self.toggle_floors)
        
#        QtCore.QObject.connect(self.ui.pushButton_12, QtCore.SIGNAL("clicked()"), self.build_maze )
#        QtCore.QObject.connect(self.ui.pushButton_13, QtCore.SIGNAL("clicked()"), self.clear )
#        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.north )
#        QtCore.QObject.connect(self.ui.pushButton_4, QtCore.SIGNAL("clicked()"), self.south )
#        QtCore.QObject.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), self.east )
#        QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.west )
#        QtCore.QObject.connect(self.ui.pushButton_9, QtCore.SIGNAL("clicked()"), self.northD )
#        QtCore.QObject.connect(self.ui.pushButton_18, QtCore.SIGNAL("clicked()"), self.southD )
#        QtCore.QObject.connect(self.ui.pushButton_6, QtCore.SIGNAL("clicked()"), self.eastD )
#        QtCore.QObject.connect(self.ui.pushButton_17, QtCore.SIGNAL("clicked()"), self.westD )
#        QtCore.QObject.connect(self.ui.pushButton_5, QtCore.SIGNAL("clicked()"), self.place_lever )
#        QtCore.QObject.connect(self.ui.pushButton_10, QtCore.SIGNAL("clicked()"), self.set_start )
#        QtCore.QObject.connect(self.ui.pushButton_11, QtCore.SIGNAL("clicked()"), self.set_finish )
#        QtCore.QObject.connect(self.ui.pushButton_14, QtCore.SIGNAL("clicked()"), self.load )
#        QtCore.QObject.connect(self.ui.pushButton_15, QtCore.SIGNAL("clicked()"), self.save )
#        QtCore.QObject.connect(self.ui.comboBox_4, QtCore.SIGNAL("currentIndexChanged(int)"), self.change_floor )
#        QtCore.QObject.connect(self.ui.pushButton_7, QtCore.SIGNAL("clicked()"), self.place_ramp )
#        QtCore.QObject.connect(self.ui.pushButton_20, QtCore.SIGNAL("clicked()"), self.toggle_floors )
        
        self.ui.plainTextEdit.setReadOnly(True)
        self.clear()
        
    def clear(self):
        self.maze = None
        self.active_lever_src = None
        self.ui.plainTextEdit.clear()
        self.ui.comboBox_4.clear()
        
    
    def build_maze(self):
        if not self.maze:
            floors=int(self.ui.comboBox.currentText())
            rows=int(self.ui.comboBox_2.currentText())
            cols=int(self.ui.comboBox_3.currentText())
            dims=(floors, rows, cols)
            combo_flrs = []
            self.ui.comboBox_4.clear()
            for f in range(floors):
                combo_flrs.append(str(f+1))
            self.ui.comboBox_4.addItems(combo_flrs)
            self.ui.comboBox_4.setCurrentIndex(0)
            self.maze = create_maze(dims)
            self.maze.build()
            self.maze.reset()
            self.update_disp()
        else:
            pass
        
    def load(self):
        filename, ext1 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Maze', self.currentDir, '*.mz')
        if filename:
            with open(filename, mode='rb') as f1:
                maze = pickle.load(f1)
#            d = shelve.open(filename[:-4])
#            try:
#                maze = d['maze']
            if maze:
                self.maze = maze
                dims = self.maze.get_dimensions()
                num_floors = dims[0]
                combo_flrs = []
                for f in range(num_floors):
                    combo_flrs.append(str(f + 1))
                self.ui.comboBox_4.addItems(combo_flrs)
                self.ui.comboBox_4.setCurrentIndex(0)
            else:
                pass
#            d.close()
            self.update_disp()
#            except KeyError:
#                d.close()
        else:
            pass
        
    def save(self):
        filename, ext1 = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Maze', self.currentDir, '*.mz')
        if filename:
            with open(filename, mode='wb') as f1:
                pickle.dump(self.maze, f1)
#            d = shelve.open(filename)
#            try:
#                d['maze'] = self.maze
#                d.sync()
#                d.close()
#            except KeyError:
#                d.close()
        else:
            pass
        
    def update_disp(self):
        lines = display_maze(self.maze)
        disp_text='\n'.join(lines)
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(disp_text)
        
    def set_start(self):
        if self.maze:
            self.maze.set_start()
            self.update_disp()
        else:
            pass
    
    def set_finish(self):
        if self.maze:
            self.maze.set_finish()
            self.update_disp()
        else:
            pass
    
    def navigate(self, direction):
        if self.maze:
            self.maze.next_room(direction)
            self.update_disp()
        else:
            pass
    
    def change_floor(self):
        if self.maze:
            new_flr=int(self.ui.comboBox_4.currentText())
            if not new_flr==self.maze.get_current_flr():
                self.maze.change_floor()
                self.update_disp()
            else:
                pass
        else:
            pass
        
    def toggle_floors(self):
        if self.maze:
            self.maze.change_floor()
            new_flr = self.maze.get_current_flr()
            self.ui.comboBox_4.setCurrentIndex(new_flr - 1)
            self.update_disp()
        else:
            pass
        
    def place_door(self, loc):
        if self.maze:
            self.maze.place_door(loc)
            self.update_disp()
        else:
            pass
        
    def place_ramp(self):
        if self.maze:
            self.maze.place_ramp()
            self.update_disp()
        else:
            pass
        
    def place_lever(self):
        if self.maze:
            src_room = self.maze.place_lever()
            self.active_lever_src = src_room
            l_id = self.maze.get_lever_id()
            self.ui.lcdNumber.display(l_id)
            self.update_disp()
        else:
            pass
        
    def assign_lever(self, loc):
        if self.maze:
            src_room = self.active_lever_src
            if src_room:
                self.maze.assign_lever(src_room, loc)
                self.active_lever_src = None
                self.ui.lcdNumber.display(0)
                self.update_disp()
            else:
                pass
        else:
            pass
    
    def north(self):
        self.navigate('N')
    
    def south(self):
        self.navigate('S')
            
    def east(self):
        self.navigate('E')
            
    def west(self):
        self.navigate('W')
        
    def northD(self):
        room = self.maze.get_current_room()
        doors = room.get_doors()
        if 'N' in doors:
            self.assign_lever('N')
        else:
            self.place_door('N')
        
    def southD(self):
        room = self.maze.get_current_room()
        doors = room.get_doors()
        if 'S' in doors:
            self.assign_lever('S')
        else:
            self.place_door('S')
        
    def eastD(self):
        room = self.maze.get_current_room()
        doors = room.get_doors()
        if 'E' in doors:
            self.assign_lever('E')
        else:
            self.place_door('E')
        
    def westD(self):
        room = self.maze.get_current_room()
        doors = room.get_doors()
        if 'W' in doors:
            self.assign_lever('W')
        else:
            self.place_door('W')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    app.exec()
