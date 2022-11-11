import http.client, urllib.parse
import mwparserfromhell
import json

class DYK:
    def __init__(self) -> None:
        self.conn = http.client.HTTPSConnection("petscan.wmflabs.org")

    def getRandomFact(self) -> str:
        contents = self.getRandomPage()
        """ Go through each line in contents to find any that starts with case-insetive dyk"""
        w = mwparserfromhell.parse(contents)
        for t in w.filter_templates():
            if t.name.lower().startswith('dyk'):
                x = t.get('entry').value.strip_code()
                """ Find the first ... in the string and return everything to the right """

                return {
                    "text": x[x.find('...')+3:].strip(),
                    "url": "https://en.wikipedia.org/wiki/%s" % self.title
                }


    def getRandomArticle(self) -> str:
        # payload = "language=en&project=wikipedia&categories=Wikipedia%2BDid%2Byou%2Bknow%2BarticlesWikiProject%2BIndia%2Barticles&combination=subset&ns%5B1%5D=1&search_max_results=1&format=json&sortby=random&output_limit=1&doit=Do%2Bit!"
        payload = {
            'language': 'en',
            'project': 'wikipedia',
            'categories': 'Wikipedia Did you know articles \nWikiProject India articles',
            'combination': 'subset',
            'ns[1]':'1',
            'search_max_results':'1',
            'format':'json',
            'sortby':'random',
            'output_limit':'1',
            'doit': 'Do it!'
        }

        body = urllib.parse.urlencode(payload)

        self.conn.request("POST", "/", body, headers = {"Content-type": "application/x-www-form-urlencoded"})

        res = self.conn.getresponse()
        data = res.read().decode('utf-8')

        article = json.loads(data)['*'][0]['a']['*'][0]
        self.title = article['title']
        return "%s:%s" % (article['nstext'], article['title'])

    def getRandomPage(self) -> str:
        self.article = self.getRandomArticle()
        p = {
            "action": "parse",
            "page": self.article,
            "format": "json",
            "prop": "wikitext"
        }

        q = urllib.parse.urlencode(p)

        conn = http.client.HTTPSConnection("en.wikipedia.org")
        conn.request("GET", "/w/api.php?" + q)

        data = conn.getresponse().read()
        return json.loads(data.decode("utf-8"))['parse']['wikitext']['*']
        