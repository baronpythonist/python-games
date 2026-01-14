# Door Maze Game
# Wrapper for 'maze_game.py'

# Byron Burks

import sys
import os
#import shelve
import pickle
from PyQt5 import QtCore, QtGui, QtWidgets
from maze_game4 import Ui_Form
import re

#from build_maze2 import Door, Elevator, Room_key, Room, Maze
from build_maze4 import Room, Maze

def load_maze(filename, name):
    with open(filename, 'rb') as f1:
        maze = pickle.load(f1)
    return maze
#    d=shelve.open(str(filename[:-4]))
#    try:
#        maze=d[name]
#        d.close()
#        return maze
#    except KeyError:
#        d.close()
#        return None
        
class Game():
    """ Allows you to play the maze """
    def __init__(self, maze):
        self.maze = maze
        self.clear()
        
    def clear(self):
        self.maze.go_to_start()
        self.levers = {}
        
    def get_current_room(self):
        return self.maze.get_current_room()
        
    def get_cheats(self, name):
        if name == 'code':
            return self.maze.get_clues()
        else:
            return None
        
    def is_finished(self):
        current_room = self.maze.get_current_room()
        props = current_room.get_properties()
        if 'finish' in props:
            return props['finish']
        else:
            return False
    
    def move(self, direction):
        current_room = self.maze.get_current_room()
        doors = current_room.get_doors()
        door1 = doors[direction]
        not_locked = False
        if not door1['locked']:
            not_locked = True
            self.maze.next_room(direction)
        else:
            pass
        return not_locked
        
    def use_ramp(self):
        current_room = self.maze.get_current_room()
        if current_room.get_ramp():
            has_ramp = True
            self.maze.change_floor()
        else:
            has_ramp = False
        return has_ramp
        
    def search_for_levers(self):
        current_room = self.maze.get_current_room()
        new_lever = current_room.get_lever()
        if new_lever:
            lever_id = new_lever['id']
            self.levers[lever_id]=new_lever
        else:
            pass
        return new_lever
    
    def unlock_door(self, lever_id):
        lever = self.levers[lever_id]
        (room1_loc, room2_loc) = lever['room_ctrl']
        (door1_loc, door2_loc) = lever['door_loc']
        room1_ctrl = self.maze.get_room2(room1_loc)
        doors = room1_ctrl.get_doors()
        door1 = doors[door1_loc]
        door1['locked'] = False
        room1_ctrl.set_door(door1_loc, door1)
        room2_ctrl = self.maze.get_room2(room2_loc)
        doors = room2_ctrl.get_doors()
        door2 = doors[door2_loc]
        door2['locked'] = False
        room2_ctrl.set_door(door2_loc, door2)

