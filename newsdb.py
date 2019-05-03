#!/usr/bin/env python

import psycopg2

# Class connects to the Database, returns a cursor and closes
# the database connection


class ConnectDb:
    def __init__(self, db_name, db_connect):
        self.db_name = db_name
        self.db_connect = db_connect

    def openConnectDb(self):
        self.db_connect = psycopg2.connect("dbname="+self.db_name)
        db_cursor = self.db_connect.cursor()
        return db_cursor

    def closeConnectDb(self):
        self.db_connect.close()


# function to select the most popular articles
def popularArticles():
    connect_to_psql = ConnectDb('news', 'db_connect')
    c = connect_to_psql.openConnectDb()
    c.execute("select path,count(path) as views from \
    log group by path order by views desc limit 4")
    results = c.fetchall()
    print("Most popular articles of all ")
    for article in (results[1:4]):
        print(str(article[0][9:]) + " -- " +
              str(article[1]) + " views")
    print("\n")
    connect_to_psql.closeConnectDb()


# function to select the most popular articles
def popularAuthors():
    connect_to_psql = ConnectDb('news', 'db_connect')
    c = connect_to_psql.openConnectDb()
    c.execute("select authors.name,author_views.views from \
    author_views,authors where authors.id = \
    author_views.author")
    results = c.fetchall()
    print("Most popular authors of all time")
    for author in results:
        print(str(author[0]) + "  -- " + str(author[1]) +
              " views")
    print("\n")
    connect_to_psql.closeConnectDb()


# function to select days with errors of more than 1%
def getMostErrors():
    connect_to_psql = ConnectDb('news', 'db_connect')
    c = connect_to_psql.openConnectDb()
    c.execute("select * from date_error_log")
    results = c.fetchall()
    print("Errors above 1%")
    for errors in results:
        percent_error = (100 * float(errors[1]) / float(errors[2]))
        if percent_error > 1:
            day_date = (errors[0]).strftime('%d %b,%Y')
            print("%s --  %2.1f%s errors" % (day_date, percent_error, '%'))
    connect_to_psql.closeConnectDb()


# Get information results
popularArticles()
popularAuthors()
getMostErrors()
