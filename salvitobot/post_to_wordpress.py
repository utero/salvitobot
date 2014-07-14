# -*- coding: utf-8 -*-
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

import config

wp = Client('http://utero.pe/xmlrpc.php', config.username, config.password)
for k, v in enumerate(wp.call(GetPosts())):
    print k, unicode(v).encode("utf-8")
print wp.call(GetUserInfo())


from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts

post = WordPressPost()
post.title = 'My post test3'
post.content = 'This is a wonderful blog post about XML-RPC.'
post.id = wp.call(posts.NewPost(post))

# whoops, I forgot to publish it!
post.post_status = 'publish'
wp.call(posts.EditPost(post.id, post))
