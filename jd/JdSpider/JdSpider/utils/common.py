# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/8/5 13:55
import hashlib
import time
import jieba
import re

# 计算方法用时的装饰器（单位：秒）
def count_time(func):
    def fun_time(*args):
        t1 = time.time()
        func(*args)
        t2 = time.time()
        print("运行时间为", t2 - t1, "秒")

    return fun_time
# 生成MD5
def genearteMD5(str):
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()

# ALL_BRAND = {'花花公子', '雪中飞', '雅鹿', '南极人', '海澜之家', '鸭鸭', '雪中飞', '吉普', '波司登', '七匹狼', '恒源祥', '罗蒙', '皮尔卡丹', '富贵鸟', '卡宾', '啄木鸟', '利郎', '柒牌', '卡帝乐鳄鱼', '与狼共舞', '坦博尔', '富贵鸟', '稻草人', 'A21', '美特斯邦威', 'HAZZYS', '杉杉', '班尼路', '北极绒', '骆驼', '劲霸男装', '红豆', '斐乐', '俞兆林', '金利来', '蒙口羽皇', '木林森', '网易严选', '皮尔卡丹', '九牧王', '京东京造', '鳄鱼', '千仞岗', '雅戈尔', '袋鼠', '威可多', '才子', '京日达', '袋鼠', '巴鲁特', 'J-VAN', 'Boy London', '真维斯', '吉普', 'MUJI', '太子龙', 'BEASTER', '艾莱依', '报喜鸟', '佐丹奴', '速写', '宾迅', 'BABIBOY', '鳄鱼恤', '杰奥', '高梵', '金盾', '比音勒芬', '富鋌', '诺帝卡', 'Cebrodz', '罗威凯狮', '金盾', '格斯岚帝', 'beanpole', '威秀', '纳维凯尔', 'Tommy Hilfiger', '玛斯梵尼', '尊首', 'MARKLESS', '斯巴奴', '千纸鹤', '爱登堡', 'CAT', '郎曼伦', 'GANT', '雪伦', '红蜻蜓', '有衣有靠', '鄂尔多斯', '培蒙', '世纪男孩', 'ANDSEEYOU', '拉博夫', '金林德伯格', 'MAFEISHIFIGURE', '查利德斯', '简龙', '大绒鹅', '吉普盾', 'AEMAPE', '稻草人', '泰勒绅士', '保罗运动', '雷迪波尔', '红都', 'G2000', 'OMGB', 'gxg.jeans', '雷威凯森', '冰洁', 'FYP', 'Glemall', '纪诗哲', '斯凯奇', 'Plory', '罗蒙', '3号堡罗', '森马', '堡梵希', 'U.S. POLO ASSN.', 'KIKC', '鼎铜', '暇步士', '斯得雅', '查尔斯桃心', '归心', 'Calvin Klein', '起蛰', '罗则', '英克斯', '黑鲸', '海一家', '裳伊居', '步云', 'AKSERIES', 'hteec', '唐纳森', '法莎尼亚', '梦特娇', '沙驰', '热风', '格男仕', 'VBTER', '李维斯', '阿诺顿', '年濛口', '梵·戴克', '迈斯特保罗', '莱克斯顿', '玛古芭', '冰尊', '犀牛呼叫', 'chiay', '保利戈斯', '康坦汀', '优斯顿保罗', 'OVZH', '虎都', '康博', 'ME&CITY', 'Lee Cooper', '臻本色', 'Katiewens', '豪宾莱', '费里克', '西原美', '侯七爷', 'SEEMAX', '康威堡', '雪莱琼斯', 'ZOGANKIN', '格诺菲驰', '浪莎', '南极人+', '南瑾秀', '雾色', '遥渠', '库罗戈', '杭瑞', '已末天成', '翼·原·服·饰', '凌登', 'BOYXCO', '法贝莎', '媚哥', '布鲁森', '胖胖到家', '丹顿赫本', '宾加迪', '石末', '凡客诚品', '奢号', '古赫伦', '良布', '凯登狮', '海布欧', 'YOOOURTHING', '思加伦', '荣上荣', '例柏', '梵木德', '烟斗琼斯', '卡搭', '柏格伦', '柏斐荻', '歌珀莱', '骆克船长', '绅丁', '悍隆', 'AEMPPE', 'ZLLMGM'}
# jieba.load_userdict('my_jieba.txt')







class Common:
    # JS unicode编码转为Python unicode中文
    @staticmethod
    def jsUnicode2Python(text):
        text=text.replace("%", "\\")
        return text.encode("utf-8").decode("unicode_escape")

    # xpath爬取（包含换行符）
    @staticmethod
    def spider_data_by_xpath(response, path):
        list_title = response.xpath(path).xpath('.//text()').extract()
        if (len(list_title) > 0):
            for index in range(len(list_title)):
                list_title[index] = list_title[index].strip()
            data = ",".join(list_title)
            return data
        else:
            return ""
    def regex_converter(param, string):
        res = re.findall(param, string) 
        if not res:
            return '-'
        return res


    # lxml xpath爬取（包含换行符）
    @staticmethod
    def lxml_data_by_xpath(response, path):
        list = response.xpath(path)
        if (len(list) > 0):
            for index in range(len(list)):
                list[index] = list[index].strip()
            data = ",".join(list)
            return data
        else:
            return ""


    
    @staticmethod
    def get_brand_name(shop_name, good_title):

        good_ = jieba.lcut(good_title)
        shop_ = jieba.lcut(shop_name)

        res1 = set(good_) & ALL_BRAND
        res2 = set(shop_) & ALL_BRAND
        res3 = res1 | res2
        if not res3:
            res = shop_name 
        else:
            res = list(res3)[0]
        return res
