from miracleh.lib.svmutil import svm_read_problem, svm_train, svm_save_model, svm_problem, svm_parameter, svm_predict
from miracleh.discriminate.coomon import cfg


def svm_data_demo():
    """
    这个是来自于网上的demo，和本识图项目无关
    :return:
    """
    y = [1, -1]  # 训练数据的标签
    x = [{1: 1, 2: 1}, {1: -1, 2: -1}]  # 训练数据的输入向量
    # <label> <index1>:<value1> <index2>:<value2>
    # 相当于找到的特征值

    prob = svm_problem(y, x)  # 定义SVM模型的训练数据
    param = svm_parameter('-t 0 -c 4 -b 1')  # 训练SVM模型所需的各种参数
    model = svm_train(prob, param)  # 训练好的SVM模型

    # svm_save_model('model_file', model)#将训练好的模型保存到文件中

    # 使用测试数据集对已经训练好的模型进行测试
    yt = [-1]  # 测试数据标签
    xt = [{1: 1, 2: 1}]  # 测试数据输入向量

    p_label, p_acc, p_val = svm_predict(yt, xt, model)

def train_hzm_test():
    y, x = [1, -1], [{1: 1, 2: 1}, {1: -1, 2: -1}]
    prob = svm_problem(y, x)
    param = svm_parameter('-t 0 -c 4 -b 1')
    model = svm_train(prob, param)
    yt = [1]
    xt = [{1: 1, 2: 1}]
    print('start predict')
    p_label, p_acc, p_val = svm_predict(yt, xt, model)
    print('start predict result')
    print(p_label)

def train_svm_model():
    """
    训练并生成model文件
    :return:
    """
    y, x = svm_read_problem(cfg.svm_feeture_txt)
    model = svm_train(y, x)
    svm_save_model(cfg.svm_model, model)


if __name__ == '__main__':
    train_svm_model()