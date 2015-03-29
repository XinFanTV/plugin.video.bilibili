#coding: utf8
import tempfile
from xbmcswift2 import Plugin, xbmcgui, xbmc
from resources.lib.bilibili import Bili
from resources.lib.config import TEMP_DIR
from resources.lib.subtitle import subtitle_offset

plugin = Plugin()
bili = Bili()

def get_tmp_dir():
    if len(TEMP_DIR) != 0:
        return TEMP_DIR
    try:
        return tempfile.gettempdir()
    except:
        return TEMP_DIR

def _print_info(info):
    print '[BiliAddon]: ' + info
 

# 首页
@plugin.route('/')
def index():
    dir_list = [
        {
            'label': name['name'],
            'path': plugin.url_for('list_type', category=name['eng_name'])
        } for name in bili.CAT_URLS ]


    #dir_list.append({
    #    'label': '热门排行',
    #    'path': plugin.url_for('hot_index', type='all')
    #})
    #
    #
    dir_list.append({
        'label': '热门排行(日)',
        'path': plugin.url_for('hot_index', type='day')
    })
    dir_list.append({
        'label': '热门排行(3日)',
        'path': plugin.url_for('hot_index', type='3day')
    })
    dir_list.append({
        'label': '热门排行(周)',
        'path': plugin.url_for('hot_index', type='week')
    })
    dir_list.append({
        'label': '热门排行(月)',
        'path': plugin.url_for('hot_index', type='month')
    })
    return dir_list




# HOT列表页
@plugin.route('/hot/<type>')
def hot_index(type):
    if type == "all":
        dir_list = [
            {
                'label': name['name'],
                'path': plugin.url_for('hot_list', type=type, category=name['eng_name'])
            } for name in bili.CAT_URLS ]

    else: 
        dir_list = [
            {
                'label': name['name'],
                'path': plugin.url_for('hot_list', type=type, category=name['id'])
            } for name in bili.HOT_CATS ]

    return dir_list

# HOT列表页
@plugin.route('/hot/<type>/<category>')
def hot_list(type,category):
    if type == "all":
        dir_list=[]
        for item in bili.get_hot_items(category):
            dir_list.append({
                'label': item['title'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('list_videos', category=category, video=item['published'])
            }) 
    else:

        dir_list=[]
        for item in bili.get_hotjson_items(type,category):
            dir_list.append({
                'label': item['title'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('list_videos', category=category, video=item['published'])
            }) 


    return dir_list

# 分类列表页
@plugin.route('/items/<category>')
def list_type(category):
    dir_list=[]
    for item in bili.get_cat_items(category):
        if category == item['category']:
            dir_list.append({
                'label': item['title'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('list_videos', category=category, video=item['published'])
            }) 
        else:
            dir_list.append({
                'label': item['title'],
                'path': plugin.url_for('list_type', category=item['link'])
            }) 

    return dir_list


# 分类列表页
@plugin.route('/items/<category>/<video>')
def list_videos(category,video):
    videos=bili.get_video_paths(category,video)
    if len(videos)>0:
        dir_list = [ {
            'label': item['title'],
            'thumbnail':item['thumbnail'],
            'path': plugin.url_for('list_parts', category=category, video=item['published'],part=item['title'])
        } for item in videos ]

    else:

        dir_list = [ {
            'label': item['title'],
            'path': item['link'],
            'thumbnail':item['thumbnail'],
            'is_playable':True,
        } for item in bili.get_video_parts(category,video,'直接播放') ]

 




    return dir_list




# 视频页
@plugin.route('/items/<category>/<video>/<part>')
def list_parts(category,video,part):
 
    dir_list = [ {
        'label': item['title'],
        'path': item['link'],
        'thumbnail':item['thumbnail'],
        'is_playable':True,
    } for item in bili.get_video_parts(category,video,part) ]
    return dir_list


if __name__ == '__main__':
    plugin.run()
