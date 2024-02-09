from PyQt6.QtWidgets import (QMainWindow, QWidget, QMenu, QFileDialog, QTabWidget, QVBoxLayout, QLabel,
                             QTableView, QDialog)
from PyQt6.QtGui import QAction, QStandardItemModel, QStandardItem
from gui.custom_widgets import MessageWindow, GraphOptions
from gui.gui_options import FONT_TYPE, LANGUAGE
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        self.lang = LANGUAGE['English']
        self.files_tab_dict = {}
        super(MainWindow, self).__init__()
        self.set_window_placements()
        self.set_menubar()
        
        
    def set_window_placements(self):
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle(self.lang['Table_Viewer']) 
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
    def set_menubar(self):
        self.menubar = self.menuBar()
        self.menubar.setFont(FONT_TYPE)
        
        file_menu = self.menubar.addMenu(self.lang['File'])
        options_menu = self.menubar.addMenu(self.lang['Options'])
        
        open_file_action = QAction(self.lang['Open_File'], self)
        close_action = QAction(self.lang['Close'], self)
        
        create_graph_action = QAction(self.lang['Create_Graph'], self)
        language_submenu = QMenu(self.lang['Language'], self)
        english_action = QAction('English', self)
        portuguese_action = QAction('Português', self)
        
        file_menu.addAction(open_file_action)
        file_menu.addAction(close_action)
        options_menu.addAction(create_graph_action)
        options_menu.addMenu(language_submenu)
        language_submenu.addAction(english_action)
        language_submenu.addAction(portuguese_action)
        
        open_file_action.triggered.connect(self.open_files_tabs)
        create_graph_action.triggered.connect(self.open_graph_menu)
        english_action.triggered.connect(lambda: self.set_language('English'))
        portuguese_action.triggered.connect(lambda: self.set_language('Português'))
        close_action.triggered.connect(self.close)
    
    def set_language(self, language: str):
        self.lang = LANGUAGE[language]
        self.setWindowTitle(self.lang['Table_Viewer']) 
        self.menubar.clear()
        self.set_menubar()
  
    def show_file_dialog(self):
        file_dialog = QFileDialog()
        # file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)

        file_dialog.setNameFilter(f'(*.csv);; (*.xlsx; *.xls);; {self.lang['All_Files']} (*)')

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            print()
            return selected_files[0]
            
    def open_files_tabs(self):
        filepath = self.show_file_dialog()
        if filepath:
            filename = filepath.split('/')[-1]
            extension = filepath.split('.')[-1]
            df = self.make_df(filepath, extension)
            if isinstance(df, pd.DataFrame):
                tab = QWidget()
                self.set_tab_layout(tab, filename, df)
                self.files_tab_dict[filename] = [tab, df]
            else:
                window = MessageWindow(self.lang['Invalid_File_Title'], [self.lang['Invalid_File_Message']], self.lang)
                self.open_qdialog(window)

    def make_df(self, filepath: str, extension: str):
        match extension:
            case 'csv':
                df = pd.read_csv(filepath)
                return df
            case 'xlsx' | 'xls':
                df = pd.read_excel(filepath)
                return df
    
    def set_tab_layout(self, tab: QWidget, filename: str, df: pd.DataFrame):
        layout = QVBoxLayout()
        table = QTableView()
        
        model = self.get_model_from_df(df)
        table.setModel(model)
        table.resizeColumnsToContents()
        
        layout.addWidget(table)
        tab.setLayout(layout)
        
        self.tab_widget.addTab(tab, filename)
        
    def get_model_from_df(self, df: pd.DataFrame):
        model = QStandardItemModel(df.shape[0], df.shape[1])
        model.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                item = QStandardItem(str(df.iat[row, column]))
                model.setItem(row, column, item)

        return model
    
    def open_graph_menu(self):
        tab_name = self.centralWidget().tabText(self.tab_widget.currentIndex())
        if tab_name:
            window = GraphOptions(self.lang, self.files_tab_dict, tab_name)
            self.open_qdialog(window)
        else:
            window = MessageWindow(self.lang['No_Tables_Title'], [self.lang['No_Tables_Message']], self.lang)
            self.open_qdialog(window)
    
    def open_qdialog(self, new_window: QDialog):
        open_qdialog = new_window
        try:
            open_qdialog.qdialog_signal.connect(self.get_plot_signal)
        except:
            pass
        open_qdialog.exec()
        
    def get_plot_signal(self, plot_data: dict):
        match plot_data['type']:
            case 'Lines' | 'Linhas':
                plot = sns.lineplot(self.files_tab_dict[plot_data['table']][1], x = plot_data['x'], y = plot_data['y'])
            case 'Bars' | 'Barras':
                plot = sns.barplot(self.files_tab_dict[plot_data['table']][1], x = plot_data['x'], y = plot_data['y'])
                
        canvas = FigureCanvas(plot.figure)
        self.tab_widget.addTab(canvas, 'G:' + plot_data['table'])
                