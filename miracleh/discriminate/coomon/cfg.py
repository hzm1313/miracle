from os.path import join

pic_root_path = 'E:\\dev_work\\pic'
base_pic = join(pic_root_path, 'base');
pic_clean_path = join(pic_root_path, 'svm_train_base\clean');
pic_cut_path = join(pic_root_path, 'svm_train_base\cut');
# 如果失效，可以考虑查一查比较旧的域名注册网站
base_data_pic_url = 'http://www.zhumi.cn/userself/RndCode.asp?rndtype=LOGIN_RndCode&t=1530519616609'

model_path = 'E:\\dev_work\\train\\model'
svm_root = 'E:\\dev_work\\train\\svm'
# 输出日志 tensorboard监控的内容
tb_log_path = 'E:\dev_work\\tmp\\mnist_logs'