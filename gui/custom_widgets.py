from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QGridLayout, QComboBox, QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from gui.gui_options import FONT_TYPE, FONT_TYPE_BOLD, LANGUAGE

class MessageWindow(QDialog):
    def __init__(self, title: str, messages: list, languages: dict):
        self.title = title
        self.messages = messages
        self.lang = languages
        super(MessageWindow, self).__init__()
        self.setFont(FONT_TYPE)
        self.set_widgets_placements()
        
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle(self.title)
        add_message_layout = QVBoxLayout()
        self.setLayout(add_message_layout)
        
        for message in self.messages:
            message_label = QLabel(message)
            add_message_layout.addWidget(message_label, alignment = Qt.AlignmentFlag.AlignCenter)
        
        message_close_button = HighOptionsButton(self.lang['Close'])
        
        add_message_layout.addWidget(message_close_button, alignment = Qt.AlignmentFlag.AlignCenter)
        
        message_close_button.clicked.connect(lambda: self.close())
        
class HighOptionsButton(QPushButton):
    def __init__(self, *args):
        super(HighOptionsButton, self).__init__(*args)
        self.setFont(FONT_TYPE_BOLD)
        self.setFixedSize(140, 40)
        
class GraphOptions(QDialog):
    qdialog_signal = pyqtSignal(dict)
    def __init__(self, languages: dict, tab_tables: dict, current_tab: str, *args, **kwargs):
        self.lang = languages
        self.tab_tables = tab_tables
        self.current_tab = current_tab
        super(QDialog, self).__init__(*args, **kwargs) 
        self.set_widgets_placements()
    
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 450, 200)
        self.setWindowTitle(self.lang['Create_Graph'])
        graph_layout = QVBoxLayout()
        self.setLayout(graph_layout)
        graph_options_layout = QGridLayout()
        graph_buttons_layout = QHBoxLayout()
        
        graph_layout.addLayout(graph_options_layout)
        graph_layout.addLayout(graph_buttons_layout)
        
        self.table_combo_box = QComboBox()
        self.plot_type_combo_box = QComboBox()
        self.x_axis_label = QLabel(self.lang['X_Axis'])
        self.x_axis_combo_box = QComboBox()
        self.y_axis_label = QLabel(self.lang['Y_Axis'])
        self.y_axis_combo_box = QComboBox()
        self.create_graph_button = HighOptionsButton(self.lang['Create_Graph'])
        close_graph_button = HighOptionsButton(self.lang['Close'])

        for key in self.tab_tables.keys():
            self.table_combo_box.addItem(key)
        self.table_combo_box.setCurrentText(self.current_tab)
            
        for type in self.lang['Plot_Types']:
            self.plot_type_combo_box.addItem(type)
            
        self.set_axis_combo_boxes()
  
        self.table_combo_box.setFixedWidth(200)
        self.plot_type_combo_box.setFixedWidth(200)
        self.x_axis_label.setFixedWidth(40)
        self.x_axis_combo_box.setFixedWidth(160)
        self.y_axis_label.setFixedWidth(40)
        self.y_axis_combo_box.setFixedWidth(160)
        
        graph_options_layout.addWidget(self.table_combo_box, 0, 0, 1, 4, Qt.AlignmentFlag.AlignLeft)
        graph_options_layout.addWidget(self.plot_type_combo_box, 0, 1, 1, 4, Qt.AlignmentFlag.AlignRight)
        graph_options_layout.addWidget(self.x_axis_label, 2, 0, Qt.AlignmentFlag.AlignRight)
        graph_options_layout.addWidget(self.x_axis_combo_box, 2, 1)
        graph_options_layout.addWidget(self.y_axis_label, 2, 2, Qt.AlignmentFlag.AlignRight)
        graph_options_layout.addWidget(self.y_axis_combo_box, 2, 3)
        graph_buttons_layout.addWidget(self.create_graph_button)
        graph_buttons_layout.addWidget(close_graph_button)
        
        self.create_graph_button.clicked.connect(self.emit_plot_signal)
        close_graph_button.clicked.connect(self.close)
        self.table_combo_box.currentTextChanged.connect(self.set_axis_combo_boxes)
        
    def set_axis_combo_boxes(self):     
        self.x_axis_combo_box.clear()
        self.y_axis_combo_box.clear()

        if self.table_combo_box.currentText():
            table = self.table_combo_box.currentText()
            for col in self.tab_tables[table][1].columns:
                self.x_axis_combo_box.addItem(col)
                self.y_axis_combo_box.addItem(col)
                       
    def emit_plot_signal(self):
        plot_dict =  {}
        plot_dict['table'] = self.table_combo_box.currentText()
        plot_dict['type'] = self.plot_type_combo_box.currentText()
        plot_dict['x'] = self.x_axis_combo_box.currentText()
        plot_dict['y'] = self.y_axis_combo_box.currentText()
        self.qdialog_signal.emit(plot_dict)
        self.close()