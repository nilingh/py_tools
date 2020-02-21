import multiprocessing as mp
import time
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup
import re

# base_url = "http://127.0.0.1:4000/"
base_url = 'https://morvanzhou.github.io/'


def crawl(url):
    """ 获取html"""
    response = urlopen(url)
    return response.read().decode('utf-8')


def parse(html):
    """ 获取网站中网页的title, 页面url"""
    soup = BeautifulSoup(html, 'lxml')
    # 页面中的链接是/开头和结尾/,因此这里使用了RE进行提取
    urls = soup.find_all('a', {"href": re.compile('^/.+?/$')})
    # 获取页面标题,去除空格
    title = soup.find('h1').get_text().strip()
    # 获取页面的url
    url = soup.find('meta', {'property': "og:url"})['content']
    # 构建一个集合set,保存该页面内的url, 好处是可以去重, 使用urljoin函数拼接url
    page_urls = set([urljoin(base_url, url['href']) for url in urls])
    return title, page_urls, url


if __name__ == "__main__":
    count, start_time = 1, time.time()
    # # 暂存未处理的url, 同时去重
    unseen = set([base_url, ])
    # 保存已处理的url
    seen = set()
    # #################################
    # # 普通爬虫 单进程
    # #################################
    # # DON'T OVER CRAWL THE WEBSITE OR YOU MAY NEVER VISIT AGAIN
    if base_url != "http://127.0.0.1:4000/":
        # 限制爬虫为True
        restricted_crawl = True
    else:
        restricted_crawl = False

    # # 循环取unseen集合中的url直到unseen为空
    # # 由于unseen初始从base_url开始,因此循环会从base_url开始进入
    # while len(unseen) != 0:                 # still get some url to visit
    #     # 如果是限制排重标记打开, 并且seen已经达到20则退出循环
    #     if restricted_crawl and len(seen) >= 20:
    #         break
    #     # 从unseen集合中获取url爬取htmls列表
    #     print('\nDistributed Crawling...')
    #     htmls = [crawl(url) for url in unseen]
    #     # 基于htmls列表,循环获取每个html中解析出来的
    #     print('\nDistributed Parsing...')
    #     results = [parse(html) for html in htmls]
    #     # 将处理过的unseen跟新到seen中, 然后清空unseen
    #     print('\nAnalysing...')
    #     seen.update(unseen)         # seen the crawled
    #     unseen.clear()              # nothing unseen
    #     # 将结果集合与seen求差集,如果有未处理url就更新到unseen中进行下一次循环
    #     for title, page_urls, url in results:
    #         # 对于集合可以用‘减号’求差集
    #         print(count, title, url)
    #         count += 1
    #         unseen.update(page_urls - seen)     # get new url to crawl
    # print('Total time: %.1f s' % (time.time()-start_time, ))    # 53 s

    #################################
    # 多进程爬虫 multiprocessing多进程池
    #################################
    unseen = set([base_url, ])
    seen = set()

    # 创建进程池
    pool = mp.Pool(4)
    count, start_time = 1, time.time()
    while len(unseen) != 0:
        if restricted_crawl and len(seen) > 20:
            break
        print('\nDistributed Crawling...')
        # 异步调用多进程,传参需使用元组,使用列表生成式获取结果
        crawl_jobs = [pool.apply_async(crawl, args=(url,)) for url in unseen]
        # 使用列表生成式从结果中获取html, apply_async需要使用get()方法获取返回值
        htmls = [j.get() for j in crawl_jobs]  # request connection
        print('\nDistributed Parsing...')
        # 异步调用多进程,传参需使用元组,使用列表生成式获取结果
        parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
        # apply_async需要使用get()方法获取返回值, 使用列表生成式获取结果
        results = [j.get() for j in parse_jobs]

        for title, page_urls, url in results:
            print(count, title, url)
            count += 1
            unseen.update(page_urls-seen)
    print('Total time: %.1f s' % (time.time()-start_time, ))
