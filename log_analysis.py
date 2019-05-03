# !/usr/bin/env python3


# Import libraries.
import psycopg2
from datetime import date


# Global database name.
DBNAME = 'news'


# Define executeQuery() function.
def executeQuery(query):
    """ This function will try to connect and perform the query.
    Then, fetch the results in a variable and return.
    It's useful for re-usability."""
    try:
        db = psycopg2.connect(database=DBNAME)
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        db.close()
        return rows
    except BaseException:
        print("Unable to connect to the database.")


# functions()
def top_three_articles():
    """ This function sets the variable "query" for selecting the
    FIRST THREE rows of the table/view created "top_articles.
    Then prints the results."""
    query = """select *
                from top_articles
                order by total_views desc
                limit 3;"""
    results = executeQuery(query)

    print('** List of the top 3 visited articles **')

    for i in results:
        print('"' + i[0] + '" | ' + str(i[1]) + " views")
    print(" ")


def top_three_authors():
    """ This function uses the views "top_articles"
    and "titles_by_author"and sums the total views,
    then select top 3 names of the authors, ordered by views."""
    query = """select name as top_three_authors,
    sum(top_articles.total_views) as views
    from titles_by_author, top_articles
    where titles_by_author.title = top_articles.title
    group by top_three_authors
    order by views desc
    limit 3;"""
    results = executeQuery(query)

    print('** List of the top 3 most popular Authors **')

    for i in results:
        print(i[0] + ' | ' + str(i[1]) + ' views')
    print(' ')


def high_error_days():
    """ This query calculates the percentage of error
    codes in one day. Then, select the days where
    the percentage was above 1 percent."""
    query = """select to_char(errors.day, 'Mon DD, YYYY'),
    ROUND(((errors.errors/total.total) * 100)::DECIMAL, 2)::TEXT as percentage
    FROM errors, total
    WHERE total.day = errors.day
    AND (((errors.errors/total.total) * 100) > 1.0)
    ORDER BY errors.day;"""
    results = executeQuery(query)

    print('** Days Which Errors Exceeded 1%' + ' of Total Views **')

    for i in results:
        print(i[0] + " | " + i[1] + "%" + " errors")
    print(' ')


if __name__ == '__main__':
    """
    Execute the functions in the __main__ scope"""
    print(" ")
    print("--- Generating Results ---")
    print(" ")

    top_three_articles()
    top_three_authors()
    high_error_days()
