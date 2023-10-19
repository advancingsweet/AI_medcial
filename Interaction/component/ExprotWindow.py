import os.path
from ui.ExportWindow import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd

class ExportWindow(QWidget,Ui_Form):

    def Export_Slot(self,dict,labels):
        #清空原来的数据
        self.ExportDataPath.setText("")
        self.ExportDataPath_2.setText("")
        while self.score_root.childCount()>0:
            self.score_root.removeChild(self.score_root.child(0))
        while self.attn_root.childCount()>0:
            self.attn_root.removeChild(self.attn_root.child(0))
        self.dict=dict
        self.labels=labels
        self.deal_data(dict)
        self.show()

    def __init__(self,*args,**kwargs):
        super(ExportWindow, self).__init__(*args,**kwargs)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setupUi(self)
        self.dict=None
        self.labels=None

        self.exportbtn.clicked.connect(self.Export_Data)
        self.ExportDatabtn.clicked.connect(self.get_file_path1)
        self.ExportDatabtn_2.clicked.connect(self.get_file_path2)

        self.init_treeWidget()

    def get_file_path1(self):
        file_path=QFileDialog.getOpenFileName(self,caption="请选择文件",filter="(*.txt *.xls *.xlsx *.csv)")[0]
        self.ExportDataPath.setText(file_path)

    def get_file_path2(self):
        file_path=QFileDialog.getOpenFileName(self,caption="请选择文件",filter="(*.pdf *.png)")[0]
        self.ExportDataPath_2.setText(file_path)

    def init_treeWidget(self):
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['选中','内容'])
        self.score_root = QTreeWidgetItem(self.treeWidget)
        self.attn_root = QTreeWidgetItem(self.treeWidget)
        self.score_root.setText(0, "Scores")
        self.attn_root.setText(0, "Attns")

    # def init_frame(self):
    #     self.treeWidget.setColumnCount(2)
    #     self.score_root = QTreeWidgetItem(self.treeWidget)
    #     self.attn_root = QTreeWidgetItem(self.treeWidget)
    #     self.score_root.setText(0, "Scores")
    #     self.attn_root.setText(0, "Attns")
    #处理数据
    def deal_data(self,dict):
        #self.init_treeWidget()
        # if dict==None:
        #     QMessageBox.warning(self,"警告","导出数据为空",QMessageBox.Close)
        #     return
        if 'score' not in dict.keys() or 'attn' not in dict.keys():
            return
        scores=dict['score']
        attns=dict['attn']
        for i in range(len(scores)):
            score=scores[i]
            attn=attns[i]
            hla=score[0]
            t=score[1] if len(scores[i]) < 8 else score[2]
            pred=score[-1]

            item1=QTreeWidgetItem(self.score_root)
            item1.setCheckState(0,Qt.CheckState.Checked)
            item1.setText(1,f"{hla}-{t} => {pred}")

            item2 = QTreeWidgetItem(self.attn_root)
            item2.setCheckState(0, Qt.CheckState.Checked)
            item2.setText(1, f"{hla}-{t}")

    def Export_Data(self):
        if self.dict==None or "score" not in self.dict.keys() or "attn" not in self.dict.keys():
            QMessageBox.warning(self,"警告","导出内容不能为空",QMessageBox.Close)
            return
        export_score=[]
        export_attns=[]
        #导出数据
        if self.ExportDataPath.text()!="":
            for i in range(self.score_root.childCount()):
                item=self.score_root.child(i)
                if item.checkState(0)==Qt.Checked:
                    export_score.append(self.dict["score"][i])
            if os.path.exists(self.ExportDataPath.text()):
                button=QMessageBox.warning(self,"警告","当前文件已存在,是否需要覆盖?",QMessageBox.Yes | QMessageBox.No)
                if button == QMessageBox.No:
                    QMessageBox.information(self,"提示","导出已取消,请重新选择文件路径",QMessageBox.Close)
                else:
                    filetype=self.ExportDataPath.text().split(".",1)[-1]
                    if filetype=="txt":
                        with open(self.ExportDataPath.text(),'w',encoding='utf-8') as f:
                            for item in export_score:
                                con=str(item[0])+','+str(item[1])+','+str(item[2])+','+str(item[3])
                                f.write(con+'\n')
                    elif filetype=="csv":
                        #导出csv文件
                        s=pd.DataFrame(data=export_score,columns=self.labels)
                        s.to_csv(self.ExportDataPath.text())
                    else:
                        QMessageBox.warning(self,"警告",f"当前文件格式不支持{self.ExportDataPath.text()}",QMessageBox.Close)
                        return
            else:
                filetype = self.ExportDataPath.text().split(".", 1)[-1]
                if filetype == "txt":
                    with open(self.ExportDataPath.text(), 'w', encoding='utf-8') as f:
                        for item in export_score:
                            con = str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + ',' + str(item[3])
                            f.write(con + '\n')
                elif filetype == "csv":
                    s = pd.DataFrame(data=export_score, columns=self.labels)
                    s.to_csv(self.ExportDataPath.text())
                else:
                    QMessageBox.warning(self, "警告", f"当前文件格式不支持{self.ExportDataPath.text()}", QMessageBox.Close)
                    return

        #导出图片
        if self.ExportDataPath_2.text()!="":
            for i in range(self.attn_root.childCount()):
                item=self.attn_root.child(i)
                if item.checkState(0)==Qt.Checked:
                    title=item.text(1)
                    export_attns.append((self.dict["attn"][i],title))
            if os.path.exists(self.ExportDataPath_2.text()):
                button=QMessageBox.warning(self,"警告","当前文件已存在,是否需要覆盖?",QMessageBox.Yes | QMessageBox.No)
                if button == QMessageBox.No:
                    QMessageBox.information(self,"提示","导出已取消,请重新选择文件路径",QMessageBox.Close)
                    return

                else:
                    filetype = self.ExportDataPath_2.text().split(".", 1)[-1]
                    if filetype=='pdf':
                        with PdfPages(self.ExportDataPath_2.text()) as pp:
                            for attn,title in export_attns:
                                plt.figure()
                                plt.clf()
                                plt.imshow(attn.T,vmin=0,vmax=1)
                                graph = plt.title(title)
                                plt.tight_layout()
                                plt.colorbar()
                                hla,t=title.split("-")
                                xticks=[c for c in hla]
                                yticks=[c for c in t]
                                plt.xticks(np.arange(len(xticks)),labels=xticks)
                                plt.yticks(np.arange(len(yticks)),labels=yticks)
                                pp.savefig(plt.gcf())
                    else:
                        QMessageBox.warning(self, "警告", f"当前文件格式不支持{self.ExportDataPath_2.text()}", QMessageBox.Close)
                        return
            else:
                filetype = self.ExportDataPath_2.text().split(".", 1)[-1]
                if filetype == 'pdf':
                    with PdfPages(self.self.ExportDataPath_2.text()) as pp:
                        for attn, title in export_attns:
                            plt.figure()
                            plt.clf()
                            plt.imshow(attn.T,vmin=0,vmax=1)
                            plt.title(title)
                            plt.tight_layout()
                            plt.colorbar()
                            hla, t = title.split("-")
                            xticks = [c for c in hla]
                            yticks = [c for c in t]
                            plt.xticks(np.arange(len(xticks)), labels=xticks)
                            plt.yticks(np.arange(len(yticks)), labels=yticks)
                            pp.savefig(plt.gcf())
                else:
                    QMessageBox.warning(self, "警告", f"当前文件格式不支持{self.ExportDataPath_2.text()}", QMessageBox.Close)
                    return
        QMessageBox.information(self,"提示","导出完成",QMessageBox.Close)


















