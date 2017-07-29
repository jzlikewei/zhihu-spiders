import os
import re
import requests
def download(folder,url):
    if not os.path.exists(folder):
        os.makedirs(folder)
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        name = url.split('/')[-1]
        f = open("./"+folder+'/'+name,'wb')
        f.write(req.content)
        f.close()
        return True
    else:
        return False

def init(url):
    ua = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    s = requests.Session()
    s.headers.update(ua)
    ret=s.get(url)
    s.headers.update({"authorization":"oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})
    return s

def fetch_answer(s,qid,limit,offset):
    params={
        'sort_by':'default',
        'include':'data[*].is_normal,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].author.follower_count,badge[?(type=best_answerer)].topics',
        'limit':limit,
        'offset':offset
    }
    url ="https://www.zhihu.com/api/v4/questions/"+qid+"/answers"
    return s.get(url,params=params)

def fetch_all_answers(url):
    session = init(url)
    q_id = url.split('/')[-1]
    offset = 0
    limit=20
    answers=[]
    is_end=False
    while not is_end:
        ret=fetch_answer(session,q_id,limit,offset)
        #total = ret.json()['paging']['totals']
        answers+=ret.json()['data']
        is_end= ret.json()['paging']['is_end']
        print("Offset: ",offset)
        print("is_end: ",is_end)
        offset+=limit
    return answers

def grep_image_urls(text):
    jpg = re.compile(r'https://[^\s]*?_r\.jpg')
    jpeg = re.compile(r'https://[^\s]*?_r\.jpeg')
    gif = re.compile(r'https://[^\s]*?_r\.gif')
    png = re.compile(r'https://[^\s]*?_r\.png')
    imgs=[]
    imgs+=jpg.findall(text)
    imgs+=jpeg.findall(text)
    imgs+=gif.findall(text)
    imgs+=png.findall(text)
    return imgs

url = "https://www.zhihu.com/question/29814297"
answers=fetch_all_answers(url)
folder = '29814297'
for ans in answers:
    imgs = grep_image_urls(ans['content'])
    for url in imgs:
        download(folder,url)