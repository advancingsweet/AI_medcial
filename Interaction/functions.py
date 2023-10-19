import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import pandas as pd
class Function:

    @staticmethod
    def load_csv(file_path,label="all"):
        """
        读取csv文件
        :param file_path:   文件路径
        :return:
        """
        if not os.path.exists(file_path):
            QMessageBox.warning(p_str="警告",p_str_1=f"当前文件{file_path}不存在",QMessageBox_StandardButtons=QMessageBox.Close)
            return None
        data=pd.read_csv(file_path)

        if label=='all':
            return np.array(data)
        else:
            return np.array(data[label])

    @staticmethod
    def load_txt(file_path):
        if not os.path.exists(file_path):
            QMessageBox.warning(p_str="警告",p_str_1=f"当前文件{file_path}不存在",QMessageBox_StandardButtons=QMessageBox.Close)
            return None
        data_list=[]
        with open(file_path,'r',encoding='utf-8') as f:
            while True:
                line = f.readline()
                if line:
                    data_list.append(line.replace('\n',''))
                else:
                    break
        return np.array(data_list)

    @staticmethod
    def run_model(hla,t,mode):
        """
        :param hla:   hla
        :param t:     peptide or tcr
        :param mode:
        :return:
        """
        if mode == 'peptide':
            """
                peptide 预测模型
                
                return hla、peptide，bidding,socre
            """
            pass
        elif mode == 'tcr':
            """
                tcr 预测模型
                
                return hla,tcr,binding,score
            """
            pass

        elif mode == 'aomp':
            """
                aomp 预测模型
                
                return HLA Original peptide Mutated peptide Mutation amino-acid site
Mutation
number
Sequence
similarity Binding Prediction score
            """
            pass


if __name__ == '__main__':
    # file_path="pep_tcr_dataset.csv"
    # peptide=Function.load_csv(file_path,None,'peptide')
    l=['111','2966899','976665']
    print(np.array(l))



