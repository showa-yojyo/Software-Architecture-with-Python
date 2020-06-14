#!/usr/bin/env python
# Code Listing #9

"""

SSTI - Server Side Template Injection example - using Flask

"""

# ssti-example.py
from flask import Flask
from flask import request, render_template_string

app = Flask(__name__)

# 本書の攻撃例は次のようになっている：
# http://localhost:5000/hello-ssti?name={% for item in person %}<p>{{ item, person[item] }}</p>{% endfor %}
# http://localhost:5000/hello-ssti?name={{ config }}
@app.route('/hello-ssti')
def hello_ssti():
    person = {'name': "world",
              'secret': 'jo5gmvlligcZ5YZGenWnGcol8JnwhWZd2lJZYo=='}
    if request.args.get('name'):
        person['name'] = request.args.get('name')

    template = '''<h2>Hello %s!</h2>''' % person['name']
    return render_template_string(template, person=person)


if __name__ == "__main__":
    app.run(debug=True)
