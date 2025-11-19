import requests
import json
import time
import DBManager as dbm

class IXIC:
    def __init__(self):

        self.url = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'
        self.headers = {
            'Accept':'application/json, text/plain, */*',
            'Accept-Encoding':'gzip, deflate, br, zstd',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Origin':'https://xueqiu.com',
            'Priority':'u=1, i',
            'Referer':'https://xueqiu.com/S/SH600519',
            'Cookie':'cookiesu=521725703998609; device_id=9bbe6c3575ad6f51a3db86a9fc8e4e95; xq_a_token=7716f523735d1e47a3dd5ec748923068ab8198a8; xqat=7716f523735d1e47a3dd5ec748923068ab8198a8; xq_r_token=0483ea3986e45954e03c9294444a1af14d7579d3; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTczMzEwMDgxNywiY3RtIjoxNzMxNDk2NTc1NjMxLCJjaWQiOiJkOWQwbjRBWnVwIn0.RB9wkC6RvArOAgPTLHl7-HjAyvRpF9ttp8MJFhQ0v_CZ7465jN0sHL2vPovRKAuI0_CZ4lnk_jXY1DbVs9a-4KOzdOwuZEZV1zXfqZksKeDECsNIRuUDjoYIiqdepgq9TZULi2h3XgGH2KTNGNPEOSiG_V9EsiS83MJqGw1Rf3BEyuXQwI1Dtkgvn1qsWZ97jIzXgbxd9Q-kqbphYxVLQcDmUt3l38lV8viZ-UTpWEP85mOaGqGN_JnE0r0rCe-D6Ad324iEz5sVxwUKUkqRTP4dTKm_ZIQEFITIUH6veNsczjhHNHuFCae8ka5Y_JyabZ81ZwVBZ-tVRr_m-9zkZA; u=521725703998609; is_overseas=0; Hm_lvt_1db88642e346389874251b5a1eded6e3=1729337755,1731496591; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1731496591; HMACCOUNT=4DE46E99F3D985C3; ssxmod_itna=WqmxgD97DQdiwqBPxBR+b+G7DyDIruoODD5q=whYim=D/nWxnqD=GFDK40EYk5RPTFi70+xqCanuKtdBB3247YK70Pi5UmKQqGLDmKDylmrTdDxEq0rD74irDDxD3vxneD+D04CMyhqi3D4qDRDAQDzdQBBDASGT=DmdiDGwIXD7QDIkUPDDXK8YKDe4DwDYPBUMdYdlbDAuwMniqBD0UQxBLx01xBIQy1H7XM+1FT1r6qNeGuDG64hqGm4Mb3ILNTvYd4mGdb+Do=D2e5F0qemBAx4hDeBi42HGe=tDmGnY+Mu5DAn7xlvc3eD=; ssxmod_itna2=WqmxgD97DQdiwqBPxBR+b+G7DyDIruoODD5q=whYieG98cFnDBdUx7PNbvkqN+PuY0gKGFimuw0xKgg2r=bKOSrEn+zR=7KX+eRrMLyCxH7lLInuQN9hb9ssRcAIkMIoclX8Ocq=K1gDPbwacQeavhPh+OE1wktjpHd0eF2r0Qd80a8evbdShxyA5IP2hOSru+eamTsFvEgGoh13MCPoczwamAzen+HhmCdb7FMaH+p/pOeAhm8nywh1TR4hW+xhDrSEen+bfiBDtxVCKyFLc=eB0XtG7Xp33btib=cPH7oInQskM+KOQaaDSDtiaECZo4QGUAhCEQtjQVgjAELc=f52hOQ0t7Lbmqhho1me0WqzG+ZxAzc6M6NzlpqYmd8AUCE8i05a38gmSc3wiePoIDUIIlAS2e0ExmGW7ZP5iqIfUPWXjWAEhndKqPIE6o2Lrbioub1WV2mfhPOffS7KrmozmfQE9kGDemEY+DyPuyFLuxY/tFi0vCGRKrIb37vRNfrbIBElFWB+atiy+QF9c9uBN20wMtnVrXtvYqDgVO+SK9QcNPcHOc4DQKxUM3EKp8ntjwAxWQ75cBDrK4ICmUkWXX2Efrw3iU9ZDi0TrFRPWwz02a55RcDohWpZiU/HQD0OKgn+oLbK1exeX5F72xscVgD3k9LygoUSdMqD08DijGm4BkNqi',
            'Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-site',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }


    def get_response(self,date):
        nowtime = int(time.time() * 1000.0)
        print("当前时间: ",nowtime)
        param_data = {
            'symbol':'.IXIC',
            'begin':str(nowtime),
            'period':'day',
            'type':'before',
            'count':'-284',
            'indicator':'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
        }
        print("开始爬取数据")
        response = requests.get(self.url,headers=self.headers,params=param_data,timeout=5)
        print(response.text)
        print("爬取成功，数据包如上")

        data_json = json.loads(response.text)  # Json反序列化
        items = data_json['data']['item']
        # for i in range(len(items)):
        # print(items[i])
        # json数据对应
        # [0] timestamp
        # [1] 成交量
        # [2] 开盘价
        # [3] 最高价
        # [4] 最低价
        # [5] 收盘价
        # [6] 涨跌额
        # [7] 涨跌幅
        # [8] 换手率
        # [9] 成交额(亿)
        # [10] null
        # [11] null
        # [12]
        return items



if __name__ == '__main__':
    mt = IXIC()
    items = mt.get_response(1)
    print("清理数据库，然后开始插入")
    dbm.clearDB()
    dbm.sendData(items)
    print("插入完成")


# create table IXIC(
#     timesamp bigint not null,
#     volume bigint not null,
#     open decimal(20,4) not null,
#     high decimal(20,4) not null,
#     low decimal(20,4) not null,
#     close decimal(20,4) not null,
#     chg decimal(20,4) not null,
#     percent decimal(20,4) not null,
#     turnoverrate decimal(20,4) not null,
#     amount decimal(30,1) not null
# );