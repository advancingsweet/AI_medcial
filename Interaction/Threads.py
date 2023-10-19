from PyQt5.QtCore import *
import numpy as np

lock=QMutex()

class Load_File_Thread(QThread):

    loaded=pyqtSignal(np.ndarray)
    end=pyqtSignal(int,str)

    def __init__(self,func,end_value=None,end_text=None,*args):
        super(Load_File_Thread, self).__init__()
        self.func=func
        self.args=args
        self.end_value=end_value
        self.end_text=end_text

    def run(self):
        lock.lock()
        result=self.func(*self.args)
        lock.unlock()
        self.loaded.emit(result)
        if self.end_value!=None and self.end_text!=None:
            self.end.emit(self.end_value,self.end_text)

class Predict_Model_Thread(QThread):

    over=pyqtSignal(dict,str,bool)
    """
        score，attn
    """
    end=pyqtSignal(int,str)
    def __init__(self,func,*args):
        super(Predict_Model_Thread, self).__init__()
        self.func=func
        self.args=args
        self.mode=args[-1]

    def run(self):
        result_dict=self.func(*self.args)
        self.over.emit(result_dict,self.mode,False)
