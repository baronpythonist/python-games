# -*- coding: utf-8 -*-
"""
Created on Sat Nov 09 16:45:33 2013

@author: Byron and Zachary Burks
"""


import sys
import shelve
from PyQt5 import QtGui, QtWidgets
from laser_chess4 import Ui_Form

# class Game_piece():
#     """ A piece displayed on the board """
#     def __init__(self):
#         self.current_sq = None
#         self.player = None

class MyForm(QtWidgets.QMainWindow):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.currentDir = sys.path[0]
        self.ui.pushButton_11.clicked.connect(self.setup_board)
        self.ui.pushButton.clicked.connect(self.green_up)
        self.ui.pushButton_3.clicked.connect(self.green_left)
        self.ui.pushButton_2.clicked.connect(self.green_down)
        self.ui.pushButton_4.clicked.connect(self.green_right)
        self.ui.pushButton_13.clicked.connect(self.green_r_up)
        self.ui.pushButton_10.clicked.connect(self.green_r_right)
        self.ui.pushButton_12.clicked.connect(self.green_r_left)
        self.ui.pushButton_14.clicked.connect(self.green_r_down)
        self.ui.pushButton_19.clicked.connect(self.red_up)
        self.ui.pushButton_18.clicked.connect(self.red_left)
        self.ui.pushButton_20.clicked.connect(self.red_down)
        self.ui.pushButton_21.clicked.connect(self.red_right)
        self.ui.pushButton_5.clicked.connect(self.red_r_left)
        self.ui.pushButton_9.clicked.connect(self.red_r_up)
        self.ui.pushButton_7.clicked.connect(self.red_r_down)
        self.ui.pushButton_6.clicked.connect(self.red_r_right)
        self.ui.pushButton_17.clicked.connect(self.cycle_green_next)
        self.ui.pushButton_16.clicked.connect(self.cycle_green_prev)
        self.ui.pushButton_23.clicked.connect(self.cycle_red_next)
        self.ui.pushButton_8.clicked.connect(self.cycle_red_prev)
        self.ui.comboBox.currentIndexChanged.connect(self.marker_trigger1)
        self.ui.comboBox_2.currentIndexChanged.connect(self.marker_trigger2)
        self.ui.comboBox_4.currentIndexChanged.connect(self.marker_trigger3)
        self.ui.comboBox_3.currentIndexChanged.connect(self.marker_trigger4)
        self.ui.pushButton_24.clicked.connect(self.green_undo1)
        self.ui.pushButton_25.clicked.connect(self.red_undo1)
#        self.ui.pushButton_15.clicked.connect(self.save_game)
#        self.ui.pushButton_22.clicked.connect(self.load_game)
        
