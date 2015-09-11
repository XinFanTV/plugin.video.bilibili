#coding: utf8

# B站根地址
BASE_URL = r'http://www.bilibili.com/'

ANIME_INDEX=r"http://www.bilibili.com/list/b--a--t----d---1.html"

# B站接口地址（用于获取视频地址）
INTERFACE_URL = r'http://interface.bilibili.com/playurl?cid={0}&sign=fd627105c78c7b877fee35f997a63eb0'

# B站评论页面地址
COMMENT_URL = r'http://comment.bilibili.tv/{0}.xml'

# 根菜单
ROOT_PATH = [ 'RSS', 'Index','新开发' ]

# 列表类型
LIST_TYPE = [ 'Month', 'Alpha' ]

# RSS地址列表
RSS_URLS = [
    {
        'name': u'动画',
        'eng_name': 'anime',
        'url': 'rss-1.xml'
    },
    {
        'name': u'音乐',
        'eng_name': 'music',
        'url': 'rss-3.xml'
    },
    {
        'name': u'游戏',
        'eng_name': 'game',
        'url': 'rss-4.xml'
    },
    {
        'name': u'娱乐',
        'eng_name': 'entertainment',
        'url': 'rss-5.xml'
    },
    {
        'name': u'专辑',
        'eng_name': 'album',
        'url': 'rss-11.xml'
    },
    {
        'name': u'新番连载',
        'eng_name': 'series',
        'url': 'rss-13.xml'
    }
]

# 索引地址列表
INDEX_URLS = [
    {
        'name': u'新番二次元',
        'eng_name': 'anime2',
        'url': 'sitemap/sitemap-33.html'
    },
    {
        'name': u'新番三次元',
        'eng_name': 'anime3',
        'url': 'sitemap/sitemap-34.html'
    },
    {
        'name': u'专辑二次元',
        'eng_name': 'album2',
        'url':  'sitemap/sitemap-32.html'
    },
    {
        'name': u'专辑三次元',
        'eng_name': 'album3',
        'url': 'sitemap/sitemap-15.html'
    }
]



