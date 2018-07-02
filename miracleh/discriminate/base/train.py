from miracleh.lib.svmutil import svm_read_problem, svm_train, svm_save_model
from miracleh.discriminate.coomon import cfg

def train_svm_model():
    """
    训练并生成model文件
    :return:
    """
    y, x = svm_read_problem(cfg.svm_root + '/train_pix_feature_xy.txt')
    model = svm_train(y, x)
    svm_save_model(cfg.model_path, model)