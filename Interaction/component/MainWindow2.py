from PyQt5 import QtGui, QtCore
from ui.MainWindow2 import Ui_Form
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFile
import queue

import numpy as np
import pyqtgraph as pg
from component.ExprotWindow import ExportWindow

from functions import Function
from Threads import *




class MainWindow2(QWidget,Ui_Form):

    Export=pyqtSignal(dict,list)                        #导出
    Predict=pyqtSignal(np.ndarray,np.ndarray,str)  #预测

    hla=None
    peptide=None
    tcr=None

    def get_hla(self,result):
        self.hla=result

    def get_peptide(self,result):
        self.peptide=result

    def get_tcr(self,result):
        self.tcr=result

    def start_peptide_progressbar(self):
        self.peptideprogress.setVisible(True)
        self.peptideprogress.setValue(1)

    def send_value_peptide_progressbar(self,value):
        self.peptideprogress.setValue(value)

    def end_peptide_progressbar(self):
        self.peptideprogress.setValue(0)
        self.peptideprogress.setVisible(False)

    def setText_peptide_progressbar(self,text):
        self.peptideprogress.setFormat(text)

    def setText_valie_peptide_progressbar(self,value,text):
        self.peptideprogress.setValue(value)
        self.peptideprogress.setFormat(text)
    def start_tcr_progressbar(self):
        self.tcrprogress.setVisible(True)
        self.tcrprogress.setValue(1)

    def send_value_tcr_progressbar(self,value):
        self.tcrprogress.setValue(value)

    def end_tcr_progressbar(self):
        self.tcrprogress.setValue(0)
        self.tcrprogress.setVisible(False)

    def setText_tcr_progressbar(self,text):
        self.tcrprogress.setFormat(text)

    def setText_valie_tcr_progressbar(self,value,text):
        self.tcrprogress.setValue(value)
        self.tcrprogress.setFormat(text)

    def start_aomp_progressbar(self):
        self.Aompprogress.setVisible(True)
        self.Aompprogress.setValue(1)

    def send_value_aomp_progressbar(self,value):
        self.Aompprogress.setValue(value)

    def end_aomp_progressbar(self):
        self.Aompprogress.setValue(0)
        self.Aompprogress.setVisible(False)

    def setText_aomp_progressbar(self,text):
        self.Aompprogress.setFormat(text)

    def setText_valie_aomp_progressbar(self,value,text):
        self.Aompprogress.setValue(value)
        self.Aomprogress.setFormat(text)


    def Model_Predict(self,hla,t,mode):
        """
        预测peptide tcr
        :param hla:
        :param t:
        :param mode:
        :return:
        """
        result_dict={}
        if mode=="peptide":
            N=hla.shape[0]
            binding=np.zeros(shape=(N,))
            score,attn=Function.run_model(hla,t,mode)
            result_dict={
                'score': np.stack([hla,t,binding,score],axis=-1),
                "attn":  attn
            }
        elif mode=='tcr':
            N = hla.shape[0]
            score, attn = Function.run_model(hla, t, mode)
            result_dict = {
                'score': np.stack([hla, t,score], axis=-1),
                "attn": attn
            }
        return result_dict
        #self.show_data(result_dict, mode=mode)

    def Aomp_model(self,hla, peptide,mode="aomp"):
        #运行aomp模型

        result_dict={}
        return result_dict

    def __init__(self,*args,**kwargs):
        super(MainWindow2, self).__init__(*args,**kwargs)
        self.peptide_dict={}

        self.tcr_dict={}

        self.aomp_dict={}

        self.peptide_labels=["HLA","Peptide","Binding","Peptide Score"]

        self.tcr_labels=["Peptide","Tcr","Tcr Score"]

        self.aomp_labels=["HLA","Original Peptide","Mutated Peptide","Mutation amino-acid site",
                          "Mutation number","Sequence similarity","Binding","Prediction score"
                          ]


        self.setupUi(self)


        self.stack=queue.LifoQueue()
        #主窗口透明
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #home按钮
        self.homebtn.clicked.connect(self.stackedWidget_switch_home)
        self.backbtn.clicked.connect(self.stackedWidget_switch_last)
        self.peptidebtn.clicked.connect(self.stackedWidget_switch_peptide)
        self.tcrbtn.clicked.connect(self.stackedWidget_switch_tcr)
        self.aompbtn.clicked.connect(self.stackedWidget_switch_aomp)
        self.modelbtn.clicked.connect(self.stackedWidget_switch_peptide)
        self.settingbtn.clicked.connect(self.stackedWidget_switch_tcr)
        self.writingbtn.clicked.connect(self.stackedWidget_switch_aomp)

        #隐藏进度条
        self.peptideprogress.setVisible(False)
        self.tcrprogress.setVisible(False)
        self.Aompprogress.setVisible(False)

        #self.peptideGraphArea.
        #肽预测
        self.peptide_window()
        #tcr预测
        self.tcr_window()
        #aomp
        self.aomp_window()

        self.test()

        #self.stackedWidget.currentChanged

    def switch_checked(self):
        if self.stackedWidget.currentIndex()==0:
            self.homebtn.setChecked(False)
        elif self.stackedWidget.currentIndex()==1:
            self.homebtn.setChecked(False)
        elif self.stackedWidget.currentIndex()==2:
            self.tcrbtn.setChecked(False)
        elif self.stackedWidget.currentIndex()==3:
            self.aompbtn.setChecked(False)

    def stackedWidget_switch_home(self):
        if self.stackedWidget.currentIndex()!=0:
            self.stack.put_nowait(self.stackedWidget.currentIndex())
            self.stackedWidget.setCurrentIndex(0)

    def stackedWidget_switch_last(self):
        if not self.stack.empty():
            self.stackedWidget.setCurrentIndex(self.stack.get_nowait())

    def stackedWidget_switch_peptide(self):
        self.stack.put_nowait(self.stackedWidget.currentIndex())
        self.stackedWidget.setCurrentIndex(1)

    def stackedWidget_switch_tcr(self):
        self.stack.put_nowait(self.stackedWidget.currentIndex())
        self.stackedWidget.setCurrentIndex(2)


    def stackedWidget_switch_aomp(self):

        self.stack.put_nowait(self.stackedWidget.currentIndex())
        self.stackedWidget.setCurrentIndex(3)

    def stackedWidget_switch_model(self):
        self.stack.put_nowait(self.stackedWidget.currentIndex())
        self.stackedWidget.setCurrentIndex(4)

    def stackedWidget_switch_setting(self):
        self.stack.put_nowait(self.stackedWidget.currentIndex())
        self.stackedWidget.setCurrentIndex(5)

    #-----------肽预测----------------
    def peptide_window(self):
        #self.peptideresult.setItem(0,0,QTableWidgetItem("test"))
        #self.test()
        self.inputHLA1.setToolTip("请输入HLA或存储HLA的文件")
        self.inputPeptide.setToolTip("请输入Peptide或存储Peptide的文件")

        header=self.peptideresult.horizontalHeader()
        header.setStyleSheet("background-color: rgb(27, 53, 113);")

        def openFileHla():
            file_path=QFileDialog.getOpenFileName(parent=self,caption="选择打开文件",filter="(*.txt *.csv)")[0]
            if file_path != '':
                self.inputHLA1.setText('file:'+file_path)

        def openFilePeptide():
            file_path=QFileDialog.getOpenFileName(parent=self,caption="选择打开文件",filter="(*.txt *.csv)")[0]
            if file_path !='':
                self.inputPeptide.setText("file:"+file_path)
        self.peptide_hla_folderbtn.clicked.connect(openFileHla)
        self.peptide_peptide_folderbtn.clicked.connect(openFilePeptide)

        def clear():
            self.peptide_dict.clear()
            self.peptideresult.clearContents()
            self.peptideresult.setRowCount(0)
            self.peptideGraphArea.widget().close()
        self.peptideRefresh.clicked.connect(clear)

        def Export():
            # if 'score' not in self.peptide_dict.keys() or 'attn' not in self.peptide_dict.keys():
            #     QMessageBox.warning(self,"警告","未找到相关内容!",QMessageBox.Close)
            #     return
            self.Export.emit(self.peptide_dict,self.peptide_labels)
        self.peptideExport.clicked.connect(Export)

        def Predict():
            hla_path=self.inputHLA1.text()
            peptide_path=self.inputPeptide.text()
            self.start_peptide_progressbar()
            if hla_path.startswith('file:') :
                self.setText_peptide_progressbar("正在加载HLA文件")
                path=hla_path.split(":",1)[-1]
                filetype=path.split('.')[-1]
                if filetype=="txt":
                    thread1=Load_File_Thread(Function.load_txt,50,"HLA获取完成",*[path])
                    thread1.loaded.connect(self.get_hla)
                    thread1.end.connect(self.setText_valie_peptide_progressbar)
                    thread1.run()

                elif filetype=="csv":
                    thread1=Load_File_Thread(Function.load_csv,50,"HLA获取完成",*[path,"HLA_sequence"])
                    thread1.loaded.connect(self.get_hla)
                    thread1.end.connect(self.setText_valie_peptide_progressbar)
                    thread1.run()

                hla=self.hla
            elif not hla_path.startswith("file:") and hla_path != '':
                #单个hla
                self.setText_valie_peptide_progressbar(50,"HLA获取完成")
                hla=np.array([hla_path])
            self.send_value_peptide_progressbar(30)

            if peptide_path.startswith("file:"):
                #读取文件
                self.setText_peptide_progressbar("正在加载tcr文件")
                path = peptide_path.split(":", 1)[-1]
                filetype = path.split('.')[-1]
                if filetype == "txt":
                    thread2=Load_File_Thread(Function.load_txt,100,"Peptide获取完成",*[path])
                    thread2.loaded.connect(self.get_peptide)
                    thread2.end.connect(self.setText_valie_peptide_progressbar)
                    thread2.run()
                elif filetype == "csv":
                    thread2=Load_File_Thread(Function.load_csv,100,"Peptide获取完成",*[path,"peptide"])
                    thread2.loaded.connect(self.get_peptide)
                    thread2.end.connect(self.setText_valie_peptide_progressbar)
                    thread2.run()
                peptide=self.peptide
            elif peptide_path != '':
                self.setText_valie_peptide_progressbar(100,"Peptide获取完成")
                peptide=np.array([peptide_path])

            if peptide_path=='' or hla_path=='':
                self.end_peptide_progressbar()
                return

            self.start_peptide_progressbar()
            self.setText_peptide_progressbar("正在运行模型")
            thread3=Predict_Model_Thread(self.Model_Predict,*[hla,peptide,'peptide'])
            thread3.over.connect(self.show_data)
            # QWaitCondition()
            thread3.run()
            #Function.run_model(hla,peptide,"peptide")
        self.predictPeptide.clicked.connect(Predict)


    def tcr_window(self):
        self.inputHLA2.setToolTip("请输入HLA或存储HLA的文件")
        self.inputTcr.setToolTip("请输入Peptide或存储Peptide的文件")

        def openFileHla():
            file_path = QFileDialog.getOpenFileName(parent=self, caption="选择打开文件", filter="(*.txt *.csv)")[0]
            if file_path != '':
                self.inputHLA2.setText('file:' + file_path)

        def openFilePeptide():
            file_path = QFileDialog.getOpenFileName(parent=self, caption="选择打开文件", filter="(*.txt *.csv)")[0]
            if file_path != '':
                self.inputTcr.setText("file:" + file_path)

        self.tcr_hla_folderbtn.clicked.connect(openFileHla)
        self.tcr_tcr_folderbtn.clicked.connect(openFilePeptide)

        def clear():
            self.tcr_dict.clear()
            self.peptideresult.clearContents()
            self.tcrresult.setRowCount(0)
            self.tcrGraphArea.widget().close()

        self.tcrRefresh.clicked.connect(clear)


        def Predict():
            peptide_path=self.inputHLA2.text()
            tcr_path=self.inputTcr.text()
            self.start_tcr_progressbar()
            if peptide_path.startswith('file:'):
                self.setText_tcr_progressbar("正在加载peptide文件")
                path=peptide_path.split(":",1)[-1]
                filetype=path.split('.')[-1]
                if filetype=="txt":
                    thread1=Load_File_Thread(Function.load_txt,50,"peptide获取完成",*[path])
                    thread1.loaded.connect(self.get_peptide)
                    thread1.end.connect(self.setText_valie_tcr_progressbar)
                    thread1.run()
                elif filetype=="csv":
                    thread1=Load_File_Thread(Function.load_csv,50,"tcr获取完成",*[path,"peptide"])
                    thread1.loaded.connect(self.get_peptide)
                    thread1.end.connect(self.setText_valie_tcr_progressbar)
                    thread1.run()
                peptide=self.peptide
            elif peptide_path != '':
                #单个peptide
                self.setText_valie_tcr_progressbar(50,"tcr获取完成")
                peptide=np.array([peptide_path])

            if tcr_path.startswith("file:"):
                #读取文件
                self.setText_tcr_progressbar("正在加载tcr文件")
                path = tcr_path.split(":", 1)[-1]
                filetype = path.split('.')[-1]
                if filetype == "txt":
                    thread2=Load_File_Thread(Function.load_txt,100,"tcr获取完成",*[path])
                    thread2.loaded.connect(self.get_tcr)
                    thread2.end.connect(self.setText_valie_tcr_progressbar)
                    thread2.run()
                elif filetype == "csv":
                    thread2=Load_File_Thread(Function.load_csv,100,'tcr获取完成',*[path,"tcr"])
                    thread2.loaded.connect(self.get_tcr)
                    thread2.end.connect(self.setText_valie_tcr_progressbar)
                    thread2.run()
                tcr=self.tcr
            elif tcr_path != '':
                self.setText_valie_tcr_progressbar(100,"tcr获取完成")
                tcr=np.array([tcr_path])

            if tcr_path=='' or peptide_path=='':
                self.end_tcr_progressbar()
                return
            thread3 = Predict_Model_Thread(self.Model_Predict, *[ peptide,tcr, 'tcr'])
            thread3.over.connect(self.show_data)
            thread3.run()
            #Function.run_model(hla,peptide,"peptide")
        self.predictTcr.clicked.connect(Predict)

        def Export():
            # if 'score' not in self.tcr_dict.keys() or 'attn' not in self.tcr_dict.keys():
            #     QMessageBox.warning(self,"警告","未找到相关内容",QMessageBox.Close)
            #     return
            # export=ExportWindow(self.tcr_dict,parent=self)
            # export.show()
            self.Export.emit(self.tcr_dict,self.tcr_labels)
        self.TcrExport.clicked.connect(Export)

    def aomp_window(self):
        self.aomphistogram.setVisible(False)

        def clear():
            self.aomp_dict.clear()
            self.aompResult.clearContents()
            self.aompResult.setRowCount(0)
            self.aompGraphArea.widget().close()
            self.aomphistogram.removeItem()
            self.aomphistogram.setVisible(False)

        self.AompRefresh.clicked.connect(clear)

        def Export():
            # if 'score' not in self.aomp_dict.keys() or 'attn' not in self.aomp_dict.keys():
            #     QMessageBox.warning(self,"警告","未找到相关内容",QMessageBox.Close)
            #     return
            # export=ExportWindow(self.tcr_dict,parent=self)
            # export.show()
            self.Export.emit(self.aomp_dict,self.aomp_labels)

        self.AompExport.clicked.connect(Export)

        def Predict():
            hla=self.inputHLA3.text()
            peptide=self.inputPeptide2.text()
            if hla=="" or peptide=="":
                QMessageBox.information(self,"提示","请输入HLA 和 Peptide ！",QMessageBox.Close)
                return

            #开启一个线程运行模型
            #thread=Predict_Model_Thread(self.Aomp_model,*[hla,peptide])

        self.predictAomp.clicked.connect(Predict)

    def show_data(self,dict,mode,append=False):
        if mode == "peptide":
            self.setText_peptide_progressbar("正在展示数据")
            self.send_value_peptide_progressbar(90)
            self.peptide_show_data(dict,append)
        elif mode == 'tcr':
            self.setText_tcr_progressbar("正在展示数据")
            self.send_value_tcr_progressbar(90)
            self.tcr_show_data(dict,append)
        elif mode=='aomp':
            self.setText_aomp_progressbar("正在展示数据")
            self.send_value_aomp_progressbar(90)
            self.aomp_show_data(dict,append)
        self.end_peptide_progressbar()

    def peptide_show_data(self,dict,append=False):
        """
        :param dict:  数据字典
                    {
                        score:[[],[],[]]            #(N,4)
                        attn:[[[],[]],[],[]]        #(N,h,w)
                    }
        :return:
        """
        if self.peptide_append.checkState()==Qt.Checked:
            append=True
        scores=dict['score']
        attns=dict['attn']

        scores=np.array(scores) if isinstance(scores,list) else scores
        attns=np.array(attns) if isinstance(attns,list) else scores

        if append:
            if self.peptide_dict != None:
                scores=np.concatenate([self.peptide_dict['score'],scores],axis=0)
                attns=np.concatenate([self.peptide_dict["attn"],attns],axis=0)

        #清空原来的内容
        self.peptideresult.clearContents()
        self.peptideresult.setRowCount(0)
        self.peptideGraphArea.widget().close()
        self.peptideresult.setRowCount(scores.shape[0])

        a = QWidget()
        b = QVBoxLayout()
        a.setLayout(b)
        for i in range(scores.shape[0]):
            #将数据送入表格
            hla=scores[i][0]
            peptide=scores[i][1]
            for j in range(scores[i].shape[-1]):
                item = QTableWidgetItem(str(scores[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.peptideresult.setItem(i, j, item)

            #热力图
            attn=attns[i]
            win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples", parent=self.peptideGraphArea)
            win.setFixedSize(440,200)
            win.setBackground('w')
            #plt = win.addPlot(title=f"HeatMap:{hla}-{peptide}:")
            xlabels = [(i, c) for i, c in enumerate(hla)]
            ylabels = [(i, c) for i, c in enumerate(peptide)]
            img = pg.ImageItem(attn)

            xAxis = pg.AxisItem(orientation="bottom")
            xAxis.setTicks([xlabels])
            yAxis = pg.AxisItem(orientation="left")
            yAxis.setTicks([ylabels])

            plt = win.addPlot(title=f"HeatMap:{hla}-{peptide}:",axisItems={
                'bottom':xAxis,
                'left': yAxis,
            })
            plt.addItem(img)
            #plt.tight_layout()
            #img.setRect(QtCore.QRectF(50, 50, 300, 300))
            #plt.setRect(QtCore.QRectF(50, 50, 300, 300))
            color_map=pg.ColorMap(None,color=[
                QtGui.QColor(68, 2, 86),
                QtGui.QColor(63, 71, 136),
                QtGui.QColor(40, 112, 141),
                QtGui.QColor(32, 163, 132),
                QtGui.QColor(121, 209, 81),
                QtGui.QColor(245, 229, 32),
            ])

            plt.addColorBar(img, colorMap=color_map,values=(0, 1))
            # plt.setXRange()
            # plt.setYRange()
            b.addWidget(win)

        self.peptideGraphArea.setWidget(a)
        self.peptide_dict['score'] = scores
        self.peptide_dict['attn'] = attns

    def test(self):
        attn1=np.random.uniform(0,1,size=(10,9))
        attn2=np.random.uniform(0,1,size=(10,9))
        attn3=np.random.uniform(0,1,size=(10,9))
        dict={
            "score":[['1111111111','222222222',3,4],['3456321456','987654789',7,8],['12hfvc6780','xncbv1234',11,12]],
            "attn":[
                    attn1,
                    attn2,
                    attn3,
            ]
        }
        self.show_data(dict,'peptide')

    def tcr_show_data(self,dict,append=False):
        scores = dict['score']
        attns = dict['attn']
        if self.tcr_append.checkState()==Qt.Checked:
            append=True

        scores=np.array(scores) if isinstance(scores,list) else scores
        attns=np.array(attns) if isinstance(attns,list) else attns

        if append:
            if self.tcr_dict != None:
                scores=np.concatenate([self.tcr_dict['score'],scores],axis=0)
                attns=np.concatenate([self.tcr_dict["attn"],attns],axis=0)

        #清除原来的内容
        self.tcrresult.clearContents()
        self.tcrresult.setRowCount(0)
        self.tcrGraphArea.widget().close()

        self.tcrresult.setRowCount(scores.shape[0])
        a = QWidget()
        b = QVBoxLayout()
        a.setLayout(b)
        for i in range(scores.shape[0]):
            # 将数据送入表格
            hla = scores[i][0]
            tcr = scores[i][1]
            for j in range(scores[i].shape[-1]):
                item=QTableWidgetItem(str(scores[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.tcrresult.setItem(i,j,item)
            # self.tcrresult.setItem(i, 0, QTableWidgetItem(str(hla)))
            # self.tcrresult.setItem(i, 1, QTableWidgetItem(str(tcr)))
            # self.tcrresult.setItem(i, 2, QTableWidgetItem(str(binding)))
            # self.tcrresult.setItem(i, 3, QTableWidgetItem(str(tcr_scores)))
        # 热力图
            attn = attns[i]
            win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples", parent=self.tcrGraphArea)
            win.setFixedSize(440, 200)
            win.setBackground('w')
            #plt = win.addPlot(title=f"HeatMap:{hla}-{tcr}:")
            xlabels = [(i,c) for i,c in enumerate(hla)]
            ylabels = [(i,c) for i,c in enumerate(tcr)]
            img = pg.ImageItem(attn)

            xAxis = pg.AxisItem(orientation="bottom")
            xAxis.setTicks([xlabels])
            yAxis = pg.AxisItem(orientation="left")
            yAxis.setTicks([ylabels])

            plt = win.addPlot(title=f"HeatMap:{hla}-{tcr}:",axisItems={
                'bottom':xAxis,
                'left': yAxis,
            })
            plt.addItem(img)
            color_map = pg.ColorMap(None, color=[
                QtGui.QColor(68, 2, 86),
                QtGui.QColor(63, 71, 136),
                QtGui.QColor(40, 112, 141),
                QtGui.QColor(32, 163, 132),
                QtGui.QColor(121, 209, 81),
                QtGui.QColor(245, 229, 32),
            ])
            plt.addColorBar(img, colorMap=color_map, values=(-1, 1))
            # y=plt.getAxis('left')
            # y.setTicks([ylaels])
            # x=plt.getAxis('bottom')
            # x.setTicks(xlabels)

            b.addWidget(win)
        self.tcrGraphArea.setWidget(a)
        self.tcr_dict['score'] = scores
        self.tcr_dict['attn'] = attns


    def aomp_show_data(self,dict,append=False):
        self.aomphistogram.setVisible(True)
        scores=dict["score"] if "score" in dict.keys() else None
        attns=dict['attn']   if 'attn' in dict.keys() else None
        if scores==None or attns ==None:
            return

        #清除原来的内容
        self.aompResult.clearContents()
        self.aompResult.setRowCount(0)
        self.aompGraphArea.widget().close()
        self.aomphistogram.removeItem()

        hla=scores[0][0]
        self.aomp_dict['score']=scores
        self.aomp_dict["attn"]=attns

        self.aompResult.setRowCount(len(scores))

        a=QWidget()
        b=QVBoxLayout()
        a.setLayout(b)
        temp_list=[]

        scores_list=[]
        #hla_list=[]
        peptide_list=[]

        for i in range(len(self.scores)):
            hla=scores[i][0]
            # original_peptide=scores[i][1]
            mutated_peptide=scores[i][2]
            # mutation_amino_acid_site=scores[i][3]
            # mutation_number=scores[i][4]
            # sequence_similarity=scores[i][5]
            # binding=scores[i][6]
            # prediction_score=scores[i][7]
            #hla_list.append(hla)
            peptide_list.append(mutated_peptide)
            scores_list.append(scores[i][-1])

            for j in range(len(scores[i])):
                item=QTableWidgetItem(str(scores[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.aompResult.setItem(i,j,item)

            #热力图
            attn=attns[i]
            temp_list.append(attn)
            if len(temp_list)==2:
                c=QHBoxLayout()
                for item in temp_list:
                    win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples", parent=self.tcrGraphArea)
                    win.setFixedSize(300, 150)
                    win.setBackground('w')
                    xlabels = [(i, c) for i, c in enumerate(hla)]
                    ylabels = [(i, c) for i, c in enumerate(mutated_peptide)]
                    img = pg.ImageItem(attn)

                    xAxis = pg.AxisItem(orientation="bottom")
                    xAxis.setTicks([xlabels])
                    yAxis = pg.AxisItem(orientation="left")
                    yAxis.setTicks([ylabels])

                    plt = win.addPlot(title=f"HeatMap:{hla}-{mutated_peptide}:", axisItems={
                        'bottom': xAxis,
                        'left': yAxis,
                    })
                    plt.addItem(img)
                    color_map = pg.ColorMap(None, color=[
                        QtGui.QColor(68, 2, 86),
                        QtGui.QColor(63, 71, 136),
                        QtGui.QColor(40, 112, 141),
                        QtGui.QColor(32, 163, 132),
                        QtGui.QColor(121, 209, 81),
                        QtGui.QColor(245, 229, 32),
                    ])
                    plt.addColorBar(img, colorMap=color_map, values=(0, 1))

                    c.addWidget(win)
                    temp_list.remove(item)
                b.addLayout(c)
        self.aompGraphArea.setWidget(a)

        #统计直方图
        #xlabels = [(i, c) for i, c in enumerate(hla_list)]
        xlabels = [(i, c) for i, c in enumerate(peptide_list)]
        xAxis = pg.AxisItem(orientation="bottom")
        xAxis.setTicks([xlabels])

        baritem=pg.BarGraphItem(x=np.arange(len(peptide_list)),height=scores_list,width=0.6)
        plt=self.aomphistogram.addPlot(title=f"{hla}",axisItems={
                'bottom':xAxis,
            })
        plt.addItem(baritem)
        #plt.addColorBar(img, colorMap='CET-R4', values=(-1, 1))
        self.aomp_dict=dict
