import requests
from add_data import update_data
from config import user_id
from config import total_page


def visit(page):
    url = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp'.format(
        user_id, page)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh-TW;q=0.6",
        "cookie": "buvid3=52EE1424-8352-DE0D-C2F9-8CEFBD6D7D2024853infoc; i-wanna-go-back=-1; _uuid=D7F4D7102-F510C-9EFD-B44C-5A15BB3D2B9825216infoc; buvid4=79C7023E-28E0-B231-6510-54E406718DAA25965-022021913-c0D4n8mIkOPQS7cPZ5EOlQ%3D%3D; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO7016452474409017; rpdid=|(Rlllkm)mY0J'uYRlkRmRum; buvid_fp_plain=undefined; blackside_state=0; fingerprint=6c8532a24d1ddc22356289c4c2d1958f; buvid_fp=34e58163f7b4e31c1736ba5b8416e000; SESSDATA=c35a2a31%2C1662290982%2Ca3c0d%2A31; bili_jct=de750fd4e484b47f40b8bb42a5a72869; DedeUserID=73827743; DedeUserID__ckMd5=9d571d9b5b827b73; sid=c3w73yp7; b_ut=5; hit-dyn-v2=1; nostalgia_conf=-1; PVID=2; innersign=0; b_lsid=B710CBE88_180E5C4ABA4; bp_video_offset_73827743=662643097963855900; CURRENT_FNVAL=80; b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_52EE1424%22%3A%22180E5C4B0BF%22%2C%22333.337.fp.risk_52EE1424%22%3A%22180E5C521EF%22%2C%22333.999.fp.risk_52EE1424%22%3A%22180E5C5494B%22%7D%7D",
        "origin": "https://space.bilibili.com",
        "referer": "https://space.bilibili.com/518973111/video?tid=0&page=2&keyword=&order=pubdate",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    }
    resp = requests.get(
        url=url,
        headers=headers
    )

    # print(resp.json())
    js = resp.json()
    vlist = js['data']['list']['vlist']
    bvid_list = list(map(lambda x: x.get('bvid'), vlist))
    return bvid_list


bv_list = []
for i in range(1, total_page + 1):
    bv_list.extend(visit(i))
    print(bv_list)
list(map(lambda x:update_data(x,1,1),bv_list))

