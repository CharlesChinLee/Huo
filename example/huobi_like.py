import numpy as np
import os
import time
from datetime import datetime

def GetNewAllDataTable(main_kind,use_yesterday):
    folder_now = './KlineData1day'+main_kind
    allfiles = os.listdir(folder_now)
    std_file_name = folder_now + '/eos' + main_kind
    if not os.path.exists(std_file_name):
        std_file_name = folder_now + '/xmr' + main_kind
        if not os.path.exists(std_file_name):
            std_file_name = folder_now + '/xlm' + main_kind
            if not os.path.exists(std_file_name):
                std_file_name = folder_now + '/ont' + main_kind
                if not os.path.exists(std_file_name):
                    print('can not find std file to make std time!!!!')
                    return -1
    std_data = np.loadtxt(std_file_name, delimiter=" ")
    std_row_num = len(std_data)
    all_data = np.zeros((std_row_num, len(allfiles) + 2))
    all_data[:, range(2)] = std_data[:, [0, 1]]

    index_col = 0
    for ki in allfiles:
        path_file = os.path.join(folder_now, ki)
        data_now = np.loadtxt(path_file, delimiter=" ")
        if (len(data_now) > 0):  # at least one row
            date_index = 0
            for m in range(len(data_now)):  # for each data_now's date
                tmp_date = data_now[m, 0]
                for di in range(date_index, std_row_num):  # find the date in (all_data)
                    if tmp_date == all_data[di, 0]:
                        all_data[di, [index_col + 2]] = data_now[m, 5]
                        date_index = di
                        break
        index_col += 1
    all_data = all_data[::-1]  # reverse matrix up and down
    if use_yesterday:
        all_data = np.delete(all_data,0,axis=0)

    np.savez(('./AllDataTable1D'+main_kind+'.npz'), all_data=all_data, allfiles=allfiles)
    return 0

def GetIndexFromAllData(all_data,short,long):
    #all_data first 2 cols are  dates ,do not caculate
    index_data = np.zeros((len(all_data),1))
    index_data[0]=100
    for i in range(1,len(index_data)):
        rate_now=0
        num_now=0
        for j in range(2,len(all_data[0])):
            if all_data[i-1,j]:
                num_now += 1
                rate_now += (all_data[i,j]-all_data[i-1,j])/all_data[i-1,j]
        rate_avg=rate_now/num_now
        index_data[i]=index_data[i-1]*(1+rate_avg)
    length_ind = len(index_data)
    short_avg = np.mean(index_data[(length_ind - short):length_ind])
    long_avg = np.mean(index_data[(length_ind - long):length_ind])
    return short_avg,long_avg

def GetOneKindIndex(all_data,old_all_data,new_main_kind,old_main_kind,all_kind,old_all_kind,short,long,logfile):
    if new_main_kind==old_main_kind:
        short_avg_old, long_avg_old = GetIndexFromAllData(old_all_data, short, long)
        short_avg, long_avg = GetIndexFromAllData(all_data, short, long)
        if long_avg>short_avg:
            if long_avg_old>short_avg_old:
                re_str = '品种 '+new_main_kind.upper()+':短周期均线= '+str(round(short_avg,3))+'  长周期均线= '+str(round(long_avg,3))+'    ++\r\n'
                logfile.write(re_str)
            else:
                re_str = '品种 ' + new_main_kind.upper() + ':短周期均线= ' + str(round(short_avg,3)) + '  长周期均线= ' + str(round(long_avg,3)) + '    +\r\n'
                logfile.write(re_str)
        else:
            re_str = '品种 ' + new_main_kind.upper() + ':短周期均线= ' + str(round(short_avg,3)) + '  长周期均线= ' + str(round(long_avg,3)) + ' \r\n'
            logfile.write(re_str)
    else:
        finded_oldcol = 0
        obj_kind = new_main_kind+old_main_kind
        for i in range(len(old_all_kind)):
            if old_all_kind[i] ==obj_kind:
                finded_oldcol = i+2
                break
        if finded_oldcol:
            std_data_old = old_all_data[:,finded_oldcol:(finded_oldcol+1)]
            old_all_data = np.delete(old_all_data, finded_oldcol, axis=1)
        else:
            re_str ='新品种 '+ new_main_kind.upper() +':老数据中没有找到数据，请重新获取数据 \r\n'
            logfile.write(re_str)
            return
        old_all_data[:,2:len(old_all_data[0])]=old_all_data[:,2:len(old_all_data[0])]/std_data_old
        short_avg_old, long_avg_old = GetIndexFromAllData(old_all_data, short, long)

        finded_col = 0
        for i in range(len(all_kind)):
            if all_kind[i] ==obj_kind:
                finded_col = i+2
                break
        if finded_oldcol:
            std_data = all_data[:,finded_col:(finded_col+1)]
            all_data = np.delete(all_data, finded_col, axis=1)
        else:
            re_str ='新品种 '+ new_main_kind.upper() +':没有找到数据，请重新获取数据 \r\n'
            logfile.write(re_str)
            return
        all_data[:,2:len(all_data[0])]=all_data[:,2:len(all_data[0])]/std_data
        short_avg, long_avg = GetIndexFromAllData(all_data, short, long)

        if long_avg>short_avg:
            if long_avg_old>short_avg_old:
                re_str = '新品种 '+new_main_kind.upper()+':短周期均线= '+str(round(short_avg,3))+'  长周期均线= '+str(round(long_avg,3))+'    ++\r\n'
                logfile.write(re_str)
            else:
                re_str = '新品种 ' + new_main_kind.upper() + ':短周期均线= ' + str(round(short_avg,3)) + '  长周期均线= ' + str(round(long_avg,3)) + '    +\r\n'
                logfile.write(re_str)
        else:
            re_str = '新品种 ' + new_main_kind.upper() + ':短周期均线= ' + str(round(short_avg,3)) + '  长周期均线= ' + str(round(long_avg,3)) + ' \r\n'
            logfile.write(re_str)

