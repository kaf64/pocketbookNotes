import pdfkit


class Adapter:
    def __init__(self):
        self.fileRead = ''
        self.fileWrite = ''
        self.soup = None

    def wrap_list_html(self, list) -> str:
        return f"""
        <div class="bookmark">
            <p class="bm-page">{list[0]}</p>
            <div class="bm-text">
            <p> {list[1]}</p>
            </div>
        </div>
       """

    def wrap_html(self, html_content):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
    <style type="text/css"><!--/*--><![CDATA[/*><!--*/
div.bm-color-none   {{background-color:#eae6dc;}}
div.bm-color-pink   {{background-color:#ecd6ea;}}
div.bm-color-blue   {{background-color:#d2ebff;}}
div.bm-color-red    {{background-color:#fcc1c1;}}
div.bm-color-yellow {{background-color:#fff3b2;}}
div.bm-color-green  {{background-color:#d8f4cf;}}

div.bm-delim {{
background-color: #d6d2c9;
height: 1px;
width: 100%;
border-bottom:1px solid #fffaec;
}}

p.bm-page:before {{content: open-quote;}}
p.bm-page:after  {{content: close-quote;}}
p.bm-page:lang(ru) {{quotes: "стр. № " "." "'" "'";}}
p.bm-page:lang(uk) {{quotes: "стор. № " "." "'" "'";}}
p.bm-page:lang(de) {{quotes: "Seite Nr " "." "'" "'";}}
p.bm-page:lang(fr) {{quotes: "page No " "." "'" "'";}}
p.bm-page:lang(zh) {{quotes: "頁 " "." "'" "'";}}

p.bm-page
{{
quotes: "page # " "." "'" "'";
color: #999999;
font-size: 14pt; 
font-family: Geneva, Arial, Helvetica, sans-serif;
}}

div.bookmark
{{
font-size: 14pt;
text-align: justify;
color: #222222;
padding: 10px 40px;
}}

div.bm-text
{{
font-family: Geneva, Arial, Helvetica, sans-serif;
}}

div.bm-note 
{{
color: #999999;
font-style: oblique;
position: relative;
padding: 5px 20px;
background: #fffaec;
-webkit-border-radius: 5px;
border-radius: 5px;
border: #d3d3d3 solid 1px;
}}

div.bm-note:after 
{{
content: '';
position: absolute;
border-color: #fffaec transparent;
display: block;
width: 0;
z-index: 2;
top: -14px;
left: 51px;
height: 0;
border-bottom: 15px solid #fffaec; 
border-right: 24px solid transparent;
}}

div.bm-note:before 
{{
content: '';
position: absolute;
display: block;
width: 0;
z-index: 1;
top: -15px;
left: 50px;
height: 0;
border-bottom: 15px solid #d3d3d3; 
border-right: 24px solid transparent;	
}}

div.bm-image
{{
width: 100%;
height: auto;
text-align: center;
}}

div.bm-image img
{{
max-width: 100%;
min-height: auto;
}}
/*]]>*/--></style>
        </head>
        <body>
            <div style="width=100%">
            {html_content}
            </div>
        <body>
        </html>
        """

    def open_file(self, path):
    # open file
        try:
            self.fileRead = open(path, 'r', encoding="utf8")
        except Exception:
            return 0
        return self.fileRead

    def save_file(self, path, content):
        html_content = ''
        #self.fileWrite = open(path, 'w')
        for item_list in content:
            html_content += self.wrap_list_html(item_list)
        html_page = self.wrap_html(html_content)
        try:
            if path.endswith(".pdf"):
                pdfkit.from_string(html_page, path)
            elif path.endswith(".html"):
                with open(path, 'w', encoding="utf-8") as file:
                    file.write(html_page)
        except Exception as e:
            # TODO handle error by tkinter message
            pass
