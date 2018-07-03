import io
import random

import requests
from PIL import Image

from miracleh.discriminate.base.handle import get_clear_bin_image, get_crop_imgs, get_feature, convert_feature_to_vector
from miracleh.lib.svmutil import svm_load_model, svm_predict
from miracleh.discriminate.coomon import cfg



def crack_captcha():
    """
    破解验证码,完整的演示流程
    :return:
    """

    # 向指定的url请求验证码图片
    rand_captcha_url = cfg.base_data_pic_url
    res = requests.get(rand_captcha_url, stream=True)

    f = io.BytesIO()
    for chunk in res.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
            f.flush()

    img = Image.open(f)  # 从网络上请求验证码图片保存在内存中
    bin_clear_img = get_clear_bin_image(img)  # 处理获得去噪的二值图
    child_img_list = get_crop_imgs(bin_clear_img)  # 切割图片为单个字符，保存在内存中,例如：4位验证码就可以分割成4个child

    # 加载SVM模型进行预测
    svm_model_name = 'svm_model_file'
    model_path = cfg.svm_model
    model = svm_load_model(model_path)

    img_ocr_name = '__'
    for child_img in child_img_list:
        img_feature_list = get_feature(child_img)  # 使用特征算法，将图像进行特征化降维

        yt = [0]  # 测试数据标签
        # xt = [{1: 1, 2: 1}]  # 测试数据输入向量
        xt = convert_feature_to_vector(img_feature_list)  # 将所有的特征转化为标准化的SVM单行的特征向量
        p_label, p_acc, p_val = svm_predict(yt, xt, model)
        img_ocr_name += ('%d' % p_label[0])  # 将识别结果合并起来

    uuid_tag = str(random.randint(1,20000)) # 生成一组随机的uuid的字符串（开发人员自己写，比较好实现）

    img_save_folder = cfg.pic_result_path
    img.save(img_save_folder + '\\' + img_ocr_name + '__' + uuid_tag + '.png')
    # 例如：__0067__77b10a28f73311e68abef0def1a6bbc8.png
    f.close()


def crack10():
    """
    直接从在线网上下载100张图片，然后识别出来
    :return:
    """
    for i in range(10):
        crack_captcha()


if __name__ == '__main__':
    crack10()
    pass
