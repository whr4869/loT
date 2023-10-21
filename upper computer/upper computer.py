from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTextEdit, QGridLayout,QPushButton, QFileDialog, QLabel, QLineEdit,QHBoxLayout,QSlider)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import (QUrl, Qt)
from PyQt5.QtGui import QFont
import numpy as np
import pandas as pd
import openpyxl
from openpyxl.chart import LineChart, Reference
import re

class MyWindow(QMainWindow):  #定义了一个名为 MyWindow 的类，继承自 QMainWindow
    def __init__(self):
        super().__init__()  #初始化方法。super().__init__() 是调用父类的初始化方法。
        
        #创建标签页控件
        self.tabs = QTabWidget()
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.tabs.setFont(font)

        #创建状态栏
        self.statusBar().showMessage('Ready')

        #创建工具栏
        #创建菜单栏

        self.filePath = None  # 用于存储用户选择的文件路径

        #添加tab到主界面
        welcome_tab = self.create_welcome_tab()
        self.tabs.addTab(welcome_tab, "欢迎使用")

        data_extract_tab = self.create_data_extract_tab()
        self.tabs.addTab(data_extract_tab, "数据提取")

        data_analyse = self.create_data_analyse_tab()
        self.tabs.addTab(data_analyse, "数据分析")

        code_tab = self.create_code_tab()
        self.tabs.addTab(code_tab, "参数修改")

        browser_tab = self.create_browser_tab()
        self.tabs.addTab(browser_tab, "网页浏览")
        
        #主窗口的中央部件设置为标签页控件并显示主窗口
        self.setCentralWidget(self.tabs)
        self.setGeometry(600, 200, 850, 650)
        self.setWindowTitle('智能吊钩')         
        self.show()
    

    def create_welcome_tab(self):
        tab = QWidget()
        data_label1 = QLabel('<font size="30" style="color:green;"><b>欢迎使用</b></font>', tab)
        data_label2 = QLabel('<font size="5" style="color:red;"><b>此代码适配于智能吊钩的开发以及快捷处理</b></font>', tab)
        # 设置文本对齐方式为居中
        data_label1.setAlignment(Qt.AlignCenter)
        data_label2.setAlignment(Qt.AlignCenter)
        # 创建布局
        central_layout1 = QVBoxLayout(tab)
        h_layout1 = QHBoxLayout(tab)
        # 向水平布局中添加弹性空间和标签
        central_layout1.addStretch()
        central_layout1.addWidget(data_label1)
        central_layout1.addWidget(data_label2)
        central_layout1.addStretch()
        # 将水平布局添加到垂直布局中，并添加弹性空间
        h_layout1.addStretch()
        #h_layout1.addLayout(h_layout1)
        h_layout1.addStretch()
        # 将布局设置为容器（例如QWidget或QMainWindow）
        tab.setLayout(central_layout1)    
        return tab
    
    def create_data_extract_tab(self):
        tab = QWidget()
        data_label3 = QLabel('<font size="15" style="color:block;"><b>导入读取的txt数据进行分析</b></font>', tab)
        # 设置文本对齐方式为居中
        data_label3.setAlignment(Qt.AlignCenter)
        # 创建布局
        central_layout3 = QVBoxLayout(tab)
        h_layout3 = QHBoxLayout(tab)
        # 向水平布局中添加弹性空间和标签
        central_layout3.addStretch()
        central_layout3.addWidget(data_label3)
        central_layout3.addStretch()
        # 将水平布局添加到垂直布局中，并添加弹性空间
        h_layout3.addStretch()
        h_layout3.addLayout(h_layout3)
        h_layout3.addStretch()
        # 将布局设置为容器（例如QWidget或QMainWindow）
        tab.setLayout(central_layout3)    
        return tab
    
    def create_data_analyse_tab(self):
        tab = QWidget()

        data_label = QLabel('<font size="1" style="color:green;"><b>选择文件后点击确认，数据将处理完成，保留在原文件夹下</b></font>', tab)
        data_label.setAlignment(Qt.AlignCenter)

        load_button = QPushButton("上传数据文件", tab)
        load_button.clicked.connect(self.load_data)

        confirm_data_button = QPushButton("确认", tab)
        confirm_data_button.clicked.connect(self.confirm_data)


        # 创建布局
        layout = QVBoxLayout()

        # Add widgets to the layout
        layout.addStretch()
        layout.addWidget(data_label)
        layout.addWidget(load_button)
        layout.addWidget(confirm_data_button)
        layout.addStretch()

        tab.setLayout(layout)
        return tab

    def create_code_tab(self):
        tab = QWidget()
        # 创建滑块
        slider_kp = QSlider(Qt.Horizontal, tab)
        slider_ki = QSlider(Qt.Horizontal, tab)
        slider_kd = QSlider(Qt.Horizontal, tab)
        slider_max = QSlider(Qt.Horizontal, tab)
        slider_min = QSlider(Qt.Horizontal, tab)
        slider_motor = QSlider(Qt.Horizontal, tab)

        # 修改滑块初始性质
        slider_kp.setSingleStep(1)  # 设置步长为1   最后除以放大倍数
        slider_kp.setValue(11)  # 将滑块设置为50的位置
        slider_kp.setRange(0, 30)  # 设置滑块的范围为0到100

        slider_ki.setSingleStep(1)  
        slider_ki.setValue(6)  
        slider_ki.setRange(0, 30)  

        slider_kd.setSingleStep(1)  
        slider_kd.setValue(2)  
        slider_kd.setRange(0, 30)  

        slider_max.setSingleStep(1)  
        slider_max.setRange(1050, 1400)
        slider_max.setValue(1300) 

        slider_min.setSingleStep(1)  
        slider_min.setRange(900, 1050)
        slider_min.setValue(1000)
        
        slider_motor.setSingleStep(1)  
        slider_motor.setRange(0, 1)
        slider_motor.setValue(1)

        # 创建滑块标签
        label_kp = QLabel("KP", tab)
        label_ki = QLabel("KI", tab)
        label_kd = QLabel("KD", tab)
        label_max = QLabel("MAX", tab)
        label_min = QLabel("MIN", tab)
        label_motor = QLabel("motor:", tab)

        # 创建额外的标签来显示滑块的数值
        value_label_kp = QLabel("1.1", tab)
        value_label_ki = QLabel("0.6", tab)
        value_label_kd = QLabel("0.2", tab)
        value_label_max = QLabel("1300", tab)
        value_label_min = QLabel("1000", tab)
        value_label_motor = QLabel("开", tab)

        # 连接滑块的 valueChanged 信号到更新函数
        slider_kp.valueChanged.connect(lambda value: value_label_kp.setText(str(value/ 10.0)))
        slider_ki.valueChanged.connect(lambda value: value_label_ki.setText(str(value/ 10.0)))
        slider_kd.valueChanged.connect(lambda value: value_label_kd.setText(str(value/ 10.0)))
        slider_max.valueChanged.connect(lambda value: value_label_max.setText(str(value)))
        slider_min.valueChanged.connect(lambda value: value_label_min.setText(str(value)))
        slider_motor.valueChanged.connect(lambda value: value_label_motor.setText("开" if value == 1 else "关" if value == 0 else str(value)))

        # 创建按钮
        button_reset = QPushButton("恢复原始", tab)

        # TODO: 如果需要，连接按钮到相应的槽函数

        # 创建布局并添加控件
        layout3 = QGridLayout(tab)

        # 添加滑块、标签和数值标签到布局
        layout3.addWidget(label_kp, 0, 0)
        layout3.addWidget(slider_kp, 0, 1)
        layout3.addWidget(value_label_kp, 0, 2)

        layout3.addWidget(label_ki, 1, 0)
        layout3.addWidget(slider_ki, 1, 1)
        layout3.addWidget(value_label_ki, 1, 2)

        layout3.addWidget(label_kd, 2, 0)
        layout3.addWidget(slider_kd, 2, 1)
        layout3.addWidget(value_label_kd, 2, 2)

        layout3.addWidget(label_max, 3, 0)
        layout3.addWidget(slider_max, 3, 1)
        layout3.addWidget(value_label_max, 3, 2)

        layout3.addWidget(label_min, 4, 0)
        layout3.addWidget(slider_min, 4, 1)
        layout3.addWidget(value_label_min, 4, 2)

        layout3.addWidget(label_motor, 5,0)
        layout3.addWidget(slider_motor, 5,1)
        layout3.addWidget(value_label_motor, 5,2)
        # 添加按钮到布局

        layout3.addWidget(button_reset, 6, 0, 1, 2)

        
        tab.setLayout(layout3)
        return tab

    def create_browser_tab(self):
        tab = QWidget()
        browser = QWebEngineView()
        browser.load(QUrl("http://baidu.com"))
        url_input = QLineEdit(tab)
        url_input.setText("http://baidu.com")
        url_input.returnPressed.connect(self.load_browser_url)
        layout = QVBoxLayout(tab)
        layout.addWidget(url_input)
        layout.addWidget(browser)
        tab.setLayout(layout)
        return tab
    
    def confirm_data(self):
        # 用户点击 "确定" 按钮后的操作
        
        if self.filePath:
            # 调用 kalman_filter_processing 函数处理文件
            self.kalman_filter_processing(self.filePath)
            print("Data confirmed and processed!")  
    
    def extract_data(self):
        # 读取文件内容
        with open("D:\\Desktop\\减摇学习\\resource\\上位机\\563.TXT", "r", encoding="utf-8") as file:
            data = file.read()

        # 使用正则表达式提取数据
        pattern = r"x:([\d.-]+)°,\s+\|\s+y:([\d.-]+)°\s+\|\s+z:([\d.-]+)°,"
        matches = re.findall(pattern, data)

        # 转换为DataFrame
        df = pd.DataFrame(matches, columns=['x', 'y', 'z'])

        # 保存为Excel文件
        output_path = "D:\\Desktop\\减摇学习\\resource\\上位机\\angles_data_from_txt.xlsx"
        df.to_excel(output_path, index=False)

        output_path
            
    def load_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.statusBar().showMessage('数据导入成功')
            with open(file_name, 'r', encoding='utf-8') as file:
                data = file.read()
                self.data_label.setText(f"Loaded data from: {file_name}{data[:500]}...")  # Displaying first 500 chars
            
    
    def save_code(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Code", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                code = self.editor.toPlainText()
                file.write(code)
    
    def load_browser_url(self):
        url = self.url_input.text()
        self.browser.load(QUrl(url))   

    def kalman_filter_processing(input_file, 
                                 initial_state=0, 
                                 initial_estimate_error=1, 
                                 process_variance=1, 
                                 measurement_variance=1, 
                                 output_path="output.xlsx"):

        
        # Define the 1D Kalman filter
        def kalman_1d(initial_state, initial_estimate_error, process_variance, measurement_variance, measurements):
            n = len(measurements)
            estimates = np.zeros(n)
            estimate_errors = np.zeros(n)
            estimates[0] = initial_state
            estimate_errors[0] = initial_estimate_error

            for i in range(1, n):
                prediction = estimates[i-1]
                prediction_error = estimate_errors[i-1] + process_variance
                kalman_gain = prediction_error / (prediction_error + measurement_variance)
                estimates[i] = prediction + kalman_gain * (measurements[i] - prediction)
                estimate_errors[i] = (1 - kalman_gain) * prediction_error

            return estimates

        # Read the data from the provided file path
        with open(input_file, "r", encoding="utf-8") as file:
            data_txt_content = file.readlines()

        # Extract x, y, z data using regular expression
        x_data, y_data, z_data = [], [], []
        pattern = r"x:([\d.-]+)°,\s*\|\s*y:([\d.-]+)°\s*\|\s*z:([\d.-]+)°,"
        for line in data_txt_content:
            match = re.search(pattern, line)
            if match:
                x, y, z = map(float, match.groups())
                x_data.append(x)
                y_data.append(y)
                z_data.append(z)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame({'X': x_data, 'Y': y_data, 'Z': z_data})
        df['序号'] = df.index + 1

        # Apply Kalman filter to x, y, z data
        df['X_filtered'] = kalman_1d(initial_state, initial_estimate_error, process_variance, measurement_variance, df["X"].values)
        df['Y_filtered'] = kalman_1d(initial_state, initial_estimate_error, process_variance, measurement_variance, df["Y"].values)
        df['Z_filtered'] = kalman_1d(initial_state, initial_estimate_error, process_variance, measurement_variance, df["Z"].values)

        # Save the DataFrame to an Excel file
        df.to_excel(output_path, index=False)

        # Load the Excel workbook and add a line chart for the filtered data
        wb = openpyxl.load_workbook(output_path)
        ws = wb.active

        chart_filtered = LineChart()
        chart_filtered.title = "Filtered Angle Data for X, Y, and Z with 序号 as Time using Kalman Filter"
        chart_filtered.style = 13
        chart_filtered.x_axis.title = '序号'
        chart_filtered.y_axis.title = 'Angle (°)'

        # Add data to the chart
        for i, label in enumerate(['X_filtered', 'Y_filtered', 'Z_filtered'], 5):
            data = Reference(ws, min_col=i, min_row=2, max_col=i, max_row=len(df) + 1)
            chart_filtered.add_data(data, titles_from_data=True)

        # Set the chart's categories
        categories = Reference(ws, min_col=1, min_row=2, max_row=len(df) + 1)
        chart_filtered.set_categories(categories)
        ws.add_chart(chart_filtered, "F30")

        # Save the workbook with the chart
        wb.save(output_path)    

app = QApplication([])  #创建了一个 QApplication 对象
window = MyWindow()     #实例化了之前定义的 MyWindow 类
app.exec_()             #启动了应用程序的事件循环