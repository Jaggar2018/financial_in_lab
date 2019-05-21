import os
import cv2
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn.neighbors import KNeighborsClassifier
from mlxtend.classifier import StackingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix, classification_report

def load_feature():
    X = []
    Y = []
    df1 = pd.read_csv('C:/Users/Jagga/Documents/feature_pore.csv',header=0)
    df2 = pd.read_csv('C:/Users/Jagga/Documents/feature_backgroud.csv',header=0)
    df1 = df1.drop(columns='Unnamed: 0')
    df2 = df2.drop(columns='Unnamed: 0')
    col1 = len(df1)
    col2 = len(df2)
    df1 = df1.T
    df1 = df1.reset_index()
    df2 = df2.T
    df2 = df2.reset_index()
    for i in range(col1):
        X.append(df1[i].tolist())
        Y.append(0)
    for i in range(col2):
        X.append(df2[i].tolist())
        Y.append(1)
    print("already load features")
    return X,Y
    #  columns = ['Pixel_0707','Pixel_0708','Pixel_0709','Pixel_0710','Pixel_0711','Pixel_0712',
    #                'Pixel_0807','Pixel_0808','Pixel_0809','Pixel_0810','Pixel_0811','Pixel_0812',
    #                'Pixel_0907','Pixel_0908','Pixel_0909','Pixel_0910','Pixel_0911','Pixel_0912',
    #                'Pixel_1007','Pixel_1008','Pixel_1009','Pixel_1010','Pixel_1011','Pixel_1012',
    #                'Pixel_1107','Pixel_1108','Pixel_1109','Pixel_1110','Pixel_1111','Pixel_1112',
    #                'Pixel_1207','Pixel_1208','Pixel_1209','Pixel_1210','Pixel_1211','Pixel_1212',
    #                'P36_Mean', 'P36_Median', 'P36_Max', 'P36_Min', 'P36_argMax', 'P36_argMin',
    #                'P36_0909_Degree', 'P36_0910_Degree', 'P36_1009_Degree', 'P36_1010_Degree',
    #                'P16_Mean', 'P16_Median', 'P16_Max', 'P16_Min', 'P16_argMax', 'P16_argMin',
    #                'P16_0909_Degree', 'P16_0910_Degree', 'P16_1009_Degree', 'P16_1010_Degree',
    #                'WhiteIncrease_36To16','WhiteIncrease_16To4']


def load_data_hog():
    X = []
    Y = []
    path1 = 'C:/Users/Jagga/Desktop/DIP/task2img/poresimg/'
    path2 = 'C:/Users/Jagga/Desktop/DIP/task2img/backgroundimg/'
    winSize = (64,64)
    blockSize = (16,16)
    blockStride = (8,8)
    cellSize = (8,8)
    nbins = 9
    derivAperture = 1
    winSigma = 4.
    histogramNormType = 0
    L2HysThreshold = 2.0000000000000001e-01
    gammaCorrection = 0
    nlevels = 64
    hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
                            histogramNormType,L2HysThreshold,gammaCorrection,nlevels)
    winStride = (8,8)
    padding = (8,8)
    locations = ((10,20),(30,30),(50,50),(70,70),(90,90),(110,110),(130,130),(150,150),(170,170),(190,190))

    print("construct positive sample ......")
    for f in os.listdir(path1):
        img = cv2.imread(path1+f)
        height = len(img)
        width = len(img[0])
        img = img[int(height*1/3):int(height*2/3), int(width*1/3):int(width*2/3)]
        hist = hog.compute(img, winStride, padding, locations)
        samples = (hist/255).flatten()
        samples = list(samples)
        hist = cv2.calcHist([img], [0], None, [256], [0, 255])
        samples.extend(list((hist / 255).flatten()))
        samples = np.array(samples)
        X.append(samples)
        Y.append(0)
    print("have already construct positive sample")

    print("construct negative sample......")
    for f in os.listdir(path2):
        img = cv2.imread(path2+f)
        height = len(img)
        width = len(img[0])
        img = img[int(height*1/3):int(height*2/3), int(width*1/3):int(width*2/3)]
        hist = hog.compute(img, winStride, padding, locations)
        samples = (hist / 255).flatten()
        samples = list(samples)
        hist = cv2.calcHist([img], [0], None, [256], [0, 255])
        samples.extend(list((hist / 255).flatten()))
        samples = np.array(samples)
        X.append(samples)
        Y.append(1)
    print("already construct negative samples")
    return X,Y

def train_pre(X,Y):
    X = np.array(X)
    Y = np.array(Y)
    ss = StandardScaler()

    index = [i for i in range(len(X))]
    np.random.shuffle(index)
    X = X[index]
    Y = Y[index]
    X = ss.fit_transform(X)

    print("starting training....")
    clf0 = XGBClassifier(max_depth=30, learning_rate=0.1,reg_lambda=1)
    clf1 = RandomForestClassifier(n_estimators=100,max_depth=30, random_state=0)
    clf2 = KNeighborsClassifier(n_neighbors=10)
    lr = LogisticRegressionCV(multi_class="ovr",fit_intercept=True,cv=2,penalty="l2",solver="lbfgs",tol=0.1)
    sclf = StackingClassifier(classifiers=[clf0, clf1, clf2],meta_classifier=lr)
    eclf1 = VotingClassifier(estimators=[('lr', lr), ('knn', clf2), ('xgb', clsudo apt-f0),('rf', clf1)], voting='hard')
    eclf2 = VotingClassifier(estimators=[('lr', lr), ('knn', clf2), ('xgb', clf0),('rf', clf1)], voting='soft')
    clf_l = [clf0, clf1, clf2, lr, sclf, eclf1, eclf2]

    for clf in clf_l:

        sl = cross_val_score(clf, X, Y, cv=3)
        score = sl.mean()
        print(score)
    print("finished")
    # pred = clf0.predict(X_test)
    # print("testing finished")
    # accuracy=clf0.score(X_test,y_test)
    # print('accuracy:%.2f%%'%(accuracy*100.0))
    # print(confusion_matrix(y_test, pred))
    # print(classification_report(y_test, pred))

if __name__ == '__main__':
    X, Y = load_feature()
    # X, Y = load_data_hog()
    train_pre(X, Y)


# 0.9263865081011176
# 0.9255458612588724
# 0.9263023332736866
# 0.9168908504546711
#
# 0.9280669545301731
# 0.9307557620147598

