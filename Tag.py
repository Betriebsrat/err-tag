import logging
import os
import sqlite3
from errbot import botcmd, BotPlugin


class Tag(BotPlugin):
    """Simple plugin for tagging messages or general information"""

    def activate(self):
        TAG_DB = self.plugin_dir + os.sep + 'tag.sqlite'
        if not os.path.exists(TAG_DB):
            logging.warning('no database found, creating a new one')
            open(TAG_DB, 'a').close()

        self.con = None
        try:
            self.con = sqlite3.connect(TAG_DB, check_same_thread=False)
            self.cur = self.con.cursor()
            self.cur.execute(
                'create table if not exists tags (id integer primary key, tag text not null, message text not null, author text default \'unknown\', date text default CURRENT_DATE) ;')
            self.con.commit()
        except sqlite3.Error as e:
            print(e)
        super(Tag, self).activate()

    def deactivate(self):
        self.con.close()
        super(Tag, self).deactivate()

    @botcmd(split_args_with=None)
    def tag_details(self, msg, args):
        """ Returns further details about a tag, usage !tag details <tag>"""
        if len(args) > 1:
            return 'Usage = !tag details <tag>'
        self.cur.execute('select * from tags where tag like "' + args[0] + '";')
        tag = self.cur.fetchone()
        if tag is not None:
            return 'Tag: %s Message: %s, Author: %s Date: %s' % (tag[1], tag[2], tag[3], tag[4])
        else:
            return 'No matches with id %s' % args[0]

    @botcmd()
    def tag_find(self, msg, args):
        """Searches the tags and their messages for given keyword, usage: !tag find <args>"""
        if args == '':
            return "Usage: !tag find <args>"

        self.cur.execute('select * from tags where message like ? or tag like ? order by random() limit 1;',
                         ('%' + args + '%', '%' + args + '%',))
        tag = self.cur.fetchone()
        if tag is None:
            return 'Found no matches for: %s.' % (args)
        else:
            return 'Tag: %s Message: %s' % (tag[1], tag[2])

    @botcmd(split_args_with=None)
    def get(self, msg, args):
        """Fetches a tag, usage: !get <tag>"""
        if len(args) != 1:
            return 'Usage: !get <tag>'
        self.cur.execute('select message from tags where tag like "' + args[0] + '";')
        message = self.cur.fetchone()
        if message is None:
            return 'No matches with tag \'%s\'.' % args[0]
        else:
            return '%s' % (message[0])

    @botcmd()
    def tag_new(self, msg, args):
        """Returns the latest 3 tags, usage !tag new"""
        if args != '':
            return 'Usage !tag new'
        self.cur.execute('select * from tags order by id desc limit 3;')
        rows = self.cur.fetchall()
        for row in rows:
            yield 'Tag: %s -> %s' % (row[1], row[2])

    @botcmd(admin_only=True,)
    def tag(self, msg, args):
        """Adds a new tag, usage: !tag <tag> -> <message> """
        if len(args) < 2:
            return "Usage: !tag <tag> -> <data>"
        author = msg.frm.nick
        sep = args.index('->')
        tag = ''.join(args[:sep - 1])
        message = ''.join(args[sep + 2:])
        self.cur.execute('select * from tags where tag like "' + tag + '";')
        hit = self.cur.fetchone()
        if hit is None:
            self.cur.execute('insert into tags (tag, message, author) values (?,?,?);', (tag, message, author))
            self.con.commit()
            return 'Added message for tag: %s.' % tag
        else:
            return 'Tag %s already exists.' % tag

    @botcmd(admin_only=True)
    def tag_del(self, msg, args):
        """Removes tag from database, usage: !tag del <tag>"""
        if args == '':
            return "Usage: !tag del <tag>"
        self.cur.execute('delete from tags where tag like  "' + args + '";')
        self.con.commit()
        return 'Removed tag: %s.' % args
