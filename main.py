#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import cgi
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
import json

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template


class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Page(db.Model):
    title = db.StringProperty()
    content = db.TextProperty()
	
class MainPage(webapp.RequestHandler):
    def get(self):
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
            }

        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')
		
class makePages(webapp.RequestHandler):
    def get(self):
        page = Page()
        page.content = "PAGE CONTENT!!"
        page.title = "PAGE title"
        page.put()
        page = Page()
        page.content = "<p>The center panel automatically grows to fit the remaining space in the container that isn't taken up by the border regions.</p><hr><p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Sed metus nibh, sodales a, porta at, vulputate eget, dui. Pellentesque ut nisl. Maecenas tortor turpis, interdum non, sodales non, iaculis ac, lacus. Vestibulum auctor, tortor quis iaculis malesuada, libero lectus bibendum purus, sit amet tincidunt quam turpis vel lacus. In pellentesque nisl non sem. Suspendisse nunc sem, pretium eget, cursus a, fringilla vel, urna. Aliquam commodo ullamcorper erat. Nullam vel justo in neque porttitor laoreet. Aenean lacus dui, consequat eu, adipiscing eget, nonummy non, nisi. Morbi nunc est, dignissim non, ornare sed, luctus eu, massa. Vivamus eget quam. Vivamus tincidunt diam nec urna. Curabitur velit. Quisque dolor magna, ornare sed, elementum porta, luctus in, leo.</p>"
        page.title = "more text"
        page.put()
        page = Page()
        page.content = "<p><b>Done reading me? Close me by clicking the X in the top right corner.</b></p><p>Vestibulum semper. Nullam non odio. Aliquam quam. Mauris eu lectus non nunc auctor ullamcorper. Sed tincidunt molestie enim. Phasellus lobortis justo sit amet quam. Duis nulla erat, varius a, cursus in, tempor sollicitudin, mauris. Aliquam mi velit, consectetuer mattis, consequat tristique, pulvinar ac, nisl. Aliquam mattis vehicula elit. Proin quis leo sed tellus scelerisque molestie. Quisque luctus. Integer mattis. Donec id augue sed leo aliquam egestas. Quisque in sem. Donec dictum enim in dolor. Praesent non erat. Nulla ultrices vestibulum quam.</p>"
        page.title = "and more"
        page.put()
        self.redirect('/')

class deletePages(webapp.RequestHandler):
    def get(self):
        
        
        query = Page.all()
        entries =query.fetch(1000)
        db.delete(entries)
        self.redirect('/')
	
class GetStuff(webapp.RequestHandler):
    def get(self):
		encoder = simplejson.JSONEncoder()
		greetings = []
		for greeting in Greeting.all():
			item = {'author' : greeting.author,
					  'content' : greeting.content,
					  'date' : str(greeting.date)}
			greetings.append(item)
		jresp   = encoder.encode(greetings)
		#self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(jresp)

class getPages(webapp.RequestHandler):
    def get(self):
		encoder = simplejson.JSONEncoder()
		pages = []
		for page in Page.all():
			item = {'title' : page.title,
					  'content' : page.content}
			pages.append(item)
		jresp   = encoder.encode(pages)
		#self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(jresp)


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook),
									  ('/GetStuff', GetStuff),
                                      ('/getPages', getPages),
									  ('/makePages', makePages),
									  ('/deletePages', deletePages)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()