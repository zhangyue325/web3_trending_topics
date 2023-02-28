import wechatsogou
import ddddocr

OCR = ddddocr.DdddOcr(ocr=True, show_ad=False, use_gpu=True, old=True,beta=True)

ws_api = wechatsogou.WechatSogouAPI()
data = ws_api.get_gzh_article_by_history("六维数据")
print(data)