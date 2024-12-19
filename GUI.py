import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget,
                             QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QLabel)


class CompilerInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('交互式编译器界面')

        # 主部件
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # 布局
        self.layout = QVBoxLayout(self.centralWidget)

        # 可编辑的代码框
        self.codeEditor = QTextEdit()
        self.codeEditor.setPlaceholderText("在这里编写代码...")
        self.layout.addWidget(QLabel("代码编辑器:"))
        self.layout.addWidget(self.codeEditor)

        # 编译后目标机器指令或中间代码显示框
        self.intermediateCodeDisplay = QTextEdit()
        self.intermediateCodeDisplay.setReadOnly(True)
        self.layout.addWidget(QLabel("中间代码:"))
        self.layout.addWidget(self.intermediateCodeDisplay)

        # 编译后及运行时数据管理显示框
        self.dataManagementDisplay = QTextEdit()
        self.dataManagementDisplay.setReadOnly(True)
        self.layout.addWidget(QLabel("数据管理:"))
        self.layout.addWidget(self.dataManagementDisplay)

        # 编译错误警示框
        self.errorDisplay = QTextEdit()
        self.errorDisplay.setReadOnly(True)
        self.layout.addWidget(QLabel("编译错误:"))
        self.layout.addWidget(self.errorDisplay)

        # 运行结果显示框
        self.outputDisplay = QTextEdit()
        self.outputDisplay.setReadOnly(True)
        self.layout.addWidget(QLabel("运行结果:"))
        self.layout.addWidget(self.outputDisplay)

        # 编译和运行按钮
        self.compileButton = QPushButton("编译")
        self.runButton = QPushButton("运行")
        self.compileButton.clicked.connect(self.compileCode)
        self.runButton.clicked.connect(self.runCode)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.compileButton)
        buttonLayout.addWidget(self.runButton)
        self.layout.addLayout(buttonLayout)

        # 菜单栏
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('文件')

        self.importAction = self.fileMenu.addAction('导入')
        self.importAction.triggered.connect(self.importFile)

        self.saveAction = self.fileMenu.addAction('保存')
        self.saveAction.triggered.connect(self.saveFile)

        self.show()

    def compileCode(self):
        code = self.codeEditor.toPlainText()
        fileName = "temp_code.l"
        with open(fileName, 'w') as file:
            file.write(code)

        # 调用flex编译文件
        try:
            subprocess.run(["flex", fileName], check=True, capture_output=True, text=True)
            result = subprocess.run(["gcc", "lex.yy.c", "-o", "output_executable"], check=True, capture_output=True, text=True)
            self.intermediateCodeDisplay.setPlainText(result.stdout)
            self.dataManagementDisplay.setPlainText("数据管理信息")
            self.errorDisplay.clear()
        except subprocess.CalledProcessError as e:
            self.errorDisplay.setPlainText(f"编译错误:\n{e.stderr}")

    def runCode(self):
        if self.errorDisplay.toPlainText():
            QMessageBox.warning(self, "无法运行", "请先修正编译错误再运行。")
        else:
            try:
                result = subprocess.run(["./output_executable"], check=True, capture_output=True, text=True)
                self.outputDisplay.setPlainText(result.stdout)
            except subprocess.CalledProcessError as e:
                self.outputDisplay.setPlainText(f"运行错误:\n{e.stderr}")

    def importFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "导入代码文件", "", "所有文件 (*);;Flex 文件 (*.l)", options=options)
        if fileName:
            with open(fileName, 'r') as file:
                self.codeEditor.setPlainText(file.read())

    def saveFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "保存代码文件", "", "所有文件 (*);;Flex 文件 (*.l)", options=options)
        if fileName:
            with open(fileName, 'w') as file:
                file.write(self.codeEditor.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CompilerInterface()
    sys.exit(app.exec_())
