import requests
import re
import argparse


# CONST
proxies = {
    'burp': 'http://127.0.0.1:8080'
}

def arguments():
    parser = argparse.ArgumentParser(description="Nah.")
    parser.add_argument("-q", "--query", help="Search query (required)", required=True)
    parser.add_argument("-e", "--engine", help="Provide search engine (default: Google)", default=None)
    parser.add_argument("-p", "--page", help="Specify nubmer of pages (default: 1)", default=1, type=int)
    parser.add_argument("-x", "--proxy", help="Use Burp Proxy", default=None)
    return parser.parse_args()

def get(url, proxies=None):
    if proxies:
        req = requests.get(url=url, proxies=proxies)
        return str(req.content)
    else:
        req = requests.get(url=url)
        return str(req.content)
    
def engine(engine):
    if engine == 1:
        return {
            "url": "https://www.google.com/search?",
            "params": "q=" + args.query + "&gws_rd=cr,ssl&client=ubuntu&ie=UTF-8&start=",
            "regex": "\"><a href=\"\/url\?q=(.*?)&amp;sa=U&amp;"
        }      
    elif engine == 2:
        return {
        "regex": "</li><li class=\"b_algo\"><h2><a href=\"(.*?)\" h=\"ID=SERP,",
		"url": "https://www.bing.com/search?",
		"params": "q=" + args.query + "&first="
        }        
    
def query(url, re):

    results_urls = []

    for page in range(0, args.page+1):
        if str(args.engine).lower() == "bing":
            pagination_url = url + (str(page * 10 + 1))
        else:
            pagination_url = url + (str(page * 10))
                    
        results = get(url=pagination_url, proxies=args.proxy)
        parsed_urls = parse(regex=re, parse=results)

        if len(parsed_urls) == 0:
            counter = 0
            breaker = False
            while breaker is False:
                results = get(url=pagination_url, proxies=args.proxy)
                parsed_urls = parse(regex=re, parse=results)

                if len(parsed_urls) > 0:
                    breaker = True
                elif counter != 5:
                    counter += 1
                else:
                    breaker = True
            
        results_urls.extend(parsed_urls)
        
    return results_urls


def parse(parse, regex):
    match = re.compile(regex)
    return match.findall(parse)


if __name__ == "__main__":
    args = arguments()
    
    if args.engine is None or str(args.engine).lower() == "google":
        final_result = query(url=engine(1)["url"] + engine(1)["params"], re=engine(1)["regex"])
    
    elif str(args.engine).lower() == "bing":
        final_result = query(url=engine(2)["url"] + engine(2)["params"], re=engine(2)["regex"])
    
    elif str(args.engine).lower() == "all":
        final_result = []
        final_result.extend(query(url=engine(1)["url"] + engine(1)["params"], re=engine(1)["regex"]))
        final_result.extend(query(url=engine(2)["url"] + engine(2)["params"], re=engine(2)["regex"]))

    else:
        print("Invalid Engine")
        quit()

    print("\n".join(sorted(list(set(final_result)))))