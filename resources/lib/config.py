#coding: utf8

# B站根地址
BASE_URL = r'http://www.bilibili.com/'

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
        'name': u'连载动画',
        'eng_name': 'bangumi-two-1.html',
        'url': 'video/bangumi-two-1.html'
    },
    {
        'name': u'完结动画',
        'eng_name': 'part-twoelement-1.html',
        'url': 'video/part-twoelement-1.html'
    },
    {
        'name': u'电影',
        'eng_name': 'movie-movie-1.html',
        'url': 'video/movie-movie-1.html'
    },
    {
        'name': u'完结电视剧',
        'eng_name': 'tv-drama-1.html',
        'url': 'video/tv-drama-1.html'
    },
    {
        'name': u'电视剧',
        'eng_name': 'soap-three-1.html',
        'url': 'video/soap-three-1.html'
    },
    {
        'name': u'三次元音乐',
        'eng_name': 'music-coordinate-1.html',
        'url': 'video/music-coordinate-1.html'
    },
    {
        'name': u'纪录片',
        'eng_name': 'tech-popular-science-1.html',
        'url': 'video/tech-popular-science-1.html'
    },
    {
        'name': u'美食',
        'eng_name': 'ent-food-1.html',
        'url': 'video/ent-food-1.html'
    },
    {
        'name': u'音乐合集',
        'eng_name': 'music-collection-1.html',
        'url': 'video/music-collection-1.html'
    },
    {
        'name': u'综艺',
        'eng_name': 'ent-variety-1.html',
        'url': 'video/ent-variety-1.html'
    },
    {
        'name': u'音乐视频',
        'eng_name': 'music-video-1.html',
        'url': 'video/music-video-1.html'
    },
    {
        'name': u'翻唱',
        'eng_name': 'music-Cover-1.html',
        'url': 'video/music-Cover-1.html'
    },
    {
        'name': u'舞蹈',
        'eng_name': 'dance-1.html',
        'url': 'video/dance-1.html'
    }
    
     
    
]




# 临时文件目录
TEMP_DIR = ''