#        QtCore.QObject.connect(self.ui.pushButton_11, QtCore.SIGNAL("clicked()"), self.setup_board )
#        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.green_up )
#        QtCore.QObject.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), self.green_left )
#        QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.green_down )
#        QtCore.QObject.connect(self.ui.pushButton_4, QtCore.SIGNAL("clicked()"), self.green_right )
#        QtCore.QObject.connect(self.ui.pushButton_13, QtCore.SIGNAL("clicked()"), self.green_r_up )
#        QtCore.QObject.connect(self.ui.pushButton_10, QtCore.SIGNAL("clicked()"), self.green_r_right )
#        QtCore.QObject.connect(self.ui.pushButton_12, QtCore.SIGNAL("clicked()"), self.green_r_left )
#        QtCore.QObject.connect(self.ui.pushButton_14, QtCore.SIGNAL("clicked()"), self.green_r_down )
#        QtCore.QObject.connect(self.ui.pushButton_19, QtCore.SIGNAL("clicked()"), self.red_up )
#        QtCore.QObject.connect(self.ui.pushButton_18, QtCore.SIGNAL("clicked()"), self.red_left )
#        QtCore.QObject.connect(self.ui.pushButton_20, QtCore.SIGNAL("clicked()"), self.red_down )
#        QtCore.QObject.connect(self.ui.pushButton_21, QtCore.SIGNAL("clicked()"), self.red_right )
#        QtCore.QObject.connect(self.ui.pushButton_5, QtCore.SIGNAL("clicked()"), self.red_r_left )
#        QtCore.QObject.connect(self.ui.pushButton_9, QtCore.SIGNAL("clicked()"), self.red_r_up )
#        QtCore.QObject.connect(self.ui.pushButton_7, QtCore.SIGNAL("clicked()"), self.red_r_down )
#        QtCore.QObject.connect(self.ui.pushButton_6, QtCore.SIGNAL("clicked()"), self.red_r_right )
#        QtCore.QObject.connect(self.ui.pushButton_17, QtCore.SIGNAL("clicked()"), self.cycle_green_next )
#        QtCore.QObject.connect(self.ui.pushButton_16, QtCore.SIGNAL("clicked()"), self.cycle_green_prev )
#        QtCore.QObject.connect(self.ui.pushButton_23, QtCore.SIGNAL("clicked()"), self.cycle_red_next )
#        QtCore.QObject.connect(self.ui.pushButton_8, QtCore.SIGNAL("clicked()"), self.cycle_red_prev )
#        QtCore.QObject.connect(self.ui.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.marker_trigger1 )
#        QtCore.QObject.connect(self.ui.comboBox_2, QtCore.SIGNAL("currentIndexChanged(int)"), self.marker_trigger2 )
#        QtCore.QObject.connect(self.ui.comboBox_4, QtCore.SIGNAL("currentIndexChanged(int)"), self.marker_trigger3 )
#        QtCore.QObject.connect(self.ui.comboBox_3, QtCore.SIGNAL("currentIndexChanged(int)"), self.marker_trigger4 )
#        QtCore.QObject.connect(self.ui.pushButton_24, QtCore.SIGNAL("clicked()"), self.green_undo1 )
#        QtCore.QObject.connect(self.ui.pushButton_25, QtCore.SIGNAL("clicked()"), self.red_undo1 )
#        QtCore.QObject.connect(self.ui.pushButton_15, QtCore.SIGNAL("clicked()"), self.save_game )
#        QtCore.QObject.connect(self.ui.pushButton_22, QtCore.SIGNAL("clicked()"), self.load_game )

        self.clear()
        
    def clear(self):
        self.mr_fnames = {}
        self.or_fnames = {}
        self.mr_images = {}
        self.or_images = {}
        self.image_map = {}
        self.game_pieces = {}
        self.game_pieces2 = {}
        self.active_pieces = {}
        self.active_squares = {}
        self.active_squares2 = {}
        self.selected_sq1 = None
        self.selected_sq2 = None
        self.old_pos1 = (0, 0)
        self.old_pos2 = (0, 0)
        self.new_pos1 = (0, 0)
        self.new_pos2 = (0, 0)
        self.last_rotate_dir1 = None
        self.last_rotate_dir2 = None
        # self.capt_pieces = {}
        self.laser_beams = {}
        # self.player1 = None
        # self.player2 = None
        self.bsquares = []
        self.assigned_px = {}
        self.player_turn = None
        self.player_turn2 = None
        self.load_pix()
        self.map_images()
        self.map_headers()
        self.clear_headers()
        self.reset_images()
        
    def load_pix(self):
        self.mr_fnames = {'ur_mr11':'up_right_mirror1a.png', 'dr_mr11':'down_right_mirror1a.png',
                          'ul_mr11':'up_left_mirror1a.png', 'dl_mr11':'down_left_mirror1a.png',
                          'ur_mr21':'up_right_mirror2a.png', 'dr_mr21':'down_right_mirror2a.png',
                          'ul_mr21':'up_left_mirror2a.png', 'dl_mr21':'down_left_mirror2a.png',
                          'ur_mr12':'up_right_mirror1b.png', 'dr_mr12':'down_right_mirror1b.png',
                          'ul_mr12':'up_left_mirror1b.png', 'dl_mr12':'down_left_mirror1b.png',
                          'ur_mr22':'up_right_mirror2b.png', 'dr_mr22':'down_right_mirror2b.png',
                          'ul_mr22':'up_left_mirror2b.png', 'dl_mr22':'down_left_mirror2b.png',
                          'ur_mr11s':'up_right_mirror1a_s.png', 'dr_mr11s':'down_right_mirror1a_s.png',
                          'ul_mr11s':'up_left_mirror1a_s.png', 'dl_mr11s':'down_left_mirror1a_s.png',
                          'ur_mr21s':'up_right_mirror2a_s.png', 'dr_mr21s':'down_right_mirror2a_s.png',
                          'ul_mr21s':'up_left_mirror2a_s.png', 'dl_mr21s':'down_left_mirror2a_s.png',
                          'ur_mr12s':'up_right_mirror1b_s.png', 'dr_mr12s':'down_right_mirror1b_s.png',
                          'ul_mr12s':'up_left_mirror1b_s.png', 'dl_mr12s':'down_left_mirror1b_s.png',
                          'ur_mr22s':'up_right_mirror2b_s.png', 'dr_mr22s':'down_right_mirror2b_s.png',
                          'ul_mr22s':'up_left_mirror2b_s.png', 'dl_mr22s':'down_left_mirror2b_s.png'}
        self.or_fnames = {'la_rt1':'laser_right1.png', 'la_rt2':'laser_right2.png', 'blk1':'laser_block1.png',
                          'blk1s':'laser_block1_s.png', 'blk2':'laser_block2.png', 'blk2s':'laser_block2_s.png',
                          'tgt_d1':'target_down1.png', 'tgt_u1':'target_up1.png',
                          'tgt_d2':'target_down2b.png', 'tgt_u2':'target_up2b.png', 'board':'laser_board2.png'}
        self.bm_fnames = {'bm_v1':'beam_green1.png', 'bm_h1':'beam_green2.png', 'bm_c1':'beam_green3.png',
                          'bm_v2':'beam_red1.png', 'bm_h2':'beam_red2.png', 'bm_c2':'beam_red3.png',
                          'bm_c21':'beam_red_green1.png', 'bm_c12':'beam_red_green2.png'}
        self.mr_images = {}
        for keyName, fname in self.mr_fnames.items():
            image1 = QtGui.QPixmap(fname)
            self.mr_images[keyName] = image1
        self.or_images = {}
        for keyName, fname in self.or_fnames.items():
            image2 = QtGui.QPixmap(fname)
            self.or_images[keyName] = image2
        self.bm_images = {}
        for keyName, fname in self.bm_fnames.items():
            image3 = QtGui.QPixmap(fname)
            self.bm_images[keyName] = image3
            
    def map_images(self):
        self.image_map = {'A1':self.ui.label_2, 'B1':self.ui.label_20, 'C1':self.ui.label_21,
                          'D1':self.ui.label_8, 'E1':self.ui.label_13, 'F1':self.ui.label_22,
                          'G1':self.ui.label_23, 'H1':self.ui.label_5, 'A2':self.ui.label_24,
                          'B2':self.ui.label_25, 'C2':self.ui.label_26, 'D2':self.ui.label_27,
                          'E2':self.ui.label_28, 'F2':self.ui.label_29, 'G2':self.ui.label_30,
                          'H2':self.ui.label_31, 'A3':self.ui.label_32, 'B3':self.ui.label_17,
                          'C3':self.ui.label_10, 'D3':self.ui.label_33, 'E3':self.ui.label_9,
                          'F3':self.ui.label_18, 'G3':self.ui.label_34, 'H3':self.ui.label_15,
                          'A4':self.ui.label_6, 'B4':self.ui.label_35, 'C4':self.ui.label_36,
                          'D4':self.ui.label_7, 'E4':self.ui.label_11, 'F4':self.ui.label_37,
                          'G4':self.ui.label_38, 'H4':self.ui.label_39, 'A5':self.ui.label_40,
                          'B5':self.ui.label_41, 'C5':self.ui.label_14, 'D5':self.ui.label_42,
                          'E5':self.ui.label_16, 'F5':self.ui.label_43, 'G5':self.ui.label_44,
                          'H5':self.ui.label_45, 'A6':self.ui.label_4, 'B6':self.ui.label_52,
                          'C6':self.ui.label_54, 'D6':self.ui.label_53, 'E6':self.ui.label_55,
                          'F6':self.ui.label_12, 'G6':self.ui.label_19, 'H6':self.ui.label_3}
    
    def reset_images(self):
        self.ui.label.setPixmap(self.or_images['board'])
        squares = [['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1'],
                   ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'],
                   ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3'],
                   ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4'],
                   ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5'],
                   ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6']]
        self.bsquares = squares
        for r in range(6):
            for c in range(8):
                sq1 = squares[r][c]
                lab1 = self.image_map[sq1]
                lab1.clear()
        self.image_map['A1'].setPixmap(self.or_images['la_rt1'])
        self.image_map['H1'].setPixmap(self.or_images['tgt_d1'])
        self.image_map['A6'].setPixmap(self.or_images['la_rt2'])
        self.image_map['H6'].setPixmap(self.or_images['tgt_u1'])
        self.ui.textEdit.clear()
        self.ui.textEdit.append('Green, Welcome to Laser Chess!\n')
        self.ui.textEdit_2.clear()
        self.ui.textEdit_2.append('Red, Welcome to Laser Chess!\n')

    def map_headers(self):
        self.colheaders = [self.ui.lineEdit, self.ui.lineEdit_2,
                           self.ui.lineEdit_3, self.ui.lineEdit_4,
                           self.ui.lineEdit_6, self.ui.lineEdit_5,
                           self.ui.lineEdit_8, self.ui.lineEdit_7]
        self.rowheaders = [self.ui.lineEdit_9, self.ui.lineEdit_10, self.ui.lineEdit_11,
                           self.ui.lineEdit_12, self.ui.lineEdit_13, self.ui.lineEdit_14]
        self.colhvals = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.rowhvals = ['1', '2', '3', '4', '5', '6']

    def clear_headers(self):
        for colh, valh in zip(self.colheaders, self.colhvals):
            colh.clear()
            colh.setText(valh)
        for rowh, valh in zip(self.rowheaders, self.rowhvals):
            rowh.clear()
            rowh.setText(valh)
    
    def setup_board(self):
        self.reset_images()
        self.game_pieces = {}
        self.game_pieces2 = {}
        self.active_squares = {}
        self.active_squares2 = {}
        # self.capt_pieces = {}
        self.laser_beams = {}
        self.player_turn = None
        self.player_turn2 = None
        self.old_pos1 = (0, 0)
        self.old_pos2 = (0, 0)
        self.new_pos1 = (0, 0)
        self.new_pos2 = (0, 0)
        self.last_rotate_dir1 = None
        self.last_rotate_dir2 = None
        # mirrors
        # green player
        # mirror = (id, direction, player)
        # direction: 1 = up & right, 2 = up & left, 
        # 3 = down & left, 0 = down & right
        mirror1b = ('mr', 0, 1)
        mirror1c = ('mr', 0, 1)
        mirror1d = ('mr', 3, 1)
        mirror1e = ('mr', 3, 1)
        self.game_pieces['A2'] = mirror1b
        self.game_pieces['A3'] = mirror1c
        self.game_pieces['C2'] = mirror1d
        self.game_pieces['C3'] = mirror1e
        # red player
        mirror2a = ('mr', 1, 2)
        mirror2b = ('mr', 1, 2)
        mirror2d = ('mr', 2, 2)
        mirror2e = ('mr', 2, 2)
        self.game_pieces['A4'] = mirror2a
        self.game_pieces['A5'] = mirror2b
        self.game_pieces['C4'] = mirror2d
        self.game_pieces['C5'] = mirror2e
        # blocks: green
        block1a = ('bk', 0, 1)
        # block1b = ('bk', 0, 1)
        self.game_pieces['D5'] = block1a
        # self.game_pieces['E4'] = block1b
        # red
        # block2a = ('bk', 0, 2)
        block2b = ('bk', 0, 2)
        # self.game_pieces['D3'] = block2a
        self.game_pieces['D2'] = block2b
        self.game_pieces2 = self.game_pieces.copy()
        self.display_pieces()
        self.player_turn = 'green'
        self.player_turn2 = 'green'
        self.ui.textEdit.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit.append('Green, it is your turn!\n')

    def save_game(self):
        filename=str(QtWidgets.QFileDialog.getSaveFileName(self, 'Save Game', self.currentDir, '*.lsr'))
        if filename:
            d = shelve.open(filename)
            d['game_pieces'] = self.game_pieces2
            d['turn'] = self.player_turn2
            d.sync()
            d.close()
        else:
            pass

    def load_game(self):
        filename=str(QtWidgets.QFileDialog.getOpenFileName(self, 'Load Saved Game', self.currentDir, '*.lsr'))
        if filename:
            self.reset_images()
            self.active_squares = {}
            self.active_squares2 = {}
            # self.capt_pieces = {}
            self.laser_beams = {}
            self.old_pos1 = (0, 0)
            self.old_pos2 = (0, 0)
            d = shelve.open(filename)
            try:
                self.game_pieces = d['game_pieces']
                self.player_turn = d['turn']
                d.close()
                self.game_pieces2 = self.game_pieces.copy()
                self.player_turn2 = self.player_turn
                self.update_display()
                self.ui.textEdit.clear()
                self.ui.textEdit_2.clear()
                filename2 = filename.split('/')[-1]
                loadstr = 'Game Loaded: {fname}\n'.format(fname=filename2)
                self.ui.textEdit.append(loadstr)
                self.ui.textEdit_2.append(loadstr)
                if self.player_turn2 == 'green':
                    self.ui.textEdit.append('Green, it is your turn!\n')
                else:
                    self.ui.textEdit_2.append('Red, it is your turn!\n')
            except KeyError:
                d.close()
                self.setup_board()
        else:
            pass
        
    def set_piece_image(self, loc, piece, active=False, selected1=False):
        sq1 = loc
        lab1 = self.image_map[sq1]
        (pcid, direct, player) = piece
        if pcid == 'mr':
            if not active:
                if not selected1:
                    if player == 1:
                        if direct == 1:
                            lab1.setPixmap(self.mr_images['ur_mr11'])
                        elif direct == 2:
                            lab1.setPixmap(self.mr_images['ul_mr11'])
                        elif direct == 3:
                            lab1.setPixmap(self.mr_images['dl_mr11'])
                        else:
                            lab1.setPixmap(self.mr_images['dr_mr11'])
                    else:
                        if direct == 1:
                            lab1.setPixmap(self.mr_images['ur_mr21'])
                        elif direct == 2:
                            lab1.setPixmap(self.mr_images['ul_mr21'])
                        elif direct == 3:
                            lab1.setPixmap(self.mr_images['dl_mr21'])
                        else:
                            lab1.setPixmap(self.mr_images['dr_mr21'])
                else:
                    if player == 1:
                        if direct == 1:
                            lab1.setPixmap(self.mr_images['ur_mr11s'])
                        elif direct == 2:
                            lab1.setPixmap(self.mr_images['ul_mr11s'])
                        elif direct == 3:
                            lab1.setPixmap(self.mr_images['dl_mr11s'])
                        else:
                            lab1.setPixmap(self.mr_images['dr_mr11s'])
                    else:
                        if direct == 1:
                            lab1.setPixmap(self.mr_images['ur_mr21s'])
                        elif direct == 2:
                            lab1.setPixmap(self.mr_images['ul_mr21s'])
                        elif direct == 3:
                            lab1.setPixmap(self.mr_images['dl_mr21s'])
                        else:
                            lab1.setPixmap(self.mr_images['dr_mr21s'])
            else:
                if not selected1:
                    if player == 1:
                        if direct == 1:
                            lab1.setPixmap(self.mr_images['ur_mr12'])
                        elif direct == 2:
                            lab1.setPixmap(self.mr_images['ul_mr12'])
                        elif direct == 3:
                            lab1.setPixmap(self.mr_images['dl_mr12'])
                        else:
                            lab1.setPixmap(self.mr_images['dr_mr12'])
                    else:
                        if direct == 1:
                            lab1.setPixmap(self.mr_images['ur_mr22'])
                        elif direct == 2:
                            lab1.setPixmap(self.mr_images['ul_mr22'])
                        elif direct == 3:
                            lab1.setPixmap(self.mr_images['dl_mr22'])
                        else:
                            lab1.setPixmap(self.mr_images['dr_mr22'])
                else:
                    if player == 1:
                        if direct == 1:
                            lab1.setPixmap(self.mr_images['ur_mr12s'])
                        elif direct == 2:
                            lab1.setPixmap(self.mr_images['ul_mr12s'])
                        elif direct == 3:
                            lab1.setPixmap(self.mr_images['dl_mr12s'])
                        else:
                            lab1.setPixmap(self.mr_images['dr_mr12s'])
                    else:
                        if direct == 1:
                            lab1.setPixmap(self.mr_images['ur_mr22s'])
                        elif direct == 2:
                            lab1.setPixmap(self.mr_images['ul_mr22s'])
                        elif direct == 3:
                            lab1.setPixmap(self.mr_images['dl_mr22s'])
                        else:
                            lab1.setPixmap(self.mr_images['dr_mr22s'])
        else:
            if not selected1:
                if player == 1:
                    lab1.setPixmap(self.or_images['blk1'])
                else:
                    lab1.setPixmap(self.or_images['blk2'])
            else:
                if player == 1:
                    lab1.setPixmap(self.or_images['blk1s'])
                else:
                    lab1.setPixmap(self.or_images['blk2s'])
        
    def display_pieces(self):
        for r in range(6):
            for c in range(8):
                sq1 = self.bsquares[r][c]
                if sq1 in self.game_pieces2:
                    piece1 = self.game_pieces2[sq1]
                    if sq1 in self.active_squares2:
                        if sq1 == self.selected_sq1 or sq1 == self.selected_sq2:
                            self.set_piece_image(sq1, piece1, active=True, selected1=True)
                        else:
                            self.set_piece_image(sq1, piece1, active=True, selected1=False)
                    else:
                        if sq1 == self.selected_sq1 or sq1 == self.selected_sq2:
                            self.set_piece_image(sq1, piece1, active=False, selected1=True)
                        else:
                            self.set_piece_image(sq1, piece1, active=False, selected1=False)
                elif sq1 in self.laser_beams:
                    lab1 = self.image_map[sq1]
                    (dir1, color1) = self.laser_beams[sq1]
                    if color1 == 1:
                        if dir1 == 1:
                            lab1.setPixmap(self.bm_images['bm_v1'])
                        elif dir1 == 2:
                            lab1.setPixmap(self.bm_images['bm_h1'])
                        else:
                            lab1.setPixmap(self.bm_images['bm_c1'])
                    elif color1 == 2:
                        if dir1 == 1:
                            lab1.setPixmap(self.bm_images['bm_v2'])
                        elif dir1 == 2:
                            lab1.setPixmap(self.bm_images['bm_h2'])
                        else:
                            lab1.setPixmap(self.bm_images['bm_c2'])
                    else:
                        if dir1 == 1:
                            lab1.setPixmap(self.bm_images['bm_c21'])
                        else:
                            lab1.setPixmap(self.bm_images['bm_c12'])
                elif sq1 in self.image_map:
                    if ((r == 0 and c == 0) or (r == 0 and c == 7) or
                        (r == 5 and c == 0) or (r == 5 and c == 7)):
                        pass
                    else:
                        lab1 = self.image_map[sq1]
                        lab1.clear()
                else:
                    pass

    def marker_trigger1(self):
        self.display_markers()

    def marker_trigger2(self):
        self.display_markers()

    def marker_trigger3(self):
        self.display_markers()

    def marker_trigger4(self):
        self.display_markers()

    def display_markers(self):
        self.clear_headers()
        c1 = self.ui.comboBox.currentIndex()
        c2 = self.ui.comboBox_4.currentIndex()
        r1 = self.ui.comboBox_2.currentIndex()
        r2 = self.ui.comboBox_3.currentIndex()
        self.new_pos1 = (r1-1, c1-1)
        self.new_pos2 = (r2-1, c2-1)
        sq1 = self.bsquares[r1-1][c1-1]
        sq2 = self.bsquares[r2-1][c2-1]
        self.selected_sq1 = sq1
        self.selected_sq2 = sq2
        if not c1 == 0:
            if not c2 == 0:
                colh1 = self.colheaders[c1-1]
                colh2 = self.colheaders[c2-1]
                colhval1 = self.colhvals[c1-1]
                colhval2 = self.colhvals[c2-1]
                if c1 == c2:
                    valstr1 = '*' + colhval1 + '*'
                    colh1.setText(valstr1)
                else:
                    valstr1a = '*' + colhval1
                    colh1.setText(valstr1a)
                    valstr2a = colhval2 + '*'
                    colh2.setText(valstr2a)
            else:
                colh1 = self.colheaders[c1-1]
                colhval1 = self.colhvals[c1-1]
                valstr1 = '*' + colhval1
                colh1.setText(valstr1)
        elif not c2 == 0:
            colh2 = self.colheaders[c2-1]
            colhval2 = self.colhvals[c2-1]
            valstr2 = colhval2 + '*'
            colh2.setText(valstr2)
        else:
            pass
        if not r1 == 0:
            if not r2 == 0:
                rowh1 = self.rowheaders[r1-1]
                rowh2 = self.rowheaders[r2-1]
                rowhval1 = self.rowhvals[r1-1]
                rowhval2 = self.rowhvals[r2-1]
                if r1 == r2:
                    valstr1 = '*' + rowhval1 + '*'
                    rowh1.setText(valstr1)
                else:
                    valstr1a = '*' + rowhval1
                    rowh1.setText(valstr1a)
                    valstr2a = rowhval2 + '*'
                    rowh2.setText(valstr2a)
            else:
                rowh1 = self.rowheaders[r1-1]
                rowhval1 = self.rowhvals[r1-1]
                valstr1 = '*' + rowhval1
                rowh1.setText(valstr1)
        elif not r2 == 0:
            rowh2 = self.rowheaders[r2-1]
            rowhval2 = self.rowhvals[r2-1]
            valstr2 = rowhval2 + '*'
            rowh2.setText(valstr2)
        else:
            pass
                
    def strike_piece(self, piece1, direct_in, player_a, last_sq=None):
        (pcid, direct2, player_b) = piece1
        action1 = None
        # old: 1 = up, -1 = down, 3 = right, -3 = left
        # 1j = up, -1j = down, 1 = right, -1 = left
        # (beam_dir, mr_dir)
        swap1 = {(-1j, 1):1, (-1j, 2):-1, (1, 2):1j, (1, 3):-1j,
                 (1j, 3):-1, (1j, 0):1, (-1, 1):1j, (-1, 0):-1j}
        if pcid == 'mr':
            if player_b == player_a:
                tp1 = (direct_in, direct2)
                if tp1 in swap1:
                    direct_out = swap1[tp1]
                    action1 = 'activate'
                else:
                    direct_out = 0
                    action1 = 'blocked'
            else:
                tp1 = (direct_in, direct2)
                if tp1 in swap1:
                    direct_out = 0
                    action1 = 'blocked'
                else:
                    direct_out = 0
                    if last_sq in self.active_squares2:
                        action1 = 'backstrike'
                    else:
                        action1 = 'blocked'
        else:
            direct_out = 0
            action1 = 'blocked'
        return direct_out, action1
                
    def track_lasers(self):
        # Green
        # laser at A1
        # right
        direct_in = 1
##         r = 1
##         c = 0
        pos = 2+1j
        self.active_squares2 = {}
        self.laser_beams = {}
        action1 = None
        action2 = None
        maxiter = 48
        at_end1 = False
        at_end2 = False
        i = 0
        last_sq1 = 'B1'
        while i < maxiter and not at_end2:
            i += 1
            try:
                r = int(pos.imag)-1
                c = int(pos.real)-1
                sq1 = self.bsquares[r][c]
            except IndexError:
                action1 = None
                break
            if r == 5:
                if c == 7:
                    if direct_in == -1j:
                        action1 = 'win'
                    else:
                        action1 = 'blocked'
                    break
                elif c == 0:
                    action1 = 'blocked'
                    break
                elif direct_in == -1j:
                    action1 = 'blocked'
                    at_end1 = True
                else:
                    at_end1 = False
            elif r == 0:
                if c == 0:
                    action1 = 'blocked'
                    break
                elif c == 7:
                    action1 = 'blocked'
                    break
                else:
                    pass
            elif r < 0 or r > 5 or c < 0 or c > 7:
                action1 = 'blocked'
                break
            else:
                at_end1 = False
            if sq1 in self.game_pieces2:
                piece1 = self.game_pieces2[sq1]
                direct_out, action1 = self.strike_piece(piece1, direct_in, 1, last_sq=last_sq1)
                if action1 == 'activate':
                    self.active_squares2[sq1] = 1
                    at_end1 = False
                elif action1 == 'backstrike':
                    (pcid, direct1, player_1) = piece1
                    player_2 = 1
                    piece2 = (pcid, direct1, player_2)
                    self.game_pieces2[sq1] = piece2
                    self.active_squares2[sq1] = 2
                    # self.capt_pieces[sq1] = piece1
                    break
                else:
                    at_end1 = False
            elif sq1 in self.laser_beams:
                beams1 = self.laser_beams[sq1]
                (bm_dir1, bm_color1) = beams1
                if bm_color1 == 1:
                    if direct_in in (1j, -1j) and bm_dir1 == 1:
                        bm_dir2 = 1
                    elif direct_in in (1, -1) and bm_dir1 == 2:
                        bm_dir2 = 2
                    else:
                        bm_dir2 = 3
                    bm_color2 = 1
                elif direct_in in (1j, -1j) and bm_dir1 == 2:
                    # vertical beam
                    bm_dir2 = 2
                    bm_color2 = 3
                elif direct_in in (1, -1) and bm_dir1 == 1:
                    # horizontal beam
                    bm_dir2 = 1
                    bm_color2 = 3
                else:
                    bm_dir2 = bm_dir1
                    bm_color2 = bm_color1
                beams2 = (bm_dir2, bm_color2)
                self.laser_beams[sq1] = beams2
                direct_out = direct_in
                action1 = None
            else:
                if direct_in in (1j, -1j):
                    self.laser_beams[sq1] = (1, 1)
                else:
                    self.laser_beams[sq1] = (2, 1)
                direct_out = direct_in
                action1 = None
                if at_end1:
                    at_end2 = True
                else:
                    at_end1 = False
            pos += direct_out.conjugate()
            last_sq1 = sq1
            if not abs(direct_out) == 0:
                direct_in = direct_out
            else:
                break
        # Red
        # laser at A6
        # right
        direct_in = 1
##         r = 4
##         c = 7
        pos = 2+6j
        i = 0
        last_sq2 = 'B6'
        at_end1 = False
        at_end2 = False
        while i < maxiter and not at_end2 and not action1 == 'win':
            i += 1
            try:
                r = int(pos.imag)-1
                c = int(pos.real)-1
                sq1 = self.bsquares[r][c]
            except IndexError:
                action2 = None
                break
            if r == 0:
                if c == 7:
                    if direct_in == 1j:
                        action2 = 'win'
                    else:
                        action2 = 'blocked'
                    break
                elif c == 0:
                    action2 = 'blocked'
                    break
                elif direct_in == 1j:
                    action2 = 'blocked'
                    at_end1 = True
                else:
                    at_end1 = False
            elif r == 5:
                if c == 0:
                    action2 = 'blocked'
                    break
                elif c == 7:
                    action2 = 'blocked'
                    break
                else:
                    pass
            elif r < 0 or r > 5 or c < 0 or c > 7:
                action2 = 'blocked'
                break
            else:
                at_end1 = False
            if sq1 in self.game_pieces2:
                piece1 = self.game_pieces2[sq1]
                direct_out, action2 = self.strike_piece(piece1, direct_in, 2, last_sq=last_sq2)
                if action2 == 'activate':
                    self.active_squares2[sq1] = 1
                    at_end1 = False
                elif action2 == 'backstrike':
                    (pcid, direct1, player_1) = piece1
                    player_2 = 2
                    piece2 = (pcid, direct1, player_2)
                    self.game_pieces2[sq1] = piece2
                    self.active_squares2[sq1] = 2
                    # self.capt_pieces[sq1] = piece1
                    break
                else:
                    at_end1 = False
            elif sq1 in self.laser_beams:
                beams1 = self.laser_beams[sq1]
                (bm_dir1, bm_color1) = beams1
                if bm_color1 == 2:
                    if direct_in in (1j, -1j) and bm_dir1 == 1:
                        bm_dir2 = 1
                    elif direct_in in (1, -1) and bm_dir1 == 2:
                        bm_dir2 = 2
                    else:
                        bm_dir2 = 3
                    bm_color2 = 2
                elif direct_in in (1j, -1j) and bm_dir1 == 2:
                    # vertical beam
                    bm_dir2 = 1
                    bm_color2 = 3
                elif direct_in in (1, -1) and bm_dir1 == 1:
                    # horizontal beam
                    bm_dir2 = 2
                    bm_color2 = 3
                else:
                    bm_dir2 = bm_dir1
                    bm_color2 = bm_color1
                beams2 = (bm_dir2, bm_color2)
                self.laser_beams[sq1] = beams2
                direct_out = direct_in
                action2 = None
            else:
                if direct_in in (1j, -1j):
                    self.laser_beams[sq1] = (1, 2)
                else:
                    self.laser_beams[sq1] = (2, 2)
                direct_out = direct_in
                action2 = None
                if at_end1:
                    at_end2 = True
                else:
                    at_end1 = False
            pos += direct_out.conjugate()
            last_sq2 = sq1
            if not abs(direct_out) == 0:
                direct_in = direct_out
            else:
                break
        return action1, action2
    
    def update_display(self):
        # lasers
        self.active_squares2 = {}
        action1, action2 = self.track_lasers()
        self.display_pieces()
        if action1 == 'win':
            lab1 = self.image_map['H6']
            lab1.setPixmap(self.or_images['tgt_u2'])
            return 'green_win'
        elif action2 == 'win':
            lab1 = self.image_map['H1']
            lab1.setPixmap(self.or_images['tgt_d2'])
            return 'red_win'
        elif 'backstrike' in (action1, action2):
            return 'backstrike'
        else:
            return None
    
    def move_piece1(self, r, c, dir1, player):
        # move
        sq1 = self.bsquares[r][c]
        pos1 = complex(c+1, r+1)
        moved1 = False
        if sq1 in self.game_pieces2:
            piece1 = self.game_pieces2[sq1]
            (pcid, direct1, player_1) = piece1
            if player_1 == player:
                pos2 = pos1 + dir1.conjugate()
                r2 = int(pos2.imag)-1
                c2 = int(pos2.real)-1
                try:
                    if not (r2 < 0 or c2 < 0):
                        sq2 = self.bsquares[r2][c2]
                    else:
                        sq2 = sq1
                    if pcid == 'bk' and sq2 in self.game_pieces2:
                        piece2 = self.game_pieces2[sq2]
                        (pcid2, direct2, player_2) = piece2
                        if pcid2 == 'bk' and not (player_2 == player_1):
                            self.game_pieces2[sq2] = piece1
                            del self.game_pieces2[sq1]
                            moved1 = True
                            if player == 1:
                                self.ui.comboBox.setCurrentIndex(c2+1)
                                self.ui.comboBox_2.setCurrentIndex(r2+1)
                            else:
                                self.ui.comboBox_4.setCurrentIndex(c2+1)
                                self.ui.comboBox_3.setCurrentIndex(r2+1)
                        else:
                            pass
                    else:
                        pass
                    if not sq2 in self.game_pieces2:
                        if (r2 == 0 or r2 == 5) and (c2 == 0 or c2 == 7):
                            pass
                        elif player == 1 and ((r2 == 5 and c2 == 1) or
                                              (r2 == 1 and c2 == 7)):
                            pass
                        elif player == 2 and ((r2 == 0 and c2 == 1) or
                                              (r2 == 4 and c2 == 7)):
                            pass
                        else:
                            self.game_pieces2[sq2] = piece1
                            del self.game_pieces2[sq1]
                            moved1 = True
                            if player == 1:
                                self.ui.comboBox.setCurrentIndex(c2+1)
                                self.ui.comboBox_2.setCurrentIndex(r2+1)
                            else:
                                self.ui.comboBox_4.setCurrentIndex(c2+1)
                                self.ui.comboBox_3.setCurrentIndex(r2+1)
                    else:
                        pass
                except IndexError:
                    pass
            else:
                pass
        else:
            pass
        return moved1
        
    def rotate_piece1(self, r, c, newdir, player):
        # rotate
        sq1 = self.bsquares[r][c]
        success1 = False
        if sq1 in self.game_pieces2:
            piece1 = self.game_pieces2[sq1]
            (pcid, direct1, player_1) = piece1
            if player_1 == player and pcid == 'mr':
                direct2 = newdir
                if not direct1 == direct2:
                    piece2 = (pcid, direct2, player_1)
                    self.game_pieces2[sq1] = piece2
                    success1 = True
                else:
                    pass
            else:
                pass
        else:
            pass
        return success1

    def green_undo1(self):
        if self.player_turn == 'green' and self.player_turn2 == 'red':
            self.player_turn2 = 'green'
            self.game_pieces2 = self.game_pieces.copy()
            self.active_squares2 = self.active_squares.copy()
            self.capt_pieces = {}
            (r, c) = self.old_pos1
            self.ui.comboBox_2.setCurrentIndex(r+1)
            self.ui.comboBox.setCurrentIndex(c+1)
            self.update_display()
            self.ui.textEdit.append("Undo; Green's turn")
            self.ui.textEdit_2.append("Undo; Green's turn")
        else:
            pass

    def red_undo1(self):
        if self.player_turn == 'red' and self.player_turn2 == 'green':
            self.player_turn2 = 'red'
            self.game_pieces2 = self.game_pieces.copy()
            self.active_squares2 = self.active_squares.copy()
            self.capt_pieces = {}
            (r, c) = self.old_pos2
            self.ui.comboBox_3.setCurrentIndex(r+1)
            self.ui.comboBox_4.setCurrentIndex(c+1)
            self.update_display()
            self.ui.textEdit.append("Undo; Red's turn")
            self.ui.textEdit_2.append("Undo; Red's turn")
        else:
            pass
        
    def green_up(self):
        self.move_piece2(1j, None, 'green')
        
    def green_left(self):
        self.move_piece2(-1, None, 'green')
        
    def green_down(self):
        self.move_piece2(-1j, None, 'green')
        
    def green_right(self):
        self.move_piece2(1, None, 'green')
        
    def red_up(self):
        self.move_piece2(1j, None, 'red')
        
    def red_left(self):
        self.move_piece2(-1, None, 'red')
        
    def red_down(self):
        self.move_piece2(-1j, None, 'red')
        
    def red_right(self):
        self.move_piece2(1, None, 'red')

    def green_r_up(self):
        if self.last_rotate_dir1 is None:
            self.last_rotate_dir1 = 1j
        elif self.last_rotate_dir1 == 1:
            self.move_piece2(None, 1, 'green')
            self.last_rotate_dir1 = None
        elif self.last_rotate_dir1 == -1:
            self.move_piece2(None, 2, 'green')
            self.last_rotate_dir1 = None
        else:
            pass

    def green_r_left(self):
        if self.last_rotate_dir1 is None:
            self.last_rotate_dir1 = -1
        elif self.last_rotate_dir1 == 1j:
            self.move_piece2(None, 2, 'green')
            self.last_rotate_dir1 = None
        elif self.last_rotate_dir1 == -1j:
            self.move_piece2(None, 3, 'green')
            self.last_rotate_dir1 = None
        else:
            pass

    def green_r_down(self):
        if self.last_rotate_dir1 is None:
            self.last_rotate_dir1 = -1j
        elif self.last_rotate_dir1 == 1:
            self.move_piece2(None, 0, 'green')
            self.last_rotate_dir1 = None
        elif self.last_rotate_dir1 == -1:
            self.move_piece2(None, 3, 'green')
            self.last_rotate_dir1 = None
        else:
            pass

    def green_r_right(self):
        if self.last_rotate_dir1 is None:
            self.last_rotate_dir1 = 1
        elif self.last_rotate_dir1 == 1j:
            self.move_piece2(None, 1, 'green')
            self.last_rotate_dir1 = None
        elif self.last_rotate_dir1 == -1j:
            self.move_piece2(None, 0, 'green')
            self.last_rotate_dir1 = None
        else:
            pass

    def red_r_up(self):
        if self.last_rotate_dir2 is None:
            self.last_rotate_dir2 = 1j
        elif self.last_rotate_dir2 == 1:
            self.move_piece2(None, 1, 'red')
            self.last_rotate_dir2 = None
        elif self.last_rotate_dir2 == -1:
            self.move_piece2(None, 2, 'red')
            self.last_rotate_dir2 = None
        else:
            pass

    def red_r_left(self):
        if self.last_rotate_dir2 is None:
            self.last_rotate_dir2 = -1
        elif self.last_rotate_dir2 == 1j:
            self.move_piece2(None, 2, 'red')
            self.last_rotate_dir2 = None
        elif self.last_rotate_dir2 == -1j:
            self.move_piece2(None, 3, 'red')
            self.last_rotate_dir2 = None
        else:
            pass

    def red_r_down(self):
        if self.last_rotate_dir2 is None:
            self.last_rotate_dir2 = -1j
        elif self.last_rotate_dir2 == 1:
            self.move_piece2(None, 0, 'red')
            self.last_rotate_dir2 = None
        elif self.last_rotate_dir2 == -1:
            self.move_piece2(None, 3, 'red')
            self.last_rotate_dir2 = None
        else:
            pass

    def red_r_right(self):
        if self.last_rotate_dir2 is None:
            self.last_rotate_dir2 = 1
        elif self.last_rotate_dir2 == 1j:
            self.move_piece2(None, 1, 'red')
            self.last_rotate_dir2 = None
        elif self.last_rotate_dir2 == -1j:
            self.move_piece2(None, 0, 'red')
            self.last_rotate_dir2 = None
        else:
            pass

    def cycle_green_next(self):
        colstr = str(self.ui.comboBox.currentText())
        rowstr = str(self.ui.comboBox_2.currentText())
        colmap = {'A':0, 'B':1, 'C':2, 'D':3,
                  'E':4, 'F':5, 'G':6, 'H':7}
        try:
            r = int(rowstr) - 1
            c = colmap[colstr]
        except (ValueError, KeyError):
            r = 0
            c = 0
        rf = r
        cf = c
        while 1:
            if c < 7:
                c += 1
            else:
                c = 0
                r += 1
            try:
                sq1 = self.bsquares[r][c]
            except IndexError:
                break
            if sq1 in self.game_pieces2:
                piece1 = self.game_pieces2[sq1]
                (pcid, direct1, player_1) = piece1
                if player_1 == 1:
                    rf = r
                    cf = c
                    break
                else:
                    pass
            else:
                pass
        self.old_pos1 = (rf, cf)
        self.ui.comboBox.setCurrentIndex(cf+1)
        self.ui.comboBox_2.setCurrentIndex(rf+1)
        self.last_rotate_dir1 = None
        self.display_pieces()

    def cycle_green_prev(self):
        colstr = str(self.ui.comboBox.currentText())
        rowstr = str(self.ui.comboBox_2.currentText())
        colmap = {'A':0, 'B':1, 'C':2, 'D':3,
                  'E':4, 'F':5, 'G':6, 'H':7}
        try:
            r = int(rowstr) - 1
            c = colmap[colstr]
        except (ValueError, KeyError):
            r = 0
            c = 0
        rf = r
        cf = c
        while 1:
            if c > 0:
                c -= 1
            elif r > 0:
                c = 7
                r -= 1
            else:
                rf = r
                cf = c
                break
            try:
                sq1 = self.bsquares[r][c]
            except IndexError:
                break
            if sq1 in self.game_pieces2:
                piece1 = self.game_pieces2[sq1]
                (pcid, direct1, player_1) = piece1
                if player_1 == 1:
                    rf = r
                    cf = c
                    break
                else:
                    pass
            else:
                pass
        self.old_pos1 = (rf, cf)
        self.ui.comboBox.setCurrentIndex(cf+1)
        self.ui.comboBox_2.setCurrentIndex(rf+1)
        self.last_rotate_dir1 = None
        self.display_pieces()

    def cycle_red_next(self):
        colstr = str(self.ui.comboBox_4.currentText())
        rowstr = str(self.ui.comboBox_3.currentText())
        colmap = {'A':0, 'B':1, 'C':2, 'D':3,
                  'E':4, 'F':5, 'G':6, 'H':7}
        try:
            r = int(rowstr) - 1
            c = colmap[colstr]
        except (ValueError, KeyError):
            r = 0
            c = 0
        rf = r
        cf = c
        while 1:
            if c < 7:
                c += 1
            else:
                c = 0
                r += 1
            try:
                sq1 = self.bsquares[r][c]
            except IndexError:
                break
            if sq1 in self.game_pieces2:
                piece1 = self.game_pieces2[sq1]
                (pcid, direct1, player_1) = piece1
                if player_1 == 2:
                    rf = r
                    cf = c
                    break
                else:
                    pass
            else:
                pass
        self.old_pos2 = (rf, cf)
        self.ui.comboBox_4.setCurrentIndex(cf+1)
        self.ui.comboBox_3.setCurrentIndex(rf+1)
        self.last_rotate_dir2 = None
        self.display_pieces()

    def cycle_red_prev(self):
        colstr = str(self.ui.comboBox_4.currentText())
        rowstr = str(self.ui.comboBox_3.currentText())
        colmap = {'A':0, 'B':1, 'C':2, 'D':3,
                  'E':4, 'F':5, 'G':6, 'H':7}
        try:
            r = int(rowstr) - 1
            c = colmap[colstr]
        except (ValueError, KeyError):
            r = 0
            c = 0
        rf = r
        cf = c
        while 1:
            if c > 0:
                c -= 1
            elif r > 0:
                c = 7
                r -= 1
            else:
                cf = c
                rf = r
                break
            try:
                sq1 = self.bsquares[r][c]
            except IndexError:
                break
            if sq1 in self.game_pieces2:
                piece1 = self.game_pieces2[sq1]
                (pcid, direct1, player_1) = piece1
                if player_1 == 2:
                    rf = r
                    cf = c
                    break
                else:
                    pass
            else:
                pass
        self.old_pos2 = (rf, cf)
        self.ui.comboBox_4.setCurrentIndex(cf+1)
        self.ui.comboBox_3.setCurrentIndex(rf+1)
        self.last_rotate_dir2 = None
        self.display_pieces()

    def move_piece2(self, movedir, rdir, player1):
        players = {'green':1, 'red':2}
        message_boxes = {'green':self.ui.textEdit, 'red':self.ui.textEdit_2}
        message_box1 = message_boxes[player1]
        if self.player_turn2 == player1:
            if self.player_turn2 == self.player_turn:
                pass
            else:
                self.player_turn = self.player_turn2
                self.active_squares = self.active_squares2.copy()
                self.game_pieces = self.game_pieces2.copy()
                self.old_pos1 = self.new_pos1
                self.old_pos2 = self.new_pos2
            if player1 == 'green':
                colstr = str(self.ui.comboBox.currentText())
                rowstr = str(self.ui.comboBox_2.currentText())
            else:
                colstr = str(self.ui.comboBox_4.currentText())
                rowstr = str(self.ui.comboBox_3.currentText())
            colmap = {'A':0, 'B':1, 'C':2, 'D':3,
                      'E':4, 'F':5, 'G':6, 'H':7}
            try:
                r = int(rowstr) - 1
                c = colmap[colstr]
            except (ValueError, KeyError):
                r = 0
                c = 0
            player_id = players[player1]
            if not movedir is None:
                dir1 = movedir
                moved1 = self.move_piece1(r, c, dir1, player_id)
                if not moved1:
                    textstr1 = 'Invalid Move!\n'
                    message_box1.append(textstr1)
                else:
                    self.last_rotate_dir1 == None
                    self.last_rotate_dir2 == None
                    info1 = self.update_display()
                    if info1 == 'green_win':
                        textstr1 = 'Green Wins!'
                        self.ui.textEdit.clear()
                        self.ui.textEdit_2.clear()
                        self.player_turn2 = 'green_win'
                    elif info1 == 'red_win':
                        textstr1 = 'Red Wins!'
                        self.ui.textEdit.clear()
                        self.ui.textEdit_2.clear()
                        self.player_turn2 = 'red_win'
                    else:
                        swap_turn = {'green':'red', 'red':'green'}
                        self.player_turn2 = swap_turn[player1]
                        textstr1 = swap_turn[player1] + "'s turn"
                    message_boxes['red'].append(textstr1)
                    message_boxes['green'].append(textstr1)
            elif not rdir is None:
                newdir1 = rdir
                rotated1 = self.rotate_piece1(r, c, newdir1, player_id)
                if not rotated1:
                    textstr1 = 'Invalid Move!\n'
                    message_box1.append(textstr1)
                else:
                    self.last_rotate_dir1 == None
                    self.last_rotate_dir2 == None
                    info1 = self.update_display()
                    if info1 == 'green_win':
                        textstr1 = 'Green Wins!'
                        self.ui.textEdit.clear()
                        self.ui.textEdit_2.clear()
                        self.player_turn2 = 'green_win'
                    elif info1 == 'red_win':
                        textstr1 = 'Red Wins!'
                        self.ui.textEdit.clear()
                        self.ui.textEdit_2.clear()
                        self.player_turn2 = 'red_win'
                    else:
                        swap_turn = {'green':'red', 'red':'green'}
                        self.player_turn2 = swap_turn[player1]
                        textstr1 = swap_turn[player1] + "'s turn"
                message_boxes['red'].append(textstr1)
                message_boxes['green'].append(textstr1)
        elif self.player_turn2 in ('green_win', 'red_win'):
            # game is over
            pass
        elif self.player_turn2 is None:
            # game has not been set up
            pass
        else:
            textstr1 = 'Not your turn!\n'
            message_box1.append(textstr1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    app.exec()
