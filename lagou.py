from urllib import request,parse
import json,time,xlwt


line = 1
def download(page_all):
    global line
    # 创建一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 在电脑桌面右键新建一个Excel文件，其中就包含sheet1，sheet2，sheet3三张表
    sheet = book.add_sheet('test', cell_overwrite_ok=True)
    # 创建一个职位信息名称列表
    position_name_list = ['companyId', 'positionName', 'workYear', 'education', 'jobNature', 'positionId', 'createTime',
                          'city', 'companyLogo', 'industryField', 'positionAdvantage', 'salary', 'companySize',
                          'approve', 'companyShortName', 'positionLables', 'industryLables', 'publisherId',
                          'financeStage', 'companyLabelList', 'district', 'latitude', 'formatCreateTime',
                          'resumeProcessRate', 'resumeProcessDay', 'imState', 'lastLogin', 'firstType', 'secondType',
                          'isSchoolJob', 'companyFullName']
    # 把键先添加到excle表中
    for i in range(0, len(position_name_list)):
        # 向表test中添加数据
        sheet.write(0, i, position_name_list[i])  # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容

    for page in range(1,page_all):
        time.sleep(3)
        #请求地址
        base_url = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0"
        if page==1:
            first="true"
        else:
            first="false"
        data = {
            "first":first,
            "pn":page,
            "kd":"python"
        }
        #将data转码并拼接
        data = parse.urlencode(data)
        #创建headers
        headers = {
            "Accept":"application/json, text/javascript, */*; q=0.01",
            #"Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Content-Length":len(data),
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"index_location_city=%E5%8C%97%E4%BA%AC; user_trace_token=20180306162739-3bac48e9-2118-11e8-b126-5254005c3644; LGUID=20180306162739-3bac4bc0-2118-11e8-b126-5254005c3644; JSESSIONID=ABAAABAAAGFABEF890255754A4A7FCA9A2A51FD31F48384; hideSliderBanner20180305WithTopBannerC=1; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Ddln2ggBgVb0YpqUEEtLDTNfboMogQOiCVGS27sTtCk_%26wd%3D%26eqid%3Dba4a2ace00074cad000000035aa26e34; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_search; SEARCH_ID=f338882fd1564bdf9e8674d9f6dfc80b; _gid=GA1.2.1698047664.1520594488; _ga=GA1.2.1581909504.1520324852; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520324858,1520594488; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520595130; LGSID=20180309192133-05d9f3b3-238c-11e8-b1a6-5254005c3644; LGRID=20180309193218-8657498e-238d-11e8-b1a6-5254005c3644",
            "Host":"www.lagou.com",
            "Origin":"https://www.lagou.com",
            "Referer":"https://www.lagou.com/jobs/list_python?px=default&city=%E5%85%A8%E5%9B%BD",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "X-Anit-Forge-Code":"0",
            "X-Anit-Forge-Token":"None",
            "X-Requested-With":"XMLHttpRequest",
        }

        #创建请求信息对象,伪装成浏览器
        req = request.Request(url=base_url,data=bytes(data,encoding="utf-8"),headers=headers)
        response = request.urlopen(req) #请求json文件,positionAjax.json
        html = response.read().decode("utf-8")
        #将请求到的json格式转换为python对象格式
        html_json = json.loads(html)

        #print(html_json)
        #print(html_json["content"]["hrInfoMap"])#hr信息
        #print(type(html_json["content"]["hrInfoMap"]))#hr信息,dict

        #print(html_json["content"]["positionResult"])
        print(html_json["content"]["positionResult"]["result"])#每页的所有职位列表,一个职位是一个字典
        all_position = html_json["content"]["positionResult"]["result"]
        #print(html_json["content"]["positionResult"]["result"][0])#其中一个职位的信息


        # position_name_list = ['companyId','positionName','workYear','education','jobNature','positionId','createTime','city','companyLogo','industryField','positionAdvantage','salary','companySize','score','approve','companyShortName','positionLables','industryLables','publisherId','financeStage','companyLabelList','district','latitude','formatCreateTime','resumeProcessRate','resumeProcessDay','imState','lastLogin','firstType','secondType','isSchoolJob','subwayline','companyFullName']
        # 删除掉不需要的键

        #循环职位列表(就是每次插入多少行)
        for i in range(len(all_position)):
            # 循环键列表(就是每次插入多少列)
            row = 0
            for key in position_name_list:
                #print(all_position[i][key])
                if all_position[i][key]:
                    sheet.write(line, row, all_position[i][key])  # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容
                else:
                    sheet.write(line, row, "空")
                row +=1
            line+=1
        print("------------------------%d----------------------------"%line)
        # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'e:\test1.xls')  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错


if __name__=="__main__":
    download(31)
