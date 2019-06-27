"""透析患者集計用プログラム"""
# -*- coding: utf-8 -*-
import csv
import sys

COLUMN_PATIENTLIST_KARUTENUM = 0
COLUMN_PATIENTLIST_NAME = 1

COLUMN_RE_TYPE = 0
COLUMN_RE_NAME = 4
COLUMN_RE_KARUTENUM = 13

COLUMN_HO_TYPE = 0
COLUMN_HO_DAYS = 4
COLUMN_HO_POINTS = 5

COLUMN_KO_TYPE = 0
COLUMN_KO_DAYS = 4
COLUMN_KO_POINTS = 5

class UserInfo:
    """UserInfo class"""
    def __init__(self):
        self.countindex = 0
        self.rowindex = 0
        self.name = ''
        self.karutenum = 0
        self.days = 0
        self.points = 0
        self.hokentype = ''

    def printline(self):
        print('[' + str(self.countindex).rjust(3, ' ') \
        + ':' + str(self.rowindex).rjust(4, ' ') + '] ' \
        + self.name + ', ' \
        + self.karutenum + ', ' \
        + str(self.days) + ', ' \
        + str(self.points))

    def getlist(self):
        output = []
        output.append(self.countindex)
        output.append(self.printhokentype())
        output.append(self.name)
        output.append(self.karutenum)
        output.append(self.days)
        output.append(self.points)
        return output

    def printhokentype(self):
        if self.hokentype == 'HO':
            return '国保'
        elif self.hokentype == 'KO':
            return '公費'

        return '保険種別なし'

def main():
    """mainプログラム"""
    # 処理対象ファイル名を第１コマンドライン引数として取得
    # 第１コマンドライン引数：処理対象ファイル（RECEIPTC.csv）
    # 第２コマンドライン引数：集計対象の患者一覧ファイル（patient.csv）
    args = sys.argv
    if len(args) != 3:
        print('第１引数に「処理対象ファイル名」を指定してください')
        print('第２引数に「集計対象の患者一覧ファイル名を指定してください')
        print('例： >' + __file__ + ' RECEIPTC.csv patient.csv')
        sys.exit(1)
    inputfilename = args[1]
    patientlistfilename = args[2]
    outputfilename = inputfilename + '.output.csv'

    karutenumlist = [] # 処理対象患者一覧（カルテ番号）
    userinfolist = []  # 出力対象患者

    # 患者一覧CSVの読み込み
    with open(patientlistfilename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for rowdata in spamreader:
            karutenum = int(rowdata[COLUMN_PATIENTLIST_KARUTENUM])
            karutenumlist.append(karutenum)
            print(karutenum) # debug print

    # レセプトデータCSVの読み込み
    with open(inputfilename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        usercountindex = 100
        userrowindex = 100
        username = ''
        userkarutenum = 100
        countindex = 1
        flag_get_hoko = False

        for rowindex, rowdata in enumerate(spamreader):
            if rowdata[COLUMN_RE_TYPE] == 'RE':
                if int(rowdata[COLUMN_RE_KARUTENUM]) in karutenumlist:
                    usercountindex = countindex
                    userrowindex = rowindex
                    username = rowdata[COLUMN_RE_NAME]
                    userkarutenum = int(rowdata[COLUMN_RE_KARUTENUM])
                    flag_get_hoko = True
                else:
                    flag_get_hoko = False

            if flag_get_hoko and rowdata[COLUMN_HO_TYPE] == 'HO':
                user = UserInfo()
                user.countindex = usercountindex
                user.rowindex = userrowindex
                user.name = username
                user.karutenum = userkarutenum

                user.days = rowdata[COLUMN_HO_DAYS]
                user.points = rowdata[COLUMN_HO_POINTS]
                user.hokentype = 'HO'
#			    user.printline() # debug print
                userinfolist.append(user)
                countindex += 1

            if flag_get_hoko and rowdata[COLUMN_KO_TYPE] == 'KO':
                user = UserInfo()
                user.countindex = usercountindex
                user.rowindex = userrowindex
                user.name = username
                user.karutenum = userkarutenum

                user.days = rowdata[COLUMN_KO_DAYS]
                user.points = rowdata[COLUMN_KO_POINTS]
                user.hokentype = 'KO'
#			    user.printline() # debug print
                userinfolist.append(user)
                countindex += 1

    # CSVファイルへの書き出し
    with open(outputfilename, 'w') as outputfile:
        writer = csv.writer(outputfile, lineterminator='\n')
        writer.writerow(['No', '保険種別', '患者氏名', 'カルテ番号', '日数', '点数'])
        for userinfo in userinfolist:
            writer.writerow(userinfo.getlist())

    print('Success !')
    print('inputfile  : ' + inputfilename)
    print('outputfile : ' + outputfilename)
