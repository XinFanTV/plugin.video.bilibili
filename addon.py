#coding: utf8
import tempfile
import json,cookielib,gzip,time,urllib2,os,os.path
from xbmcswift2 import Plugin, xbmcgui, xbmc
from resources.lib.bilibili import Bili
from resources.lib.config import TEMP_DIR
from resources.lib.subtitle import subtitle_offset

plugin = Plugin()
bili = Bili()

skin_used = xbmc.getSkinDir()
if skin_used == 'skin.confluence':
    xbmc.executebuiltin('Container.SetViewMode(500)') # "Thumbnail" view


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

    dir_list = []
    dir_list.append({
        'label': '新番索引',
        'path': plugin.url_for('anime_index', type='1')
    })
    dir_list.append({
        'label': 'TAGS',
        'path': plugin.url_for('anime_tags_index')
    })

    for name in bili.CAT_URLS:
        dir_list.append({
            'label': name['name'],
            'path': plugin.url_for('list_type', category=name['eng_name'])
        })

   
    #dir_list.append({
    #    'label': '热门排行',
    #    'path': plugin.url_for('hot_index', type='all')
    #})
    #
    #
    dir_list.append({
        'label': '热门排行(日)',
        'path': plugin.url_for('hot_index', type='1')
    })
    dir_list.append({
        'label': '热门排行(3日)',
        'path': plugin.url_for('hot_index', type='3')
    })
    dir_list.append({
        'label': '热门排行(周)',
        'path': plugin.url_for('hot_index', type='7')
    })
    dir_list.append({
        'label': '热门排行(月)',
        'path': plugin.url_for('hot_index', type='30')
    })
    return dir_list

#  JSON 接口调用首页 
@plugin.route('/anime/tags/index')
def anime_tags_index():
    dir_list=[]
    for item in bili.ROOT_CATEGORY_IDS:
        dir_list.append({
            'label': item,
            'thumbnail':bili.ROOT_CATEGORY_IDS[item]['thumbnail'],
            'path': plugin.url_for('anime_tags_rootcategory', cat_id=item)
        }) 
    return dir_list

@plugin.route('/anime/tags/rootcategory/<cat_id>')
def anime_tags_rootcategory(cat_id):
    print '[BiliAddon]: ' + cat_id
    print bili.ROOT_CATEGORY_IDS[cat_id]
    dir_list=[]
    for item in bili.ROOT_CATEGORY_IDS[cat_id]['children']:
        dir_list.append({
            'label': item,
            'thumbnail':item,
            'path': plugin.url_for('anime_tags_category', cat_id=bili.ROOT_CATEGORY_IDS[cat_id]['children'][item])
        }) 
    return dir_list

@plugin.route('/anime/tags/category/<cat_id>')
def anime_tags_category(cat_id):
    dir_list=[]
    for item in bili.get_tag_category(cat_id):
        dir_list.append({
            'label': item['label'],
            'thumbnail':item['thumbnail'],
            'path': plugin.url_for('anime_tags_view', tagname=item['path'], cat_id=cat_id,page=1)
        }) 
    return dir_list

@plugin.route('/anime/tags/view/category/<cat_id>/tag/<tagname>/page/<page>')
def anime_tags_view(tagname,cat_id,page):
    dir_list=[] 
    for item in bili.get_tag_videos(cat_id,tagname,page):
        if item['type']=="video":
            dir_list.append({
                'label': item['label'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('list_videos', category=cat_id, video=item['path'])
            }) 
        if item['type']=="pager":
            dir_list.append({
                'label': item['label'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('anime_tags_view', tagname=tagname, cat_id=cat_id,page=item['path'])
            }) 


    return dir_list


# HOT列表页
@plugin.route('/anime/index/')
def anime_index():
    dir_list=[]
    for item in bili.get_anime_index():
        if item['type']=="list":
            dir_list.append({
                'label': item['title'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('anime_list', list=item['published'])
            }) 
  

        if item['type']=="sp":
            dir_list.append({
                'label': item['title'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('show_anime', anime=item['published'])
            }) 
  
    return dir_list


# List页
@plugin.route('/anime/list/<list>')
def anime_list(list):
    dir_list=[]
    for item in bili.get_anime_list(list):
        if item['type']=="list":
            dir_list.append({
                'label': item['title'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('anime_list', list=item['published'])
            }) 
  

        if item['type']=="sp":
            dir_list.append({
                'label': item['title'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('show_anime', anime=item['published'])
            }) 
  
    return dir_list

# Anime页
@plugin.route('/anime/anime/<anime>')
def show_anime(anime):
    dir_list=[]
    for item in bili.get_anime_series(anime):
        if item['type']=="bangumi":
            dir_list.append({
                'label': item['title'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('list_videos', category=anime, video=item['link'])
            }) 
  
        if item['type']=="series":
            dir_list.append({
                'label': item['title'],
                'thumbnail':item['thumbnail'],
                'path': plugin.url_for('anime_series', anime=item['link'])
            }) 


    return dir_list

# Anime页
@plugin.route('/anime/series/<anime>')
def anime_series(anime):
    dir_list=[]
    for item in bili.get_anime_series_links(anime):
        dir_list.append({
            'label': item['title'],
            'thumbnail':item['thumbnail'],
            'path': plugin.url_for('list_videos', category=anime, video=item['link'])
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
    if len(videos)>1:
        dir_list = [ {
            'label': item['title'],
            'thumbnail':item['thumbnail'],
            'path': plugin.url_for('list_parts', category=category, video=item['published'],part=item['part'])
        } for item in videos ]

    else:

        playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        playlist.clear()
        for item in bili.get_video_parts(category,video,'直接播放'):
            playlist.add(item['link'])
        xbmc.Player().play(playlist)


    return dir_list




# 视频页
@plugin.route('/items/<category>/<video>/<part>')
def list_parts(category,video,part):
 
    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()

    
    for item in bili.get_video_parts2(category,video,part):
        playlist.add(item['link'])



    xbmc.Player().play(playlist)



if __name__ == '__main__':
    plugin.run()
