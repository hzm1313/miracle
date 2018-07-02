import requests
from miracleh.discriminate.coomon import cfg


def downloads_pic(**kwargs):
    pic_name = kwargs.get('pic_name', None)

    pic_url = kwargs.get('pic_url', cfg.base_data_pic_url)
    url = pic_url
    res = requests.get(url, stream=True)
    with open(cfg.base_pic + "\\" + pic_name + '.bmp', 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()

if __name__ == '__main__':
    for w in range(1, 50):
        downloads_pic(pic_name=str(w), pic_url=cfg.base_data_pic_url)
