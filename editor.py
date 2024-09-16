from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QColorDialog, QFontDialog, QToolBar, QComboBox, QVBoxLayout, QWidget, QMessageBox, QInputDialog, QMenu
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QTextListFormat, QTextTableFormat, QImage, QTextDocument, QTextCharFormat, QTextDocumentFragment, QCursor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices  # Import QDesktopServices

import sys

class AdvancedTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)

        self.init_ui()

    def init_ui(self):
        self.create_toolbar()
        self.create_menu()

        self.setWindowTitle('Advanced Text Editor')
        self.setGeometry(100, 100, 800, 600)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Font actions
        font_action = QAction('Font', self)
        font_action.triggered.connect(self.change_font)
        toolbar.addAction(font_action)

        # Font size selector
        self.font_size_selector = QComboBox(self)
        self.font_size_selector.addItems([str(size) for size in range(8, 30, 2)])
        self.font_size_selector.setCurrentText('12')
        self.font_size_selector.currentTextChanged.connect(self.change_font_size)
        toolbar.addWidget(self.font_size_selector)

        # Bold action
        bold_action = QAction('B', self)
        bold_action.setShortcut('Ctrl+B')
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        # Italic action
        italic_action = QAction('I', self)
        italic_action.setShortcut('Ctrl+I')
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)

        # Underline action
        underline_action = QAction('U', self)
        underline_action.setShortcut('Ctrl+U')
        underline_action.triggered.connect(self.toggle_underline)
        toolbar.addAction(underline_action)

        # Align left action
        align_left_action = QAction('L', self)
        align_left_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        toolbar.addAction(align_left_action)

        # Align center action
        align_center_action = QAction('C', self)
        align_center_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        toolbar.addAction(align_center_action)

        # Align right action
        align_right_action = QAction('R', self)
        align_right_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        toolbar.addAction(align_right_action)

        # Text color action
        color_action = QAction('Color', self)
        color_action.triggered.connect(self.change_text_color)
        toolbar.addAction(color_action)

        # Attach file action
        attach_action = QAction('Attach', self)
        attach_action.triggered.connect(self.attach_file)
        toolbar.addAction(attach_action)

        # Insert table action
        table_action = QAction('Table', self)
        table_action.triggered.connect(self.insert_table)
        toolbar.addAction(table_action)

        # Ordered list action
        ordered_list_action = QAction('OL', self)
        ordered_list_action.triggered.connect(self.insert_ordered_list)
        toolbar.addAction(ordered_list_action)

        # Unordered list action
        unordered_list_action = QAction('UL', self)
        unordered_list_action.triggered.connect(self.insert_unordered_list)
        toolbar.addAction(unordered_list_action)

        # Insert hyperlink action
        # hyperlink_action = QAction('Hyperlink', self)
        # hyperlink_action.triggered.connect(self.insert_hyperlink)
        # toolbar.addAction(hyperlink_action)

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        # New file action
        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        # Open file action
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Save file action
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Edit menu
        # edit_menu = menubar.addMenu('Edit')

        # Context menu for hyperlinks
        # self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.editor.customContextMenuRequested.connect(self.show_context_menu)

        # self.link_action = QAction('Open Link', self)
        # self.link_action.triggered.connect(self.open_selected_link)
        # edit_menu.addAction(self.link_action)

    def toggle_bold(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontWeight(QFont.Bold if not fmt.fontWeight() == QFont.Bold else QFont.Normal)
        self.editor.setCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.editor.setCurrentCharFormat(fmt)

    def toggle_underline(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.editor.setCurrentCharFormat(fmt)

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.editor.setCurrentFont(font)

    def change_font_size(self, size):
        fmt = self.editor.currentCharFormat()
        fmt.setFontPointSize(float(size))
        self.editor.setCurrentCharFormat(fmt)

    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = self.editor.currentCharFormat()
            fmt.setForeground(color)
            self.editor.setCurrentCharFormat(fmt)

    def attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Attach File', '', 'All Files (*)')
        if file_path:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image = QImage(file_path)
                if image.isNull():
                    QMessageBox.information(self, "Image Viewer", "Cannot load %s." % file_path)
                    return
                cursor = self.editor.textCursor()
                cursor.insertImage(image)
            else:
                self.editor.insertPlainText(f'\nAttached file: {file_path}\n')

    def insert_table(self):
        rows, ok1 = QInputDialog.getInt(self, 'Rows', 'Enter number of rows:')
        cols, ok2 = QInputDialog.getInt(self, 'Columns', 'Enter number of columns:')
        if ok1 and ok2:
            cursor = self.editor.textCursor()
            table_format = QTextTableFormat()
            table_format.setBorder(1)
            table_format.setCellPadding(4)
            table_format.setCellSpacing(2)
            cursor.insertTable(rows, cols, table_format)

    def insert_ordered_list(self):
        cursor = self.editor.textCursor()
        cursor.insertList(QTextListFormat.ListDecimal)

    def insert_unordered_list(self):
        cursor = self.editor.textCursor()
        cursor.insertList(QTextListFormat.ListDisc)

    # def insert_hyperlink(self):
    #     url, ok = QInputDialog.getText(self, 'Insert Hyperlink', 'Enter URL:')
    #     if ok and url:
    #         cursor = self.editor.textCursor()
    #         selected_text = cursor.selectedText()
    #         if not selected_text:
    #             cursor.insertText(url)
    #             cursor.setPosition(cursor.position() - len(url))
    #         else:
    #             format = QTextCharFormat()
    #             format.setAnchor(True)
    #             format.setAnchorHref(url)
    #             format.setForeground(Qt.blue)
    #             cursor.mergeCharFormat(format)

    # def show_context_menu(self, pos):
    #     cursor = self.editor.cursorForPosition(pos)
    #     cursor.select(QTextCursor.WordUnderCursor)
    #     selected_text = cursor.selectedText()

    #     if cursor.charFormat().isAnchor():
    #         menu = QMenu(self)
    #         menu.addAction(self.link_action)
    #         menu.exec_(self.editor.viewport().mapToGlobal(pos))

    # def open_selected_link(self):
        cursor = self.editor.cursorForPosition(self.editor.mapFromGlobal(QCursor.pos()))
        if cursor.charFormat().isAnchor():
            url = cursor.charFormat().anchorHref()
            if QUrl(url).isValid():
                QDesktopServices.openUrl(QUrl(url))

    def new_file(self):
        self.editor.clear()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            with open(file_path, 'r') as file:
                self.editor.setText(file.read())

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.editor.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = AdvancedTextEditor()
    editor.show()
    sys.exit(app.exec_())
