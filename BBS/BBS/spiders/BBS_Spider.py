#--------------------------------------------#
#           title:BBSSpider                  #
#           date:2017/5/5                    #
#           author:Guten_Tag                 #
#--------------------------------------------#

# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
import sys
from BBS.items import post
from BBS.items import replys
import re
import difflib
from collections import defaultdict

class BBSpider(scrapy.Spider):
    name = "bbs"
    allowed_domains = []
    start_urls = [
        "http://www.hzlen.com/forum.php?mod=viewthread&tid=2107988&extra=page%3D1",
        "http://www.hzlen.com/forum.php?mod=viewthread&tid=2107986&extra=page%3D1",
        "http://www.hzlen.com/forum.php?mod=viewthread&tid=2107724&extra=page%3D1",
        "http://www.hzlen.com/forum.php?mod=viewthread&tid=2107901&extra=page%3D1",
        "http://www.hzlen.com/forum.php?mod=viewthread&tid=2107873&extra=page%3D1",
        "http://www.hzlen.com/forum.php?mod=viewthread&tid=2107860&extra=page%3D1",
        "http://benyouhui.it168.com/thread-5101302-1-1.html",
        "http://benyouhui.it168.com/thread-5659013-1-1.html",
        "http://hongdou.gxnews.com.cn/viewthread-15278172.html",
        "http://hongdou.gxnews.com.cn/viewthread-15278000.html",
        "http://hongdou.gxnews.com.cn/viewthread-15276630.html",
        "http://hongdou.gxnews.com.cn/viewthread-15276515.html",
        "http://hongdou.gxnews.com.cn/viewthread-15275811.html",
        "http://hongdou.gxnews.com.cn/viewthread-15277255.html",
        "http://bbs.auto.ifeng.com/thread-2858830-1-1.html",
        "http://bbs.55bbs.com/thread-10139143-1-1.html",
        "http://bbs.55bbs.com/thread-10139954-1-1.html",
        "http://bbs.55bbs.com/thread-10139091-1-1.html",
        "http://bbs.55bbs.com/thread-10138662-1-1.html",
        "http://bbs.55bbs.com/thread-5568177-1-1.html",
        "http://bbs.55bbs.com/thread-10139272-1-1.html",
        "http://games.hiapk.com/thread-27931984-1-1.html",
        "http://games.hiapk.com/thread-27335229-1-1.html",
        "http://games.hiapk.com/thread-26788619-1-1.html",
        "http://games.hiapk.com/thread-27299148-1-1.html",
        "http://games.hiapk.com/thread-27123690-1-1.html",
        "http://games.hiapk.com/thread-27291206-1-1.html",
        "http://bbs.17k.com/thread-3411535-1-1.html",
        "http://bbs.17k.com/thread-3411835-1-1.html",
        "http://bbs.17k.com/thread-3411629-1-1.html",
        "http://bbs.17k.com/thread-3411631-1-1.html",
        "http://bbs.17k.com/thread-3411542-1-1.html",
        "http://bbs.17k.com/thread-3411824-1-1.html",
        "http://bbs.hexun.com/post_111_11366684_1_d.html",
        "http://bbs.hexun.com/post_111_11363746_1_d.html",
        "http://bbs.hexun.com/post_111_11364459_1_d.html",
        "http://bbs.hexun.com/post_111_11367022_1_d.html",
        "http://bbs.hexun.com/post_91_11368602_1_d.html",
        "http://bbs.hexun.com/post_91_11368961_1_d.html",
        "http://bbs.9game.cn/thread-20233532-1-1.html",
        "http://bbs.9game.cn/thread-23059139-1-1.html",
        "http://bbs.9game.cn/thread-23059523-1-1.html",
        "http://bbs.9game.cn/thread-23045031-1-1.html",
        "http://bbs.9game.cn/thread-23057367-1-1.html",
        "http://bbs.9game.cn/thread-23058559-1-1.html",
        "http://bbs.hiapk.com/thread-25569836-1-1.html",
        "http://bbs.hiapk.com/thread-25511858-1-1.html",
        "http://club.lenovo.com.cn/thread-2009723-1-1.html",
        "http://club.lenovo.com.cn/thread-2009726-1-1.html",
        "http://club.lenovo.com.cn/thread-2009351-1-1.html",
        "http://club.lenovo.com.cn/thread-1986556-1-1.html",
        "http://club.dzwww.com/thread-56102395-1-1.html",
        "http://club.dzwww.com/thread-56099679-1-1.html",
        "http://club.dzwww.com/thread-56101593-1-1.html",
        "http://club.dzwww.com/thread-56098149-1-1.html",
        "http://club.dzwww.com/thread-55335746-1-1.html",
        "http://club.dzwww.com/thread-55688482-1-1.html",
        "http://szbbs.sznews.com/thread-3454941-1-1.html",
        "http://szbbs.sznews.com/thread-3454941-1-1.html",
        "http://szbbs.sznews.com/thread-3454941-1-1.html",
        "http://szbbs.sznews.com/thread-3454941-1-1.html",
        "http://szbbs.sznews.com/thread-3454941-1-1.html",
        "http://szbbs.sznews.com/thread-3454941-1-1.html",
        "http://bbs.haoche51.com/thread-10197-1-1.html",
        "http://club.bandao.cn/thread-7192692-1-1.html",
        "http://bbs.house.163.com/bbs/yzjlb/620002274.html",
        "http://bbs.house.163.com/bbs/yzjlb/620001757.html",
        "http://bbs.house.163.com/bbs/yzjlb/620001732.html",
        "http://bbs.hsw.cn/read-htm-tid-19056842.html",
        "http://bbs.hsw.cn/read-htm-tid-19056850.html",
        "http://bbs.hsw.cn/read-htm-tid-19056828.html",
        "http://bbs.hsw.cn/read-htm-tid-19056853.html",
        "http://bbs.hsw.cn/read-htm-tid-19056822.html",
        "http://bbs.hsw.cn/read-htm-tid-19056843.html",
        "http://bbs.home.163.com/bbs/riji/620002323.html",
        "http://bbs.home.163.com/bbs/riji/619999962.html",
        "http://bbs.home.163.com/bbs/riji/619999956.html",
        "http://bbs.home.163.com/bbs/riji/619999930.html",
        "http://bbs.home.163.com/bbs/riji/619999921.html",
        "http://bbs.home.163.com/bbs/riji/619999583.html",
        "http://bbs.houdao.com/r13642116/",
        "http://bbs.houdao.com/r13642112/",
        "http://bbs.houdao.com/r13641987/",
        "http://bbs.houdao.com/r13641921/",
        "http://bbs.houdao.com/r13638688/",
        "http://bbs.houdao.com/r13641841/",
        "http://bbs.huway.com/thread/5001838/1/1.html",
        "http://bbs.huanqiu.com/thread-4020302-1-1.html",
        "http://bbs.huanqiu.com/thread-4029235-1-1.html",
        "http://bbs.huanqiu.com/thread-4029221-1-1.html",
        "http://bbs.huanqiu.com/thread-4022169-1-1.html",
        "http://bbs.huanqiu.com/thread-4029230-1-1.html",
        "http://bbs.huanqiu.com/thread-4029142-1-1.html",
        "http://bbs.hupu.com/18434177.html",
        "http://bbs.hupu.com/18418434.html",
        "http://bbs.hupu.com/18429225.html",
        "http://bbs.hupu.com/18437261.html",
        "http://bbs.hupu.com/18418165.html",
        "http://bbs.hupu.com/18419560.html",
        "http://sxy.hc360.com/article-215521.html",
        "http://sxy.hc360.com/article-215496.html",
        "http://sxy.hc360.com/article-215515.html",
        "http://sxy.hc360.com/article-215304.html",
        "http://sxy.hc360.com/article-215524.html",
        "http://sxy.hc360.com/article-215196.html",
        "https://maijia.bbs.taobao.com/detail.html?postId=7611318",
        "https://maijia.bbs.taobao.com/detail.html?postId=7610262",
        "https://maijia.bbs.taobao.com/detail.html?postId=7609494",
        "https://maijia.bbs.taobao.com/detail.html?postId=7565098",
        "https://maijia.bbs.taobao.com/detail.html?postId=7610488",
        "https://maijia.bbs.taobao.com/detail.html?postId=7610781",
        "http://www.mahua.com/xiaohua/1671603.htm",
        "http://www.mahua.com/xiaohua/1671673.htm",
        "http://www.mahua.com/xiaohua/1671676.htm",
        "http://www.mahua.com/xiaohua/1671503.htm",
        "http://www.mahua.com/xiaohua/1671557.htm",
        "http://www.mahua.com/xiaohua/1669125.htm",
        "http://www.lookgz.com/thread-1175540-1-1.html",
        "http://www.lookgz.com/thread-1175539-1-1.html",
        "http://www.lookgz.com/thread-1175518-1-1.html",
        "http://www.lookgz.com/thread-1175517-1-1.html",
        "http://www.lookgz.com/thread-1174826-1-1.html",
        "http://www.lookgz.com/thread-1174814-1-1.html",
        "http://www.mala.cn/thread-14518360-1-1.html",
        "http://www.mala.cn/thread-14520241-1-1.html",
        "http://www.mala.cn/thread-14517994-1-1.html",
        "http://www.mala.cn/thread-14510805-1-1.html",
        "http://www.mala.cn/thread-14506646-1-1.html",
        "http://www.mala.cn/thread-14520234-1-1.html",
        "http://bbs.17173.com/thread-10065609-1-1.html",
        "http://bbs.17173.com/thread-10040207-1-1.html",
        "http://bbs.17173.com/thread-10063070-1-1.html",
        "http://bbs.17173.com/thread-9975745-1-1.html",
        "http://bbs.17173.com/thread-10065429-1-1.html",
        "http://bbs.17173.com/thread-10064069-1-1.html",
        "http://www.hainei.org/thread-7587784-1-1.html",
        "http://www.hainei.org/thread-7589947-1-1.html",
        "http://www.hainei.org/thread-7588063-1-1.html",
        "http://www.hainei.org/thread-7591324-1-1.html",
        "http://www.hainei.org/thread-7591840-1-1.html",
        "http://www.hainei.org/thread-7575484-1-1.html",
        "http://www.hepan.com/thread-3563131-1-1.html",
        "http://bbs.360.cn/thread-14930209-1-1.html",
        "http://bbs.360.cn/thread-14933486-1-1.html",
        "http://bbs.360.cn/thread-14932493-1-1.html",
        "http://bbs.360.cn/thread-14931081-1-1.html",
        "http://bbs.360.cn/thread-14924032-1-1.html",
        "http://bbs.360.cn/thread-14826265-1-1.html",
        "http://forum.xitek.com/thread-1672181-1-1-1.html",
        "http://forum.xitek.com/thread-1670402-1-1-1.html",
        "http://forum.xitek.com/thread-1672237-1-1-1.html",
        "http://forum.xitek.com/thread-1408996-1-1-1.html",
        "http://forum.xitek.com/thread-1638059-1-1-1.html",
        "http://forum.xitek.com/thread-1559551-1-1-1.html",
        "http://bbs.elecfans.com/jishu_1122857_1_1.html",
        "http://bbs.elecfans.com/jishu_329455_1_1.html",
        "http://bbs.elecfans.com/jishu_1123318_1_1.html",
        "http://bbs.elecfans.com/jishu_396911_1_1.html",
        "http://bbs.elecfans.com/jishu_1123078_1_1.html",
        "http://bbs.elecfans.com/jishu_597184_1_1.html",
        "http://guba.eastmoney.com/news,300593,629651662.html",
        "http://guba.eastmoney.com/news,cjpl,629621444.html",
        "http://guba.eastmoney.com/news,300593,629330950.html",
        "http://guba.eastmoney.com/news,300593,629036019.html",
        "http://guba.eastmoney.com/news,300593,629443470.html",
        "http://guba.eastmoney.com/news,300593,629504800.html",
        "http://bbs.mb.qq.com/thread-1585324-1-1.html",
        "http://bbs.e23.cn/thread-180481286-1-1.html",
        "http://bbs.e23.cn/thread-180496560-1-1.html",
        "http://bbs.e23.cn/thread-180481293-1-1.html",
        "http://bbs.e23.cn/thread-180480455-1-1.html",
        "http://bbs.e23.cn/thread-180478141-1-1.html",
        "http://bbs.e23.cn/thread-180496870-1-1.html",
        "http://www.17lu.cn/read-htm-tid-2387082.html",
        "http://www.17lu.cn/read-htm-tid-2387072.html",
        "http://www.17lu.cn/read-htm-tid-2387037.html",
        "http://www.17lu.cn/read-htm-tid-2387036.html",
        "http://www.17lu.cn/read-htm-tid-2387030.html",
        "http://www.17lu.cn/read-htm-tid-2387025.html",
        "http://bbs.lygbst.cn/forum.php?mod=viewthread&tid=4931150&extra=page%3D1%26filter%3Dsortid%26sortid%3D34",
        "http://bbs.duowan.com/thread-40010835-1-1.html",
        "http://bbs.duowan.com/thread-45582508-1-1.html",
        "http://bbs.duowan.com/thread-42872560-1-1.html",
        "http://bbs.duowan.com/thread-45583299-1-1.html",
        "http://bbs.duowan.com/thread-45584663-1-1.html",
        "http://bbs.duowan.com/thread-45583497-1-1.html",
        "http://www.19lou.com/forum-47-thread-42691490762466795-1-1.html",
        "http://www.19lou.com/forum-47-thread-10401492411385426-1-1.html",
        "http://www.19lou.com/forum-47-thread-8681492127117279-1-1.html",
        "http://www.19lou.com/forum-47-thread-42281492248691317-1-1.html",
        "http://www.19lou.com/forum-47-thread-8291492411794479-1-1.html",
        "http://www.19lou.com/forum-47-thread-8281492411763453-1-1.html",
        "http://bbs.coolpad.com/thread-5825400-1-1.html",
        "http://www.3sogou.com/read.php?tid=1211649",
        "http://www.3sogou.com/read.php?tid=1211438&page=e",
        "http://www.3sogou.com/read.php?tid=1211221&page=e",
        "http://www.3sogou.com/read.php?tid=1211194",
        "http://www.3sogou.com/read.php?tid=1211635&page=e",
        "http://www.3sogou.com/read.php?tid=1211363",
        "http://www.55188.com/thread-7938848-1-1.html",
        "http://www.55188.com/thread-7948111-1-1.html",
        "http://www.55188.com/thread-7238001-1-1.html",
        "http://www.55188.com/thread-7947024-1-1.html",
        "http://www.55188.com/thread-7947207-1-1.html",
        "http://www.55188.com/thread-7947182-1-1.html",
        "http://nanhai.hinews.cn/thread-7194938-1-1.html",
        "http://nanhai.hinews.cn/thread-7196582-1-1.html",
        "http://nanhai.hinews.cn/thread-7197886-1-1.html",
        "http://nanhai.hinews.cn/thread-7196653-1-1.html",
        "http://nanhai.hinews.cn/thread-7198192-1-1.html",
        "http://nanhai.hinews.cn/thread-7198493-1-1.html",
        "http://shzy.myubbs.com/thread-136851-1-1.html",
        "http://shzy.myubbs.com/thread-136852-1-1.html",
        "http://bbs.mumayi.com/thread-6158857-1-1.html",
        "http://bbs.mumayi.com/thread-6266884-1-1.html",
        "http://bbs.mumayi.com/thread-6266883-1-1.html",
        "http://bbs.mumayi.com/thread-5462281-1-1.html",
        "http://bbs.mumayi.com/thread-6266916-1-1.html",
        "http://bbs.mumayi.com/thread-6266915-1-1.html",
        "http://s.dianping.com/topic/17565364",
        "http://s.dianping.com/topic/17709876",
        "http://s.dianping.com/topic/17703115",
        "http://s.dianping.com/topic/17698775",
        "http://s.dianping.com/topic/17720913",
        "http://s.dianping.com/topic/17646892",
        "http://bbs.mydigit.cn/read.php?tid=2065103&page=e",
        "http://bbs.mydigit.cn/read.php?tid=2065115",
        "http://bbs.mydigit.cn/read.php?tid=2065115&page=e",
        "http://bbs.mydigit.cn/read.php?tid=2065103",
        "http://bbs.mydigit.cn/read.php?tid=2064888&page=e",
        "http://bbs.mydigit.cn/read.php?tid=2065102&page=e",
        "http://bbs.cjn.cn/read.php?tid-22587334.html",
        "http://bbs.cjn.cn/read.php?tid-22587358.html",
        "http://bbs.cjn.cn/read.php?tid-22587334.html",
        "http://bbs.cjn.cn/read.php?tid-22587362.html",
        "http://bbs.cjn.cn/read.php?tid-22587334.html",
        "http://bbs.cjn.cn/read.php?tid-22587370.html",
        "http://bbs.cnmo.com/thread-1525137-1-1.html",
        "http://bbs.cnmo.com/thread-1515377-1-1.html",
        "http://bbs.cnmo.com/thread-15700730-1-1.html",
        "http://bbs.cnmo.com/thread-15700729-1-1.html",
        "http://bbs.cnmo.com/thread-15700728-1-1.html",
        "http://bbs.cnmo.com/thread-15700724-1-1.html",
        "http://bbs.cnnb.com.cn/forum.php?mod=viewthread&tid=7303963&extra=page%3D1",
        "http://bbs.cnnb.com.cn/forum.php?mod=viewthread&tid=7303961&extra=page%3D1",
        "http://bbs.cnnb.com.cn/forum.php?mod=viewthread&tid=7303870&extra=page%3D1",
        "http://bbs.cnnb.com.cn/forum.php?mod=viewthread&tid=7303869&extra=page%3D1",
        "http://bbs.cnnb.com.cn/forum.php?mod=viewthread&tid=7303562&extra=page%3D1",
        "http://bbs.cnnb.com.cn/forum.php?mod=viewthread&tid=7303561&extra=page%3D1",
        "http://bbs.cnool.net/cthread-106641316.html",
        "http://bbs.cheshi.com/thread-5109698-1-1.html",
        "http://bbs.cheshi.com/thread-5109695-1-1.html",
        "http://bbs.cheshi.com/thread-5109701-1-1.html",
        "http://bbs.cheshi.com/thread-5109299-1-1.html",
        "http://bbs.cheshi.com/thread-5109657-1-1.html",
        "http://bbs.cheshi.com/thread-5109570-1-1.html",
        "http://bbs.jj.xmfish.com/read-htm-tid-2461347.html",
        "http://bbs.jj.xmfish.com/read-htm-tid-2461306.html",
        "http://bbs.jj.xmfish.com/read-htm-tid-2461296.html",
        "http://bbs.jj.xmfish.com/read-htm-tid-2461289.html",
        "http://bbs.jj.xmfish.com/read-htm-tid-2461262.html",
        "http://bbs.jj.xmfish.com/read-htm-tid-2461252.html",
        "http://x.heshuicun.com/thread-65511-1-1.html",
        "http://x.heshuicun.com/thread-65517-1-1.html",
        "http://x.heshuicun.com/thread-12023-1-1.html",
        "http://x.heshuicun.com/thread-12418-1-1.html",
        "http://x.heshuicun.com/thread-3196-1-1.html",
        "http://bbs.jrj.com.cn/msg,100501797.html",
        "http://bbs.bitscn.com/thread-411722-1-1.html",
        "http://bbs.lvye.cn/thread-2575601-1-1.html",
        "http://bbs.liulanqi.baidu.com/thread-180831-1-1.html",
        "http://forum.home.news.cn/detail/140440458/1.html",
        "http://forum.home.news.cn/detail/140803461/1.html",
        "http://forum.home.news.cn/detail/140792420/1.html",
        "http://forum.home.news.cn/detail/140802305/1.html",
        "http://forum.home.news.cn/detail/140796005/1.html",
        "http://forum.home.news.cn/detail/140797384/1.html",
        "http://bbs.fx110.com/thread/50931/0/0/1",
        "http://bbs.fx110.com/thread/50927/0/0/1",
        "http://bbs.fx110.com/thread/50918/0/0/1",
        "http://bbs.fx110.com/thread/50922/0/0/1",
        "http://bbs.fx110.com/thread/50929/0/0/1",
        "http://bbs.fx110.com/thread/50920/0/0/1",
        "http://www.szbbs.cn/thread-2935724-1-1.html",
        "http://www.szbbs.cn/thread-2935691-1-1.html",
        "http://www.szbbs.cn/thread-2935577-1-1.html",
        "http://www.szbbs.cn/thread-2935450-1-1.html",
        "http://www.szbbs.cn/thread-2935590-1-1.html",
        "http://www.szbbs.cn/thread-2935286-1-1.html",
        "http://bbs.suyoo.cn/thread-1000568-1-1.html",
        "http://bbs.suyoo.cn/thread-1000565-1-1.html",
        "http://bbs.suyoo.cn/thread-988324-1-1.html",
        "http://bbs.suyoo.cn/thread-1000514-1-1.html",
        "http://bbs.suyoo.cn/thread-1000478-1-1.html",
        "http://bbs.suyoo.cn/thread-1000432-1-1.html",
        "http://www.cntieba.com/thread-265496-1-1.html",
        "http://www.cntieba.com/thread-264910-1-1.html",
        "http://www.cntieba.com/thread-266768-1-1.html",
        "http://www.cntieba.com/thread-265496-1-1.html",
        "http://www.cntieba.com/thread-264910-1-1.html",
        "http://www.cntieba.com/thread-266768-1-1.html",
        "http://bbs.scol.com.cn/thread-15171012-1-1.html",
        "http://bbs.scol.com.cn/thread-15170958-1-1.html",
        "http://bbs.scol.com.cn/thread-15170836-1-1.html",
        "http://bbs.scol.com.cn/thread-15170864-1-1.html",
        "http://bbs.scol.com.cn/thread-15170915-1-1.html",
        "http://bbs.scol.com.cn/thread-15171021-1-1.html",
        "http://usst.myubbs.com/thread-136900-1-1.html",
        "http://bbs.smartisan.com/forum.php?mod=viewthread&tid=534013&extra=page%3D1",
        "http://bbs.smartisan.com/forum.php?mod=viewthread&tid=534010&extra=page%3D1",
        "http://bbs.smartisan.com/forum.php?mod=viewthread&tid=534008&extra=page%3D1",
        "http://bbs.smartisan.com/forum.php?mod=viewthread&tid=534007&extra=page%3D1",
        "http://bbs.smartisan.com/forum.php?mod=viewthread&tid=534009&extra=page%3D1",
        "http://bbs.smartisan.com/forum.php?mod=viewthread&tid=533888&extra=page%3D1",
        "http://itbbs.pconline.com.cn/tv/53448715.html",
        "http://itbbs.pconline.com.cn/dc/53398376.html",
        "http://itbbs.pconline.com.cn/es/53448391.html",
        "http://itbbs.pconline.com.cn/mobile/53450914.html",
        "http://itbbs.pconline.com.cn/dc/53449907.html",
        "http://itbbs.pconline.com.cn/dc/53451327.html",
        "http://bbs.sh021.cc/thread-281584-1-1.html",
        "http://bbs.sh021.cc/thread-281596-1-1.html",
        "http://bbs.sh021.cc/thread-281425-1-1.html",
        "http://bbs.sh021.cc/thread-281562-1-1.html",
        "http://bbs.sh021.cc/thread-281473-1-1.html",
        "http://bbs.sh021.cc/thread-281236-1-1.html",
        "http://bbs.sgamer.com/thread-13334561-1-1.html",
        "http://bbs.sgamer.com/thread-13334546-1-1.html",
        "http://bbs.sgamer.com/thread-13334291-1-1.html",
        "http://bbs.sgamer.com/thread-13334032-1-1.html",
        "http://bbs.sgamer.com/thread-13334390-1-1.html",
        "http://bbs.sgamer.com/thread-13333778-1-1.html",
        "http://www.oneplusbbs.com/thread-3318992-1-1.html",
        "http://www.oneplusbbs.com/thread-3296582-1-1.html",
        "http://www.oneplusbbs.com/thread-3325892-1-1.html",
        "http://www.oneplusbbs.com/thread-3298436-1-1.html",
        "http://www.oneplusbbs.com/thread-3322142-1-1.html",
        "http://www.oneplusbbs.com/thread-3346636-1-1.html",
        "http://guba.sina.com.cn/?s=thread&tid=289966&bid=25",
        "http://guba.sina.com.cn/?s=thread&tid=289954&bid=25",
        "http://guba.sina.com.cn/?s=thread&tid=228163&bid=33",
        "http://guba.sina.com.cn/?s=thread&tid=228154&bid=33",
        "http://guba.sina.com.cn/?s=thread&tid=366895&bid=16",
        "http://guba.sina.com.cn/?s=thread&tid=382824&bid=18",
        "http://bbs.dospy.com/thread-17795786-1-141-1.html",
        "http://bbs.dospy.com/thread-17792416-1-141-1.html",
        "http://bbs.dospy.com/thread-17795845-1-141-1.html",
        "http://bbs.dospy.com/thread-17794618-1-141-1.html",
        "http://bbs.dospy.com/thread-17794965-1-141-1.html",
        "http://bbs.dospy.com/thread-17794551-1-141-1.html",
        "http://bbs.gxsky.com/thread-13971751-1-1.html",
        "http://bbs.gxsky.com/thread-13971751-1-1.html",
        "http://bbs.gxsky.com/thread-13971734-1-1.html",
        "http://bbs.gxsky.com/thread-13971734-1-1.html",
        "http://bbs.gxsky.com/thread-13971705-1-1.html",
        "http://bbs.gxsky.com/thread-13971705-1-1.html",
        "http://www.xcar.com.cn/bbs/viewthread.php?tid=29598308",
        "http://www.xcar.com.cn/bbs/viewthread.php?tid=29598756",
        "http://www.xcar.com.cn/bbs/viewthread.php?tid=29602158",
        "http://www.xcar.com.cn/bbs/viewthread.php?tid=29595394",
        "http://www.xcar.com.cn/bbs/viewthread.php?tid=29602262",
        "http://www.xcar.com.cn/bbs/viewthread.php?tid=29582643",
        "http://club.autohome.com.cn/bbs/threadqa-c-2123-62307772-1.html",
        "http://club.autohome.com.cn/bbs/thread-c-2123-62307611-1.html",
        "http://club.autohome.com.cn/bbs/thread-c-2123-62307293-1.html",
        "http://club.autohome.com.cn/bbs/thread-c-2123-62307217-1.html",
        "http://club.autohome.com.cn/bbs/thread-c-873-62291061-1.html",
        "http://club.autohome.com.cn/bbs/threadqa-c-2123-62307178-1.html",
        "http://bbs.25pp.com/thread-514664-1-1.html",
        "http://bbs.25pp.com/thread-235995-1-1.html",
        "http://bbs.25pp.com/thread-514647-1-1.html",
        "http://bbs.25pp.com/thread-514656-1-1.html",
        "http://bbs.25pp.com/thread-469917-1-1.html",
        "http://bbs.25pp.com/thread-504648-1-1.html",
        "http://www.gbbye.com/read.php?tid=1068916",
        "http://www.gbbye.com/read.php?tid=1068914",
        "http://www.gbbye.com/read.php?tid=1068888",
        "http://www.gbbye.com/read.php?tid=1068912",
        "http://www.gbbye.com/read.php?tid=1068887",
        "http://www.gbbye.com/read.php?tid=1068911",
        "http://www.c2000.cn/dispbbs.asp?boardID=40&ID=3136650",
        "http://www.c2000.cn/dispbbs.asp?boardID=40&ID=3138036",
        "http://www.c2000.cn/dispbbs.asp?boardID=40&ID=3138347",
        "http://www.c2000.cn/dispbbs.asp?boardID=40&ID=3138345",
        "http://www.c2000.cn/dispbbs.asp?boardID=40&ID=3137951",
        "http://www.c2000.cn/dispbbs.asp?boardID=40&ID=3135038",
        "http://bbs.qianlong.com/thread-9998498-1-1.html",
        "http://bbs.qianlong.com/thread-9998614-1-1.html",
        "http://bbs.qianlong.com/thread-10001078-1-1.html",
        "http://bbs.qianlong.com/thread-10000963-1-1.html",
        "http://bbs.qianlong.com/thread-10000967-1-1.html",
        "http://bbs.qianlong.com/thread-10001435-1-1.html",
        "http://36.01ny.cn/thread-4733395-1-1.html",
        "http://36.01ny.cn/thread-4733382-1-1.html",
        "http://36.01ny.cn/thread-4733419-1-1.html",
        "http://36.01ny.cn/thread-4732188-1-1.html",
        "http://36.01ny.cn/thread-4732882-1-1.html",
        "http://36.01ny.cn/thread-4733132-1-1.html",
        "http://my.fx678.com/thread-1560691-1-1.html",
        "http://my.fx678.com/thread-1559824-1-1.html",
        "http://my.fx678.com/thread-1560611-1-1.html",
        "http://my.fx678.com/thread-1559589-1-1.html",
        "http://my.fx678.com/thread-1559499-1-1.html",
        "http://my.fx678.com/thread-1560692-1-1.html",
        "http://bbs.gfan.com/android-9027135-1-1.html",
        "http://bbs.gfan.com/android-8311516-1-1.html",
        "http://bbs.gfan.com/android-8300671-1-1.html",
        "http://bbs.gfan.com/android-8206112-1-1.html",
        "http://bbs.gfan.com/android-8237600-1-1.html",
        "http://bbs.gfan.com/android-9031539-1-1.html",
        "http://bbs.oeeee.com/thread-17907342-1-1.html",
        "http://bbs.oeeee.com/thread-17907353-1-1.html",
        "http://bbs.oeeee.com/thread-17907316-1-1.html",
        "http://bbs.oeeee.com/thread-17907321-1-1.html",
        "http://bbs.guanjia.qq.com/forum.php?mod=viewthread&tid=5281598&extra=page%3D1",
        "http://bbs.guanjia.qq.com/forum.php?mod=viewthread&tid=5281589&extra=page%3D1",
        "http://bbs.guanjia.qq.com/forum.php?mod=viewthread&tid=5281525&extra=page%3D1",
        "http://bbs.guanjia.qq.com/forum.php?mod=viewthread&tid=5281462&extra=page%3D1",
        "http://bbs.guanjia.qq.com/forum.php?mod=viewthread&tid=5277978&extra=page%3D1",
        "http://bbs.guanjia.qq.com/forum.php?mod=viewthread&tid=5281544&extra=page%3D1",
        "http://bbs.njtu.net/forum.php?mod=viewthread&tid=50010&extra=page%3D1",
        "http://bbs.njtu.net/forum.php?mod=viewthread&tid=50002&extra=page%3D1",
        "http://bbs.njtu.net/forum.php?mod=viewthread&tid=49953&extra=page%3D1",
        "http://bbs.njtu.net/forum.php?mod=viewthread&tid=49992&extra=page%3D1",
        "http://bbs.njtu.net/forum.php?mod=viewthread&tid=49991&extra=page%3D1",
        "http://bbs.njtu.net/forum.php?mod=viewthread&tid=49985&extra=page%3D1",
        "http://www.oppo.cn/thread-77564123-1",
        "http://www.oppo.cn/thread-77312723-1",
        "http://www.oppo.cn/thread-77543469-1",
        "http://www.oppo.cn/thread-77099549-1",
        "http://www.oppo.cn/thread-77466478-1",
        "http://www.oppo.cn/thread-76650735-1",
        "http://bbs.haibao.com/thread-3693721-1-1.html",
        "http://bbs.onlylady.com/thread-4021913-1-1.html",
        "http://quan.ithome.com/0/129/294.htm",
        "http://quan.ithome.com/0/126/857.htm",
        "http://quan.ithome.com/0/129/499.htm",
        "http://quan.ithome.com/0/129/218.htm",
        "http://quan.ithome.com/0/128/861.htm",
        "http://quan.ithome.com/0/130/593.htm",
        "http://bbs1.people.com.cn/post/7/1/1/162171173.html",
        "http://bbs1.people.com.cn/post/7/1/2/162122748.html",
        "http://bbs1.people.com.cn/post/7/1/2/162147104.html",
        "http://bbs1.people.com.cn/post/7/1/2/162167913.html",
        "http://bbs1.people.com.cn/post/7/1/2/162157718.html",
        "http://bbs1.people.com.cn/post/7/1/1/162149472.html",
        "http://www.pengfu.com/content_1669635_1.html",
        "http://www.pengfu.com/content_1669640_1.html",
        "http://www.pengfu.com/content_1669634_1.html",
        "http://www.pengfu.com/content_1666422_1.html",
        "http://www.pengfu.com/content_1669637_1.html",
        "http://www.pengfu.com/content_1666423_1.html",
        "http://www.myzte.cn/thread-338135-1-1.html",
        "http://www.myzte.cn/thread-338084-1-1.html",
        "http://www.myzte.cn/thread-338115-1-1.html",
        "http://www.myzte.cn/thread-338105-1-1.html",
        "http://www.myzte.cn/thread-338129-1-1.html",
        "http://www.myzte.cn/thread-338126-1-1.html",
        "http://www.ecuer.com/read.php?tid=871898",
        "http://www.ecuer.com/read.php?tid=871892",
        "http://www.ecuer.com/read.php?tid=871901",
        "http://www.hhphh.com/read.php?tid=1103350",
        "http://www.hhphh.com/read.php?tid=1103094",
        "http://www.hhphh.com/read.php?tid=1103358",
        "http://www.hhphh.com/read.php?tid=1103200",
        "http://www.hhphh.com/read.php?tid=1103199",
        "http://www.hhphh.com/read.php?tid=1102974",
        "http://bbs.zol.com.cn/quanzi/d41_27148.html",
        "http://bbs.zol.com.cn/padbbs/d173_10032.html",
        "http://bbs.zol.com.cn/padbbs/d128_1073.html",
        "http://bbs.zhiyoo.com/thread-13295202-1-1.html",
        "http://bbs.zhiyoo.com/thread-12519097-1-1.html",
        "http://bbs.zhiyoo.com/thread-13278108-1-1.html",
        "http://bbs.zhiyoo.com/thread-12800471-1-1.html",
        "http://bbs.zhiyoo.com/thread-13293078-1-1.html",
        "http://bbs.zhiyoo.com/thread-13288203-1-1.html",
        "http://bbs.yzz.cn/thread-5917672-1-1.html",
        "http://bbs.yzz.cn/thread-5917657-1-1.html",
        "http://bbs.yzz.cn/thread-5917537-1-1.html",
        "http://bbs.yzz.cn/thread-5917132-1-1.html",
        "http://bbs.yzz.cn/thread-5913592-1-1.html",
        "http://bbs.ydss.cn/thread-836235-1-1.html",
        "http://bbs.ydss.cn/thread-836478-1-1.html",
        "http://bbs.ydss.cn/thread-836505-1-1.html",
        "http://bbs.ydss.cn/thread-836523-1-1.html",
        "http://bbs.ydss.cn/thread-837962-1-1.html",
        "http://bbs.ydss.cn/thread-836509-1-1.html",
        "http://bbs.xmfish.com/read-htm-tid-14240696.html",
        "http://bbs.xmfish.com/read-htm-tid-14241260.html",
        "http://bbs.xmfish.com/read-htm-tid-14200047.html",
        "http://bbs.xmfish.com/read-htm-tid-14241590.html",
        "http://bbs.xmfish.com/read-htm-tid-14232379.html",
        "http://bbs.xmfish.com/read-htm-tid-14240986.html",
        "http://bbs.xiaomi.cn/t-13450581",
        "http://bbs.xiaomi.cn/t-13455812",
        "http://www.shdxlt.cn/ShowPost.asp?ThreadID=163469",
        "http://www.shdxlt.cn/ShowPost.asp?ThreadID=163468",
        "http://www.shdxlt.cn/ShowPost.asp?ThreadID=163467",
        "http://www.shdxlt.cn/ShowPost.asp?ThreadID=163466",
        "http://www.shdxlt.cn/ShowPost.asp?ThreadID=163499",
        "https://www.cqsq.com/read/7075872",
        "https://www.cqsq.com/read/7075718",
        "https://www.cqsq.com/read/7075616",
        "https://www.cqsq.com/read/7074867",
        "https://www.cqsq.com/read/7075022",
        "https://www.cqsq.com/read/7075746",
        "http://baa.bitauto.com/track/thread-10978878.html",
        "http://baa.bitauto.com/sh/thread-10959075.html",
        "http://baa.bitauto.com/teana/thread-9776229.html",
        "http://baa.bitauto.com/teana/thread-10978742.html",
        "http://baa.bitauto.com/teana/thread-9774520.html",
        "http://baa.bitauto.com/teana/thread-9759591.html",
        "http://club.qingdaonews.com/showAnnounce_26_4232435_1_0.htm",
        "http://club.qingdaonews.com/showAnnounce_2_5848776_1_0.htm",
        "http://club.qingdaonews.com/showAnnounce_2_5849006_1_0.htm",
        "http://club.qingdaonews.com/showAnnounce_2_5848977_1_0.htm",
        "http://club.qingdaonews.com/showAnnounce_2_5845429_1_0.htm",
        "http://club.qingdaonews.com/showAnnounce_2_5848774_1_0.htm",
        "http://www.dddzs.com/read.php?tid=1578725",
        "http://www.dddzs.com/read.php?tid=1578725&page=e",
        "http://www.dddzs.com/read.php?tid=1578728",
        "http://www.dddzs.com/read.php?tid=1578745&page=e",
        "http://www.dddzs.com/read.php?tid=1578728&page=e",
        "http://www.dddzs.com/read.php?tid=1578745",
        "http://club.sports.sohu.com/soccer/thread/4uusmxws3oj/p1",
        "http://club.sports.sohu.com/soccer/thread/4upokpe15t5/p1",
        "http://club.sports.sohu.com/soccer/thread/4uvjcxl22r7/p1",
        "http://club.sports.sohu.com/soccer/thread/4uvm05ub3xp/p1",
        "http://club.sports.sohu.com/soccer/thread/4uv5t11s0jg/p1",
        "http://club.sports.sohu.com/soccer/thread/4uvlr7lmyq3/p1",
        "http://www.djtz.net/thread-3260445-1-1.html",
        "http://www.djtz.net/thread-3260900-1-1.html",
        "http://www.djtz.net/thread-3260332-1-1.html",
        "http://www.djtz.net/thread-3260947-1-1.html",
        "http://www.djtz.net/thread-3260951-1-1.html",
        "http://www.djtz.net/thread-3260953-1-1.html",
        "http://bbs.vogue.com.cn/thread-784047-1-1.html",
        "http://bbs.vogue.com.cn/thread-784045-1-1.html",
        "http://bbs.vc52.cn/thread-868289-1-1.html",
        "http://bbs.vc52.cn/thread-868290-1-1.html",
        "http://bbs.vc52.cn/thread-868295-1-1.html",
        "http://bbs.vc52.cn/thread-868293-1-1.html",
        "http://bbs.vc52.cn/thread-868279-1-1.html",
        "http://bbs.vc52.cn/thread-868222-1-1.html",
        "http://cn.club.vmall.com/thread-12529602-1-1.html",
        "http://cn.club.vmall.com/thread-12580673-1-1.html",
        "http://cn.club.vmall.com/thread-11876506-1-1.html",
        "http://cn.club.vmall.com/thread-12580939-1-1.html",
        "http://cn.club.vmall.com/thread-12582636-1-1.html",
        "http://cn.club.vmall.com/thread-12575069-1-1.html",
        "http://bbs.voc.com.cn/topic-7759335-1-1.html",
        "http://bbs.voc.com.cn/topic-7759255-1-1.html",
        "http://bbs.voc.com.cn/topic-7759315-1-1.html",
        "http://bbs.voc.com.cn/topic-7741496-1-1.html",
        "http://bbs.voc.com.cn/topic-7679320-1-1.html",
        "http://bbs.voc.com.cn/topic-7695858-1-1.html",
        "http://bbs.tianya.cn/post-23-815442-1.shtml",
        "http://bbs.tianya.cn/post-23-815438-1.shtml",
        "http://bbs.tianya.cn/post-23-815437-1.shtml",
        "http://bbs.tianya.cn/post-23-815436-1.shtml",
        "http://bbs.tianya.cn/post-enterprise-1472196-1.shtml",
        "http://bbs.tianya.cn/post-23-815435-1.shtml"
    ]

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")

    def parse(self, response):
        
        def get_text(root):
            string = root.text
            if string == None or len(string) <= 2:
                string = ""

            children = root.getchildren()
            if len(children) == 0:
                return string

            for child in children:
                string = string + get_text(child)

            return string

        def parse_traverse(root):#遍历所有结点
            #print (root.tag, root.attrib)

            children = root.getchildren()
            if len(children) == 0:
                return
            for child in children:
                parse_traverse(child)

            return

        def parse_preprocess(root):
            children = root.getchildren()
            if len(children) == 0:
                return
            for child in children:
                if child.tag == "script" or child.tag == "img" or child.tag == "style":
                    root.remove(child)
                else:
                    parse_preprocess(child)

            return
        
        def parse_find_title_text(root):
            title = root.iter("h1")
            for t in title:
                title_text = get_text(t)
            p=re.compile('\s+')
            title_text=re.sub(p,'',title_text)

            return title_text

        def parse_find_title(root):
            title = root.iter("h1")
            for t in title:
                title=t
                break
            return title

        def filterTag(html):
            re_comment = re.compile('<!--.*[^>]*?-->')
            re_img = re.compile('<img.*?>')
            re_script = re.compile('<script[^>]*?>[\s\S]*?<\/script>')
            re_style = re.compile('<style[^>]*?>[\s\S]*?<\/style>')
            re_h = re.compile('<h[2-9][^>]*?>[\s\S]*?<\/h[2-9]>')
            html = re_script.sub('', html)
            html = re_style.sub('', html)
            html = re_img.sub('', html)
            html = re_comment.sub('', html)
            html = re_h.sub('', html)

            return html

        def parse_find_post_function(root):
            flag=0
            if root!=None:
                children = root.getchildren()
                if len(children)>4:
                    for child in children:
                            if child.getnext()!=None:
                                if child.attrib.get('class')!=None or child.attrib.get('id')!=None:
                                    str1=str(child.attrib.get('class',''))+str(child.attrib.get('id',''))
                                    str2=str(child.getnext().get('class',''))+str(child.getnext().get('id',''))
                                    seq = difflib.SequenceMatcher(None, str1, str2)  
                                    ratio = seq.ratio()
                                    if ratio>=0.7:
                                        flag=1
                                        break
                                    else:
                                        flag=0
            return flag

        def parse_find_post(root):
            if root!=None:
                parent=root.getparent()
                flag=parse_find_post_function(parent)
                if flag==1:
                    return parent
                else:
                    if parent!=None:
                        children=parent.getchildren()
                        if len(children) == 0:
                            parse_find_post(parent)
                        for child in children:
                            flag=parse_find_post_function(child)
                            if flag==1:
                                break
                            else:
                                continue
                        if flag==1:
                            return child
                        else:
                            return parse_find_post(parent)

        def get_author_date_content(root):
            string = ""
            if 'class' in root.attrib:
                if "author" in root.attrib['class'] or "authi" in root.attrib['class']:
                    string = get_text(root)
                    re_date = re.compile('.*?((?:19|20)\d\d)-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])')
                    date = re_date.match(string)
                    if date:
                        start = date.start()
                        end = date.end()
                        string = string[start:end+1]
                        format = '0123456789-'
                        for c in string:
                            if c not in format:
                                string = string.replace(c, '')
                        if string == "":
                            string = " "
                        string = "%" + string + "%"
                    else:
                        if string == "":
                            string = " "
                        string = "#" + string + "#"
                elif 'class' in root.attrib:
                    if "t_f" in root.attrib['class']:
                        string = get_text(root)
                        if string == "":
                            string = " "
                        string = "$" + string + "$"
                        return string
            elif 'id' in root.attrib:
                if "author" in root.attrib['id'] or "authi" in root.attrib['id']:
                    string = get_text(root)
                    re_date = re.compile('.*?((?:19|20)\d\d)-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])')
                    date = re_date.match(string)
                    if date:
                        start = date.start()
                        end = date.end()
                        string = string[start:end+1]
                        format = '0123456789-'
                        for c in string:
                            if c not in format:
                                string = string.replace(c, '')
                        if string == "":
                            string = " "
                        string = "%" + string + "%"
                    else:
                        if string == "":
                            string = " "
                        string = "#" + string + "#"
                else:
                    string = ""
            else:
                string = ""

            if string == None:
                string = ""

            children = root.getchildren()
            if len(children) == 0:
                return string

            for child in children:
                string = string + get_author_date_content(child)

            return string

        def deal_author_date_content(author_date_content):
            return author_date_content.replace('##', '')

        html = filterTag(response.text)

        root = etree.HTML(html)
        children = root.getchildren()
        for child in children:
            if child.tag == "body":
                root = child
        parse_preprocess(root)#预处理,去除噪音标签

        item = post()
        item1 = replys()
        t = parse_find_title(root)
        post_pos = parse_find_post(t)
        author_date_content = get_author_date_content(post_pos)
        author_date_content = deal_author_date_content(author_date_content)
        
        item['url'] = "\n" + response.url
        item['title'] = parse_find_title_text(root)
        item1['title'] = item['title']
        item['author'] = " "
        item['publish_date'] = " "
        flag1 = flag2 = flag3 = count = 0
        flag4 = 1
        content  = author = date = ""
        for c in author_date_content:
            if c == " " or c == '\n' or c == '\r':
                continue
            if c == '$' and flag1 == 0:
                flag1 = 1
                continue
            if c == '$' and flag1 == 1:
                flag1 = 0
                if flag4:
                    item['content'] = content
                    flag4 = 0
                    yield item
                else:
                    item1['content'] = content
                    count = count + 1
                content = " "
                continue
            if flag1 == 1:
                content = content + c

            if c == '#' and flag2 == 0:
                flag2 = 1
                continue
            if c == '#' and flag2 == 1:
                flag2 = 0
                item1['author'] = author
                count = count + 1
                author = " "
                continue
            if flag2 == 1:
                author = author + c

            if c == '%' and flag3 == 0:
                flag3 = 1
                continue
            if c == '%' and flag3 == 1:
                flag3 = 0
                item1['publish_date'] = date
                count = count + 1
                date = " "
                continue
            if flag3 == 1:
                date = date + c

            if count == 3:
                count = 0
                yield item1


