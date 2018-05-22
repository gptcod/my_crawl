import requests
from lxml import etree
import pandas as pd
import numpy as np

def job51_crawl(new_file):
    data = pd.np.empty((1000000, 6)) * pd.np.nan
    df_all = pd.DataFrame(columns=['title', 'place', 'company', 'money', 'job_content', 'url'], data=data)

    i = 0
        
    for page in range(1, 200):
        print page
        site = r'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(page)
        
        for index in range(4, 54):
            if i < 1000000:
                response = requests.get(site)
                response.encoding = 'gbk'
                text = response.text

                root = etree.HTML(text)
                root_second = root.xpath(r'//*[@id="resultList"]/div[{}]'.format(index))[0]

                if len(root_second.xpath(r'./p/span/a')) == 0:
                    print('Program finished')
                    return df_all

                for name, value in root_second.xpath(r'./p/span/a')[0].items():
                    if name == 'title':
                        title = value
                        title = title.strip()

                    if name == 'href':
                        url = value



                company = root_second.xpath(r'./span[1]/a/text()')[0]
                place = root_second.xpath(r'./span[2]/text()')[0]

                if len (root_second.xpath(r'./span[1]/a/text()')) == 0:
                    money = ' '

                else:
                    money = root_second.xpath(r'./span[4]/text()')[0]

                if len (root_second.xpath(r'./span[4]/a/text()')) == 0:
                    publish_time = ' '

                else:
                    publish_time = root_second.xpath(r'./span[4]/text()')[0]


                response = requests.get(url)
                response.encoding = 'gbk'
                text = response.text
                root = etree.HTML(text)

                root_second = root.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div')
                print 'root_second', root_second
                if len(root_second) == 0:
                    job_content = ' '

                else:
                    print root_second[0]
                    for i, content in enumerate(root_second[0]):
                        if i == 1 and content.tag == u'p':
                            job_content = content.text

                row = [title, place, company, money, job_content, url]
                #row = map(str.strip, row)
                print row

                df_all.iloc[i] = row

                i = i+1
            
    df_all = df_all.drop_duplicates()
    df_all.to_excel(new_file)
    