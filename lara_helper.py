import os
from pathlib import Path

import urllib3
from bs4 import BeautifulSoup


def download_all_pics(pic_urls, dest_folder):
  dest_folder = Path(dest_folder)
  if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

  req = urllib3.PoolManager()
  count = 0
  for img_path in pic_urls:
    res = req.request('GET', img_path, preload_content=False)
    path = dest_folder / '{}.jpg'.format(count)

    chunk_size = 10
    with open(path, 'wb') as out:
      while True:
        data = res.read(chunk_size)
        if not data:
          break
        out.write(data)

    count += 1
    res.release_conn()


def download_all_pics_radio(url, dest_folder):
  req = urllib3.PoolManager()
  res = req.request('GET', url)

  soup = BeautifulSoup(res.data, 'html.parser')
  res.release_conn()

  links = soup.find_all('a', {'class': 'fancybox'})
  pic_urls = []
  for link in links:
    img_path = link.find('img').get('src')

    if 'ads' not in img_path and img_path.endswith('.jpg'):
      img_path = 'http://bilder.radiogong.com/' + img_path.replace('thumbnails', 'files')
      print(img_path)
      pic_urls.append(img_path)

  download_all_pics(pic_urls, dest_folder)


def download_all_pics_frizz(url, dest_folder):
  req = urllib3.PoolManager()
  res = req.request('GET', url)

  soup = BeautifulSoup(res.data, 'html.parser')
  res.release_conn()

  links = soup.find_all('div', {'class': 'gallery_slide'})
  pic_urls = []
  for link in links:
    img_path = link.find('img').get('src')
    img_path = img_path.replace('&w=600', '')
    print(img_path)
    pic_urls.append(img_path)

  download_all_pics(pic_urls, dest_folder)


if __name__ == '__main__':
  download_all_pics_radio('http://bilder.radiogong.com/gallery.php?galuid=7547', '/Users/nosebrain/Desktop/lara/laby_1')
  download_all_pics_radio('http://bilder.radiogong.com/gallery.php?galuid=7633', '/Users/nosebrain/Desktop/lara/laby_2')
  download_all_pics_frizz('https://frizz-wuerzburg.de/blitzlicht/biofete-laby/', '/Users/nosebrain/Desktop/lara/frizz_1')
