def svm_model_test():
    """
    使用测试集测试模型
    :return:
    """
    yt, xt = svm_read_problem(svm_root + '/last_test_pix_xy_new.txt')
    model = svm_load_model(model_path)
    p_label, p_acc, p_val = svm_predict(yt, xt, model)#p_label即为识别的结果

    cnt = 0
    for item in p_label:
        print('%d' % item, end=',')
        cnt += 1
        if cnt % 8 == 0:
            print('')