CAT_URLS = [
    {
        'name': u'番剧-连载动画',
        'eng_name': 'bangumi-two-1.html',
        'url': 'video/bangumi-two-1.html'
    },
    {
        'name': u'番剧-连载动画-TAG-OVA，OAD',
        'eng_name': 'bangumi-two-1.html#!tag=OVA•OAD&page=1',
        'url': 'video/bangumi-two-1.html#!tag=OVA•OAD&page=1'
    },
    {
        'name': u'番剧-连载动画-TAG-剧场版',
        'eng_name': 'bangumi-two-1.html#!tag=剧场版&page=1',
        'url': 'video/bangumi-two-1.html#!tag=剧场版&page=1'
    },
    {
        'name': u'番剧-完结动画',
        'eng_name': 'part-twoelement-1.html',
        'url': 'video/part-twoelement-1.html'
    },
    {
        'name': u'番剧-完结动画-剧场·OVA',
        'eng_name': 'bangumi-ova-1.html',
        'url': 'video/bangumi-ova-1.html'
    },

    {
        'name': u'电影-电影',
        'eng_name': 'movie-movie-1.html',
        'url': 'video/movie-movie-1.html'
    },
    {
        'name': u'电视剧-完结剧集',
        'eng_name': 'tv-drama-1.html',
        'url': 'video/tv-drama-1.html'
    },
    {
        'name': u'电视剧-完结剧集-国产',
        'eng_name': 'tv-drama-cn-1.html',
        'url': 'video/tv-drama-cn-1.html'
    },
    {
        'name': u'电视剧-完结剧集-日剧',
        'eng_name': 'tv-drama-jp-1.html',
        'url': 'video/tv-drama-jp-1.html'
    },
    {
        'name': u'电视剧-完结剧集-美剧',
        'eng_name': 'tv-drama-us-1.html',
        'url': 'video/tv-drama-us-1.html'
    },
    {
        'name': u'电视剧-完结剧集-其他',
        'eng_name': 'tv-drama-other-1.html',
        'url': 'video/tv-drama-other-1.html'
    },
    {
        'name': u'电视剧-连载剧集',
        'eng_name': 'soap-three-1.html',
        'url': 'video/soap-three-1.html'
    },
    {
        'name': u'电视剧-连载剧集-国产',
        'eng_name': 'soap-three-cn-1.html',
        'url': 'video/soap-three-cn-1.html'
    },
    {
        'name': u'电视剧-连载剧集-日剧',
        'eng_name': 'soap-three-jp-1.html',
        'url': 'video/soap-three-jp-1.html'
    },
    {
        'name': u'电视剧-连载剧集-美剧',
        'eng_name': 'soap-three-us-1.html',
        'url': 'video/soap-three-us-1.html'
    },
    {
        'name': u'电视剧-连载剧集-其他',
        'eng_name': 'soap-three-oth-1.html',
        'url': 'video/soap-three-oth-1.html'
    },


    {
        'name': u'科技-纪录片',
        'eng_name': 'tech-popular-science-1.html',
        'url': 'video/tech-popular-science-1.html'
    },
    {
        'name': u'科技-全球科技',
        'eng_name': 'tech-future-1.html',
        'url': 'video/tech-future-1.html'
    },


    {
        'name': u'娱乐-综艺',
        'eng_name': 'ent-variety-1.html',
        'url': 'video/ent-variety-1.html'
    },

    {
        'name': u'娱乐-美食',
        'eng_name': 'ent-food-1.html',
        'url': 'video/ent-food-1.html'
    },
    {
        'name': u'娱乐-生活娱乐',
        'eng_name': 'ent-life-1.html',
        'url': 'video/ent-life-1.html'
    }, 
    {
        'name': u'音乐-音乐选集',
        'eng_name': 'music-collection-1.html',
        'url': 'video/music-collection-1.html'
    },
    {
        'name': u'音乐-三次元音乐',
        'eng_name': 'music-coordinate-1.html',
        'url': 'video/music-coordinate-1.html'
    },
    {
        'name': u'音乐-音乐视频',
        'eng_name': 'music-video-1.html',
        'url': 'video/music-video-1.html'
    },
    {
        'name': u'舞蹈',
        'eng_name': 'dance-1.html',
        'url': 'video/dance-1.html'
    },
    {
        'name': u'动画-综合',
        'eng_name': 'douga-else-1.html',
        'url': 'video/douga-else-1.html'
    },
    {
        'name': u'电影-微电影·短片',
        'eng_name': 'tv-micromovie-1.html',
        'url': 'video/tv-micromovie-1.html'
    },
    {
        'name': u'电影-预告·花絮',
        'eng_name': 'movie-presentation-1.html',
        'url': 'video/movie-presentation-1.html'
    },
    {
        'name': u'电视剧-特摄·布袋',
        'eng_name': 'tv-sfx-1.html',
        'url': 'video/tv-sfx-1.html'
    },
    {
        'name': u'电视剧-预告·花絮',
        'eng_name': 'tv-presentation-1.html',
        'url': 'video/tv-presentation-1.html'
    },
    {
        'name': u'动画-原创·配音',
        'eng_name': 'douga-voice-1.html',
        'url': 'video/douga-voice-1.html'
    },
    {
        'name': u'动画-MMD·3D',
        'eng_name': 'douga-mmd-1.html',
        'url': 'video/douga-mmd-1.html'
    },
    {
        'name': u'动画-MAD·AMV',
        'eng_name': 'douga-mad-1.html',
        'url': 'video/douga-mad-1.html'
    },
    {
        'name': u'音乐-演奏',
        'eng_name': 'music-perform-1.html',
        'url': 'video/music-perform-1.html'
    },
    {
        'name': u'音乐-VOCALOID·UTAU',
        'eng_name': 'music-vocaloid-1.html',
        'url': 'video/music-vocaloid-1.html'
    },
    {
        'name': u'音乐-翻唱',
        'eng_name': 'music-Cover-1.html',
        'url': 'video/music-Cover-1.html'
    },
    {
        'name': u'科技-野生技术协会',
        'eng_name': 'tech-wild-1.html',
        'url': 'video/tech-wild-1.html'
    },
    {
        'name': u'科技-趣味科普',
        'eng_name': 'tech-fun-1.html',
        'url': 'video/tech-fun-1.html'
    },
    
    {
        'name': u'娱乐-动物圈',
        'eng_name': 'ent-animal-1.html',
        'url': 'video/ent-animal-1.html'
    },
    {
        'name': u'娱乐-Korea相关',
        'eng_name': 'ent-korea-1.html',
        'url': 'video/ent-korea-1.html'
    },
     
    {
        'name': u'游戏-游戏视频',
        'eng_name': 'game-video-1.html',
        'url': 'video/game-video-1.html'
    },
    {
        'name': u'游戏-游戏攻略·解说',
        'eng_name': 'game-ctary-1.html',
        'url': 'video/game-ctary-1.html'
    },
    {
        'name': u'游戏-电子竞技',
        'eng_name': 'game-fight-1.html',
        'url': 'video/game-fight-1.html'
    },
    {
        'name': u'游戏-Mugen',
        'eng_name': 'game-mugen-1.html',
        'url': 'video/game-mugen-1.html'
    },
       
     
    {
        'name': u'鬼畜-二次元鬼畜',
        'eng_name': 'douga-kichiku-1.html',
        'url': 'video/douga-kichiku-1.html'
    },
    {
        'name': u'鬼畜-三次元鬼畜',
        'eng_name': 'ent-Kichiku-1.html',
        'url': 'video/ent-Kichiku-1.html'
    },
    {
        'name': u'鬼畜-人力VOCALOID',
        'eng_name': 'kichiku-manual_vocaloid-1.html',
        'url': 'video/kichiku-manual_vocaloid-1.html'
    },
    {
        'name': u'鬼畜-教程演示',
        'eng_name': 'kichiku-course-1.html',
        'url': 'video/kichiku-course-1.html'
    },
    
]

HOT_CATS= [
    {
        'name': u'连载新番',
        'id': '33',
    },
    {
        'name': u'完结新番',
        'id': '32',
    },
    {
        'name': u'全站',
        'id': '0',
    },
    {
        'name': u'动画',
        'id': '1',
    },
    {
        'name': u'音乐',
        'id': '3',
    },
    {
        'name': u'舞蹈',
        'id': '129',
    },
    {
        'name': u'游戏',
        'id': '4',
    },
    {
        'name': u'科技',
        'id': '36',
    },
    {
        'name': u'娱乐',
        'id': '5',
    },
    {
        'name': u'电影',
        'id': '23',
    },
    {
        'name': u'鬼畜',
        'id': '119',
    },
    {
        'name': u'电视剧',
        'id': '11',
    },
    
]

# 临时文件目录
TEMP_DIR = ''
