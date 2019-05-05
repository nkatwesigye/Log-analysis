# Log Analysis Reporting Tool
## Tool Description

This is a log analysis reporting tool for an online newspaper.
The newspaper platform provides the capability to log access to the newspaper
articles in real time driven with all the logs stored in an Postgres Database.  
The database contains newspaper articles, as well as the web server log for
the site.  
The log has a database row for each time a reader loaded a web page.  
The Log analysis tool is design to allow the newspaper platform's administrators
view site's user activity.  
The log analysis reporting tool is implemented in python2.7 with a backend
Postgres SQL database.  
The `psycopg2` module is used to setup the database connection and perform
the respective SQL queries to produce the information required to answer
the 3 problems.  
A  total of 7 veiws are required to solve all the 3 log analysis problems for
the user-facing newspaper site .  
If the all the views are created correctly running the query below will
give you the results displayed

   ```sql
    select table_name from INFORMATION_SCHEMA.views
    WHERE table_schema = ANY
    (current_schemas(false));
    ```

    Expected views in the result  


    table_name   
    slug
    article_authors
    author_views
    popularby_slug
    date_errors
    date_logs
    date_error_log


## Database setup instructions

### Environment setup:
The following steps will reproduce the environment which allows for the tool
to function:
* The data at
[log data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
enables the creation of database and imports  log data which the tool will analyze:  
`psql -d news -f newsdata.sql` to import the data

### Database views setup
1. ###  A single view is required to solve the first problem selecting the most
What are the most popular three articles of all time?
  - #### popularby_slug view:
      This view provides a list of the top 3 articles by slug with their
      respective number of views

      ##### command to recreate the popularby_slug view:
      ```sql
      create view popularby_slug as
      SELECT replace(log.path, '/article/', '')
      AS slug , count(*) as views from log
      where path != '/' group by slug order
      by views desc limit 3;
      ```

2. ### Three  views are required to solve the second problem to select the most
Who are the most popular article authors of all time?
 - #### slug view:
      This view selects the log path from the log table and replaces the
     `/article` string with and empty string and aggregates the slug column
     into a views column counting similar slugs

     ##### command to recreate the slug view:
     ```sql
     create view slug as SELECT
       replace(log.path, '/article/', '')
     AS name , count(*) as views from
     log group by name order by views desc;
     ```

 - #### article_authors view:
     This view selects authors from the articles by their ids and matches them
     up with the views from the slug view , there by allowing us to see which
     ids have how many views.
     This view however still has duplicate authors with different total views

     ##### command to recreate the article_authors view:
     ```sql
     create view article_authors as select
     articles.author,articles.slug,
     slug.name,slug.views from articles left join
     slug on articles.slug = slug.name;
     ```
 - #### author_views view:
     This view selects the author id and sums up the total number of views for
     each author including authors with multiple articles

     ##### command to recreate the author_views view:
     ```sql
     create view author_views as
     select author,sum(views) as views
     from article_authors group by
     author order by views desc;
     ```

    NOTE:
    The final query used in the python code consolidates the author_views
    and authors table to select the most popular authors

    ##### command to  query most popular authors using the above author_views:
    ```sql
    select authors.name,author_views.views
    from author_views,authors
    where authors.id = author_views.author;
    ```

3. ### Three views are required to solve the date with errors above 1% ##
On which days did more than 1% of requests lead to errors?
- #### date_errors view:
    This view selects the errors for each date from the log table , it also
    converts the long datetime format to only date for the date column

    ##### command to recreate the author_views view:
    ```sql
    create view date_errors as
    select time::timestamp::date  as date,
    count(*) from log where status != '200 OK'
    group by date order by
    count desc;
     ```
- #### date_logs view:
    This view selects the total logs for each day as date and sums them
    up as count , ordered from highest to lowest number of logs  

    ##### command to recreate the date_logs view:  
    ```sql
    create view date_logs as
    select time::timestamp::date
    as date , count(*) from log  
    group by date order by count desc;
    ```
- #### date_error_log view:
    This view consolidates the date,errors for each day and the total logs
    for that day. This view allows us to parse this information using python to
    generate the percentage of logs that show up as errors for each day

    ##### command to recreate the author_views view:
    ```sql
    create view date_error_log as select date_errors.date,date_errors.count
    as errors ,date_logs.count as all_logs from date_errors,date_logs where
    date_errors.date = date_logs.date;
    ```

## Tool usage:
  Requires python module `psycopg2`  and a running instance of `postgresql` with
  the news database to run successfully.
  #### Tool execution:
  `python newsdb.py`

## License

Log analysis tool is Copyright © 2008-2019 nkatwesigye . It is free software,
and may be redistributed under the terms specified in the
[LICENSE](https://creativecommons.org/licenses/by/3.0/us/) file.
