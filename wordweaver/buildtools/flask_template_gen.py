# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import wordweaver
from wordweaver.config import BUILD_CONFIG

class FlaskTemplateGenerator():
    def __init__(self, plt, path):
        self.plt = plt
        self.path = path
        self.pre_path = os.path.join(os.path.dirname(wordweaver.__file__), "static", self.path, "index.html")
        self.post_path = os.path.join(os.path.dirname(wordweaver.__file__), "templates", "{}.html".format(self.plt))
       
        with open(self.pre_path, 'r', encoding='utf8') as f:
            self.soup = BeautifulSoup(f, 'html.parser')
        
        self.fstring = "{{{{ url_for('static', filename='{fn}') }}}}"

    def linkify(self, fpath):
        fn = os.path.join(self.path, fpath).replace("\\","/")
        return self.fstring.format(fn=fn)
    
    def replaceLocalLinks(self):
        for css in self.soup.findAll('link'):
            if css.has_attr('href') and not css['href'].startswith('http') and not css['href'].startswith('www') and not css['href'].startswith('//'):
                css['href'] = self.linkify(css['href'])

    def replaceLocalScripts(self):
        for js in self.soup.findAll('script'):
            if js.has_attr('src') and not js['src'].startswith('http') and not js['src'].startswith('www') and not js['src'].startswith('//'):
                js['src'] = self.linkify(js['src'])
    
    def addNonce(self):
        for script in self.soup.findAll('script'):
            script['nonce'] = "{{ csp_nonce() }}"
    
    def inject(self):
        css = '''
            .bg[_ngcontent-c0] {
                background-image: url({bg_img})
                }
        '''
        new_el = self.soup.new_tag('style')
        new_el.string = css.format(bg_img=BUILD_CONFIG['flask']['bg_img'])
        self.soup.html.append(new_el)

    def createFile(self):
        self.replaceLocalLinks()
        self.replaceLocalScripts()
        self.addNonce()
        if self.plt == 'web':
            self.inject()
        with open(self.post_path, 'w', encoding='utf8') as f:
            f.write(str(self.soup))

  
