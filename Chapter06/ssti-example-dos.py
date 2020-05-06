#!/usr/bin/env python
# Code Listing #11

"""

SSTI - Server Side Template Injection example (using Flask) demonstrating a DoS attack

"""


# ssti-example-dos.py
from flask import Flask
from flask import request, render_template_string

app = Flask(__name__)
secret = 'jo5gmvlligcZ5YZGenWnGcol8JnwhWZd2lJZYo=='
TEMPLATE = '''
<html>
 <head><title> Hello {{ person.name }} </title></head>
 <body> Hello FOO </body>
</html>
'''

# 攻撃例：
# (DOS) http://localhost:5000/hello-ssti?name=Tom{{ 100*1000000 }}
# (XSS) http://localhost:5000/hello-ssti?name=Tom<script>alert("...")</script>
@app.route('/hello-ssti')
def hello_ssti():
    person = {'name': "world",
              'secret': 'jo5gmvlligcZ5YZGenWnGcol8JnwhWZd2lJZYo=='}
    if request.args.get('name'):
        person['name'] = request.args.get('name')

    # Replace FOO with person's name
    template = TEMPLATE.replace("FOO", person['name'])
    return render_template_string(template, person=person)


if __name__ == "__main__":
    app.run(debug=True)