def Caculate(folder,main_kind):
    #folder = 'D:\linux_folder'
    # S1 change new_file to old_file
    now_file_name = ('./AllDataTable1D'+main_kind+'.npz')
    old_file_name = ('./OLD_AllDataTable1D'+main_kind+'.npz')

    if not os.path.exists(old_file_name):
        if not os.path.exists(now_file_name):
            GetNewAllDataTable(main_kind, 0)
            os.rename(now_file_name, old_file_name)
    if not os.path.exists(now_file_name):
        GetNewAllDataTable(main_kind, 0)


    now_file = os.stat(now_file_name)
    #old_file = os.stat(old_file_name)
    if time.time()- now_file.st_mtime>(23*3600):
        if  os.path.exists(now_file_name):
            if os.path.exists(old_file_name):
                os.remove(old_file_name)
        os.rename(now_file_name,old_file_name)
    # S2 create new new_file
    GetNewAllDataTable(main_kind, 0)
    # S3 calculate
    if main_kind=='usdt':
        logfile = open('./logfile.txt', 'w')
        time_str = datetime.strftime(datetime.utcfromtimestamp(time.time() + 8 * 60 * 60), "%Y/%m/%d %H:%M:%S")
        logfile.write(time_str+'\r\n')
    else:
        logfile = open('./logfile.txt', 'a')

    a = np.load(now_file_name)
    all_data = a['all_data']
    allfiles = a['allfiles']
    b = np.load(old_file_name)
    all_data_old = b['all_data']
    allfiles_old = b['allfiles']

    GetOneKindIndex(all_data, all_data_old, main_kind, main_kind, allfiles, allfiles_old, 4, 10, logfile)
    logfile.write('\r\n')

    if main_kind == 'usdt':
        new_kind_set = ['btc', 'eth', 'xrp', 'eos', 'ltc', 'bch', 'xlm', 'trx', 'bsv', 'ada', 'xmr', 'dash', 'neo',
                        'etc', 'zec', 'ont', 'ht']
        for new_kind in new_kind_set:
            GetOneKindIndex(all_data, all_data, new_kind, 'usdt', allfiles, allfiles, 4, 10, logfile)
        logfile.write('\r\n')

    logfile.close()


from email import encoders
import smtplib
from email.mime.text import MIMEText


def send_result():
    mail_server = "smtp.qq.com"  # 邮箱服务器地址
    username_send = '1099059992@qq.com'  # 邮箱用户名
    password = 'zrjvacvtymhcffda'  # 邮箱密码：需要使用授权码
    username_recv = 'lz_charles@163.com'  # 收件人，多个收件人用逗号隔开

    file_obj = open('./logfile.txt', 'r')  # 需要两个\\,或者用原始字符串，在引号前面加r
    try:
        strings = file_obj.read()
    finally:
        file_obj.close()
    mail = MIMEText(strings)
    mail['Subject'] = '火币更新测试'
    mail['From'] = 'charles_lz'  # 发件人
    mail['To'] = 'li zhen'  # 收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
    smtp = smtplib.SMTP(mail_server, port=465)  # 连接邮箱服务器，smtp的端口号是25
    # smtp=smtplib.SMTP_SSL('smtp.qq.com',port=465) #QQ邮箱的服务器和端口号
    smtp.login(username_send, password)  # 登录邮箱
    smtp.sendmail(username_send, username_recv, mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
    smtp.quit()  # 发送完毕后退出smtp
    print('success')

def run_all():
    Caculate('.', 'usdt')
    Caculate('.', 'eth')
    Caculate('.', 'btc')
    send_result()