class MyForm(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.currentDir = self.getDir()
        
        self.ui.pushButton_6.clicked.connect(self.clear)
        self.ui.pushButton_5.clicked.connect(self.load)
        self.ui.pushButton.clicked.connect(self.north)
        self.ui.pushButton_4.clicked.connect(self.south)
        self.ui.pushButton_2.clicked.connect(self.east)
        self.ui.pushButton_3.clicked.connect(self.west)
        self.ui.pushButton_7.clicked.connect(self.search)
        self.ui.pushButton_8.clicked.connect(self.op_ramp)
        self.ui.lineEdit.textChanged.connect(self.disp_cheats)
        
#        QtCore.QObject.connect(self.ui.pushButton_6, QtCore.SIGNAL("clicked()"), self.clear )
#        QtCore.QObject.connect(self.ui.pushButton_5, QtCore.SIGNAL("clicked()"), self.load )
#        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.north )
#        QtCore.QObject.connect(self.ui.pushButton_4, QtCore.SIGNAL("clicked()"), self.south )
#        QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.east )
#        QtCore.QObject.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), self.west )
#        QtCore.QObject.connect(self.ui.pushButton_7, QtCore.SIGNAL("clicked()"), self.search )
#        QtCore.QObject.connect(self.ui.pushButton_8, QtCore.SIGNAL("clicked()"), self.op_ramp )
#        QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL("textChanged(QString)"), self.disp_cheats )
        
        self.clear()
        
    def clear(self):
#        self.game_display=None
        self.image_names = {'room':'door_maze_room3.png', 
                            'room2':'door_maze_room4.png',
                            'west':'door_west2b.png', 
                            'east':'door_east2b.png', 'north':'door_north2b.png',
                            'south':'door_south2b.png', 'ramp':'maze_ramp1.png',
                            'mouse_image':'mouse_image2b.png',
                            'closed_west':'door_closed_w2b.png', 
                            'closed_east':'door_closed_e2b.png',
                            'closed_north':'door_closed_n2b.png',
                            'closed_south':'door_closed_s2b.png',
                            'final_room':'door_maze_win1.png'}
        self.generate_px()
        self.game = None
        self.levers = {}
        self.mouse_pos = 'S'
        self.ui.label_2.clear()
        self.ui.label_3.clear()
        self.ui.label_4.clear()
        self.ui.label_5.clear()
        self.ui.label_6.clear()
        self.ui.label_7.clear()
        self.ui.label_8.clear()
        self.ui.label_9.clear()
        self.ui.label_10.clear()
        self.ui.label_11.clear()
#        self.ui.plainTextEdit.clear()
#        self.ui.plainTextEdit_2.clear()
#        self.ui.comboBox.clear()
#        self.add_to_combo('None')
        self.ui.textEdit.clear()
        self.ui.textEdit.setText('Welcome!')
        
#    def add_to_combo(self, item):
#        self.ui.comboBox.addItem(item)

    def getDir(self):
        currentDirRaw = sys.path[0]
        dirParts = currentDirRaw.split('\\')
        if dirParts[-1] == 'library.zip':
            currentDir = '\\'.join(dirParts[:-1])
        else:
            currentDir = currentDirRaw
        os.chdir(currentDir)
        return currentDir
        
    def load(self):
        filename, ext1 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Maze', self.currentDir, '*.mz')
        if filename:
            maze = load_maze(filename, 'maze')
            if maze:
                self.clear()
#                self.game_display=Game_disp(maze)
                self.game = Game(maze)
                maze.reset()
                maze.set_clues()
                self.update_room_disp(None)
            else:
                pass
        else:
            pass
            
#    def update_room_disp2(self):
#        self.game_display.update_room_lines()
#        room_lines=self.game_display.get_lines()
#        disp_text='\n'.join(room_lines)
#        self.ui.plainTextEdit.clear()
#        self.ui.plainTextEdit.setPlainText(disp_text)
        
    def generate_px(self):
        try:
            self.room_px = QtGui.QPixmap(self.image_names['room'])
            self.room2_px = QtGui.QPixmap(self.image_names['room2'])
            self.mouse_px = QtGui.QPixmap(self.image_names['mouse_image'])
            self.west_px = QtGui.QPixmap(self.image_names['west'])
            self.east_px = QtGui.QPixmap(self.image_names['east'])
            self.north_px = QtGui.QPixmap(self.image_names['north'])
            self.south_px = QtGui.QPixmap(self.image_names['south'])
            self.wclosed_px = QtGui.QPixmap(self.image_names['closed_west'])
            self.eclosed_px = QtGui.QPixmap(self.image_names['closed_east'])
            self.nclosed_px = QtGui.QPixmap(self.image_names['closed_north'])
            self.sclosed_px = QtGui.QPixmap(self.image_names['closed_south'])
            self.ramp_px = QtGui.QPixmap(self.image_names['ramp'])
            self.win_px = QtGui.QPixmap(self.image_names['final_room'])
        except WindowsError:
            self.room_px = None
            self.room2_px = None
            self.mouse_px = None
            self.west_px = None
            self.east_px = None
            self.north_px = None
            self.south_px = None
            self.wclosed_px = None
            self.eclosed_px = None
            self.nclosed_px = None
            self.sclosed_px = None
            self.ramp_px = None
            self.win_px = None
            message='Could not find the images!'
            self.ui.textEdit.clear()
            self.ui.textEdit.setText(message)
        
    def update_room_disp(self, direction):
        self.ui.label_2.clear()
        self.ui.label_3.clear()
        self.ui.label_4.clear()
        self.ui.label_5.clear()
        self.ui.label_6.clear()
        self.ui.label_7.clear()
        self.ui.label_8.clear()
        self.ui.label_9.clear()
        self.ui.label_10.clear()
        self.ui.label_11.clear()
        self.disp_cheats()
        room = self.game.get_current_room()
        floor = self.game.maze.get_current_flr()
        doors = room.get_doors()
        ramp = room.get_ramp()
#        swap_pos = {'N':'S', 'W':'E', 'S':'N', 'E':'W'}
        props = room.get_properties()
        if 'finish' in props:
            is_finish = props['finish']
        else:
            is_finish = False
        if not is_finish:
            if floor == 1:
                self.ui.label_2.setPixmap(self.room_px)
            elif floor == 2:
                self.ui.label_2.setPixmap(self.room2_px)
            else:
                self.ui.label_2.setPixmap(self.room_px)
            old_pos = self.mouse_pos
            if not direction == None:
                new_pos = direction
#                new_pos = swap_pos[direction]
            else:
                new_pos = old_pos
            self.mouse_pos = new_pos
            if new_pos == 'N':
                self.ui.label_9.setPixmap(self.mouse_px)
            elif new_pos == 'W':
                self.ui.label_11.setPixmap(self.mouse_px)
            elif new_pos == 'E':
                self.ui.label_10.setPixmap(self.mouse_px)
            elif new_pos == 'S':
                self.ui.label_8.setPixmap(self.mouse_px)
            else:
                pass
        else:
            self.ui.label_2.setPixmap(self.win_px)
        if True:
#        if not room.finish:
            if 'N' in doors:
                door1 = doors['N']
                if door1['locked']:
                    self.ui.label_4.setPixmap(self.nclosed_px)
                else:
                    self.ui.label_4.setPixmap(self.north_px)
            else:
                pass
            if ramp:
                self.ui.label_7.setPixmap(self.ramp_px)
            else:
                pass
            if 'W' in doors:
                door2 = doors['W']
                if door2['locked']:
                    self.ui.label_3.setPixmap(self.wclosed_px)
                else:
                    self.ui.label_3.setPixmap(self.west_px)
            else:
                pass
            if 'E' in doors:
                door3 = doors['E']
                if door3['locked']:
                    self.ui.label_6.setPixmap(self.eclosed_px)
                else:
                    self.ui.label_6.setPixmap(self.east_px)
            else:
                pass
            if 'S' in doors:
                door4 = doors['S']
                if door4['locked']:
                    self.ui.label_5.setPixmap(self.sclosed_px)
                else:
                    self.ui.label_5.setPixmap(self.south_px)
            else:
                pass
        else:
            pass
        
    def disp_cheats(self):
        chStr = str(self.ui.lineEdit.text())
        if re.search('(mouse|mice)', chStr.lower()):
            # display location code
            room_clues = self.game.get_cheats('code')
            (roomSym1, roomAlph1, roomNum1) = room_clues
            message = 'location:\n{0:d}\n{sym1}\n{alph1}\n'.format(roomNum1, sym1=roomSym1, alph1=roomAlph1)
            self.ui.textEdit_2.clear()
            self.ui.textEdit_2.setText(message)
        elif re.search('(cheese)', chStr.lower()):
            # will display an arrow to show which way to go
            self.ui.textEdit_2.clear()
        else:
            self.ui.textEdit_2.clear()
        
    def navigate(self, direction):
        try:
            not_locked=self.game.move(direction)
            if not_locked:
                pass
            else:
                message='Door locked!'
                self.ui.textEdit.clear()
                self.ui.textEdit.setText(message)
        except KeyError:
            message='Blocked!'
            self.ui.textEdit.clear()
            self.ui.textEdit.setText(message)
        self.update_room_disp(direction)
        if self.game.is_finished():
            message='Thanks For Playing!\n\t=)'
            self.ui.textEdit.clear()
            self.ui.textEdit.setText(message)
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
        
    def op_ramp(self):
        has_ramp = self.game.use_ramp()
        if has_ramp:
            self.update_room_disp(None)
            new_floor=self.game.maze.get_current_flr()
            message='Floor no. ' + str(new_floor)
            self.ui.textEdit.clear()
            self.ui.textEdit.setText(message)
            if self.game.is_finished():
                message='Thanks For Playing!\n\t=)'
                self.ui.textEdit.clear()
                self.ui.textEdit.setText(message)
            else:
                pass
        else:
            pass
        
    def search(self):
        lever=self.game.search_for_levers()
        if lever:
            l_id = lever['id']
            self.levers[l_id] = lever
            self.game.unlock_door(l_id)
            message='Lever Found!'
        else:
            message='No Lever Found.'
        self.ui.textEdit.clear()
        self.ui.textEdit.setText(message)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    app.exec()
