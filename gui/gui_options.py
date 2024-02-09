from PyQt6.QtGui import QFont

FONT_TYPE = QFont("Segoe UI", 10, weight = -1)
FONT_TYPE_BOLD = QFont("Segoe UI", 10)
FONT_TYPE_BOLD.setWeight(QFont.Weight.Bold)

LANGUAGE = {'English' : {'Table_Viewer' : 'Table Viewer', 'File' : 'File', 'Options' : 'Options', 'Open_File' : 'Open File',
                         'Close' : 'Close', 'Language' : 'Language', 'All_Files' : 'All Files', 'Invalid_File_Title' : 'Invalid File',
                         'Invalid_File_Message' : 'Invalid file format selected', 'Create_Graph' : 'Create Graphic','Plot_Types' : ['Bars', 'Lines'],
                         'X_Axis' : 'X Axis', 'Y_Axis' : 'Y Axis', 'No_Tables_Title' : 'No Open Tables', 'No_Tables_Message' : 'There is no open table'},
            'Português' : {'Table_Viewer' : 'Visualizador de Tablas', 'File' : 'Ficheiro', 'Options' : 'Opções',
                           'Open_File' : 'Abrir Ficheiro', 'Close' : 'Fechar', 'Language' : 'Linguagem', 'All_Files': 'Todos os Ficheiros',
                           'Invalid_File_Title' : 'Formato Inválido', 'Invalid_File_Message' : 'Formato de ficheiro selecionado inválido',
                           'Create_Graph' : 'Criar Gráfico', 'Plot_Types' : ['Barras', 'Linhas'], 'X_Axis' : 'Eixo X', 'Y_Axis' : 'Eixo Y',
                           'No_Tables_Title' : 'Sem Tabelas', 'No_Tables_Message' : 'Não existem tabelas abertas'}}