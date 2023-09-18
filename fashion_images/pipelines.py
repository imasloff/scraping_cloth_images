# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
# import cv2
import scrapy
import urllib
import numpy as np
from urllib import parse
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


# hog = cv2.HOGDescriptor()
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

class ClothImagePipeline(ImagesPipeline):

    def process_item(self, item, spider):
        cat_dict = {
            'tops': 'upper_body',
            'bottoms': 'lower_body',
            'dresses': 'dresses',
        }
        adapter = ItemAdapter(item)
        url_parse = dict(parse.parse_qsl(parse.urlsplit(adapter['category']).query))
        adapter['category'] = cat_dict[url_parse['listTitle'].lower()]
        adapter['unisex'] = 'unisex' in adapter['title']
        adapter['title'] = adapter['title'].split()[-1].lower() if adapter['title'] else 'None'
        super().process_item(item, spider)

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        for image_url in adapter["image_urls"]:
            ## trying to detect people on image - doesn't work very well with photoshoped cloth images
            # req = urllib.urlopen(image_url)
            # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            # img = cv2.imdecode(arr, -1)
            # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # humans, _ = hog.detectMultiScale(gray_img)

            # generate image name
            postfix = image_url.split('/')[-1].split('.')[-1]
            image_name = f"{adapter['category']}/{'men' if adapter['unisex'] else 'women'}/cloth/{adapter['id']}_{adapter['title']}_{adapter['image_urls'].index(image_url)}.{postfix}"
            yield scrapy.Request(image_url, meta={'image_name': image_name})

    def file_path(self, request, response=None, info=None, *, item=None):
        return request.meta['image_name']
