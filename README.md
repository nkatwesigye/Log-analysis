

1) ## Three  views were created to solve the second problem to select the most
popular authors:
 - slug:
     <p> This view selects the log path from the log table and replaces the
     "/article" string with and empty string and aggregates the slug column
     into a views column counting similar slugs

     command to recreate the slug view:
     ----------------------------------
     ``create view slug as SELECT replace(log.path, '/article/', '')
     AS name , count(*) as views from log group by name order by views desc;``
     </p>
 - article_authors:
     <p> This view selects authors from the articles by their ids and matches them
     up with the views from the slug view , there by allowing us to see which
     ids have how many views.
     This view however still has duplicate authors with different total views

     command to recreate the article_authors view:
     --------------------------------------------
     ``create view article_authors as select
     articles.author,articles.slug,slug.name,slug.views from articles left join
     slug on articles.slug = slug.name;``
     </p>
 - author_views
     <p> This view selects the author id and sums up the total number of views for
     each author including authors with multiple articles

     command to recreate the author_views view:
     --------------------------------------------
     ``create view author_views as select author,sum(views) as views
     from article_authors group by author order by views desc;``
     
    NOTE:
    The final query used in the python code consolidates the author_views
    and authors table to select the most popular authors

    command to  query most popular authors using the above author_views:
    --------------------------------------------------------------------
    ``select authors.name,author_views.views from author_views,authors
    where authors.id = author_views.author;``
    </p>


2) ## Two views were created to solve the date with errors above 1% ##

- date_errors
    <p> This view selects the errors for each date from the log table , it also
    converts the long datetime format to only date for the date column

    command to recreate the author_views view:
    ------------------------------------------
    ``create view date_errors as select time::timestamp::date  as date ,
      count(*) from log where status != '200 OK' group by date order by
      count desc;``
   </p>
- date_error_log
    <p> This view consolidates the date,errors for each day and the total logs
    for that day. This view allows us to parse this information using python to
    generate the percentage of logs that show up as errors for each day .

    command to recreate the author_views view:
    ------------------------------------------
    ``create view date_error_log as select date_errors.date,date_errors.count
    as errors ,date_logs.count as all_logs from date_errors,date_logs where
    date_errors.date = date_logs.date;``
    </p>
