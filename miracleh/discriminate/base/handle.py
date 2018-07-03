import os
from PIL import Image
from os.path import join
from miracleh.discriminate.coomon import cfg


def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table


def remove_noise_pixel(img, noise_point_list):
    """
    根据噪点的位置信息，消除二值图片的黑点噪声
    :type img:Image
    :param img:
    :param noise_point_list:
    :return:
    """
    for item in noise_point_list:
        img.putpixel((item[0], item[1]), 1)

def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # todo 判断图片的长宽度下限
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum

def get_crop_imgs(img):
    """
    按照图片的特点,进行切割,这个要根据具体的验证码来进行工作. # 见原理图
    :param img:
    :return:
    """
    child_img_list = []
    for i in range(4):
        x = 2 + i * (6 + 4)  # 见原理图
        y = 0
        child_img = img.crop((x, y, x + 6, y + 10))
        child_img_list.append(child_img)

    return child_img_list

def get_feature(img):
    """
    获取指定图片的特征值,
    1. 按照每排的像素点,高度为10,则有10个维度,然后为6列,总共16个维度
    :param img_path:
    :return:一个维度为10（高度）的列表
    """

    width, height = img.size

    pixel_cnt_list = []
    height = 10
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list


def get_clear_bin_image(image):
    """
    获取干净的二值化的图片。
    图像的预处理：
    1. 先转化为灰度
    2. 再二值化
    3. 然后清除噪点
    参考:http://python.jobbole.com/84625/
    :type img:Image
    :return:
    """
    imgry = image.convert('L')  # 转化为灰度图

    table = get_bin_table()
    out = imgry.point(table, '1')  # 变成二值图片:0表示黑色,1表示白色

    noise_point_list = []  # 通过算法找出噪声点,第一步比较严格,可能会有些误删除的噪点
    for x in range(out.width):
        for y in range(out.height):
            res_9 = sum_9_region(out, x, y)
            if (0 < res_9 < 3) and out.getpixel((x, y)) == 0:  # 找到孤立点
                pos = (x, y)  #
                noise_point_list.append(pos)
    remove_noise_pixel(out, noise_point_list)
    return out

def print_line_x(img, x):
    """
    打印一个Image图像的第x行，方便调试
    :param img:
    :type img:Image
    :param x:
    :return:
    """
    print("line:%s" % x)
    for w in range(img.width):
        print(img.getpixel((w, x)), end='')
    print('')

def print_bin(img):
    """
    输出二值后的图片到控制台，方便调试的函数
    :param img:
    :type img: Image
    :return:
    """
    print('current binary output,width:%s-height:%s\n')
    for h in range(img.height):
        for w in range(img.width):
            print(img.getpixel((w, h)), end='')
        print('')


def save_crop_imgs(bin_clear_image_path, child_img_list, new_pic_path):
    """
    输入：整个干净的二化图片
    输出：每张切成4版后的图片集
    保存切割的图片

    例如： A.png ---> A-1.png,A-2.png,... A-4.png 并保存，这个保存后需要去做label标记的
    :param bin_clear_image_path: xxxx/xxxxx/xxxxx.png 主要是用来提取切割的子图保存的文件名称
    :param child_img_list:
    :return:
    """
    full_file_name = os.path.basename(bin_clear_image_path)  # 文件名称
    full_file_name_split = full_file_name.split('.')
    file_name = full_file_name_split[0]
    # file_ext = full_file_name_split[1]

    i = 0
    for child_img in child_img_list:
        cut_img_file_name = file_name + '-' + ("%s.png" % i)
        child_img.save(join(new_pic_path, cut_img_file_name))
        i += 1

def batch_cut_images(pic_url, new_pic_path):
    """
    训练素材准备。
    批量操作：分割切除所有 "二值 -> 除噪声" 之后的图片，变成所有的单字符的图片。然后保存到相应的目录，方便打标签
    """

    file_list = os.listdir(pic_url)
    for file_name in file_list:
        bin_clear_img_path = os.path.join(pic_url, file_name)
        img = Image.open(bin_clear_img_path)

        child_img_list = get_crop_imgs(img)
        save_crop_imgs(bin_clear_img_path, child_img_list, new_pic_path)  # 将切割的图进行保存，后面打标签时要用

def handle_path_all_image(pic_image_path, pic_new_path):
    # 获取所有图片,进行第一步处理
    file_list = os.listdir(pic_image_path)
    for file_name in file_list:
        file_full_path = os.path.join(cfg.base_pic, file_name)
        image = Image.open(file_full_path)
        #处理的图片返回
        out_image = get_clear_bin_image(image)
        out_image.save(join(cfg.pic_clean_path,file_name))
    # 获取所有图片，进行第二步处理
    batch_cut_images(cfg.pic_clean_path, pic_new_path)
    return pic_new_path

##下面的代码都会获取特征值
def get_feature(img):
    """
    获取指定图片的特征值,
    1. 按照每排的像素点,高度为10,则有10个维度,然后为6列,总共16个维度
    :param img_path:
    :return:一个维度为10（高度）的列表
    """

    width, height = img.size

    pixel_cnt_list = []
    height = 10
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

def convert_imgs_to_feature_file(dig, svm_feature_file, img_folder):
    """
    将某个目录下二进制图片文件，转换成特征文件
    :param dig:检查的数字
    :param svm_feature_file: svm的特征文件完整路径
    :type dig:int
    :return:
    """
    file_list = os.listdir(img_folder)

    # sample_cnt = 0
    # right_cnt = 0
    for file in file_list:
        img = Image.open(img_folder + '/' + file)
        dif_list = get_feature(img)
        # sample_cnt += 1
        line = convert_values_to_str(dig, dif_list)
        svm_feature_file.write(line)
        svm_feature_file.write('\n')



def convert_values_to_str(dig, dif_list):
    """
    将特征值串转化为标准的svm输入向量:

    9 1:4 2:2 3:2 4:2 5:3 6:4 7:1 8:1 9:1 10:3 11:5 12:3 13:3 14:3 15:3 16:6

    最前面的是 标记值，后续是特征值
    :param dif_list:
    :type dif_list: list[int]
    :return:
    """
    index = 1
    line = '%d' % dig

    for item in dif_list:
        fmt = ' %d:%d' % (index, item)
        line += fmt
        index += 1

    # print(line)
    return line

def convert_feature_to_vector(feature_list):
    """

    :param feature_list:
    :return:
    """
    index = 1
    xt_vector = []
    feature_dict = {}
    for item in feature_list:
        feature_dict[index] = item
        index += 1
    xt_vector.append(feature_dict)
    return xt_vector




if __name__ == "__main__":
    # 获取切割图
    # handle_path_all_image(pic_image_path=cfg.base_pic, pic_new_path=cfg.pic_cut_path)
    # 获取svm的数据，注意我的代码结构
    img_folder = cfg.pic_cut_path
    file_list = os.listdir(img_folder)
    test_file = open(cfg.svm_feeture_txt, 'w')
    for fileNum in file_list:
        convert_imgs_to_feature_file(int(fileNum), test_file, img_folder + "\\" +fileNum)  # todo 先用0代替
    test_file.close()
    pass