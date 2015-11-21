Platform: 

IMDB 

Motivation:

Copy pasting review information from IMDB can be a tedious task, especially for
movies with a huge number of reviews. Safe Haven for example has 680 reviews,
where each review has 5 attributes.

This presents the motivation for automating this task through computer script or
code. More importantly the script can be standardized for extracting useful
information for any movie listed on IMDB.

Technique for extracting data:

IMDB lists user reviews in an indexed format that can be accessed using a static
URL. For example reviews for the movie Safe Haven can be accessed from the
following link,

http://www.imdb.com/title/tt1702439/reviews-index?start=0;count=131

The start and the count parameters represent the first review and the number of
reviews to be displayed thereon. In the example above, the URL requests 131
reviews starting with the review 1 (indexed at 0) from the web server.  The
highlighted portion of the URL represents a unique identifier for a movie.  The
parameters above can be modified to query reviews for any movie listed on IMDB.

A python script is used to parse the html response returned by the web server,
extract pertinent review blocks and write them to a file.

Requirements:

Python 2.7

