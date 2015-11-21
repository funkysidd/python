'''
Python script for extracting review information from IMDB.
Implemented by Nidhi Singh (nis52@pitt.edu).
'''

#!/usr/bin/python

import re
import sys
import urllib2

'''
Stores user specific attributes
'''
class User:
  def __init__(self):
    self._id = ''
    self.name = ''

  def reset(self):
    self._id = ''
    self.name = ''

'''
Stores review specific attributes, including user the attribute.
'''
class Attributes:
  def __init__(self):
    self.user = User()
    self.review = ''
    self.rating = ''
    self.date = ''

  def reset(self):
    self.user.reset()
    self.review = ''
    self.rating = ''
    self.date = ''

  def to_str(self):
    return self.user._id+','+self.user.name+',\"'+self.review+'\",\"'+self.rating+'\",'+self.date

  def header():
    return 'User Id,Name,Review,Rating(out of 10),Date'
  header = staticmethod(header)

'''
Parsing utilies for various sections of the review block
'''
def parse_review(line):
  review = ''
  match = re.search(r'<a href=\"(.+?)\">(.+?)</a>', line)
  if match:
    review = match.group(2)

  return review

def parse_user_id_and_name(line):
  _user = User()
  match = re.search(r'<a href=\"/user/(.+?)/\">(.+?)</a>', line)
  if match:
    _user._id = match.group(1)
    _user.name = match.group(2)

  return _user

def parse_rating(line):
  rating = ''
  match = re.search(r'alt=\"(.+?)/(.+?)\"', line)
  if match:
    rating = match.group(1)

  return rating

def parse_date(line):
  date = ''
  match = re.search(r'<small>on (.+?)</small>', line)
  if match:
    date = match.group(1)

  return date

'''
The entry function for parsing review blocks
'''
def parse_and_write_review_blocks(url, csv_file_name):
  try:
    response = urllib2.urlopen(url)
    if response.info().gettype()=='text/html':
      review_counter = 0
      review_block_found = False

      # Opens the csv file for writing
      csv_file = open(csv_file_name, 'w')

      # Attributes we wish to store
      attributes = Attributes()

      # Writes the header to the csv file; via a static method
      csv_file.write(Attributes.header()+'\n')

      for line in response:
        if line.find('class="comment-summary"')!=-1:
          # _cntr = 1

          # Resets the attributes
          attributes.reset()

          review_block_found = True
          review_counter = review_counter+1
        else:
          if review_block_found:
            # interesting_found = False
            # if line.find('class="avatar"')!=-1:
            #   interesting_found = True
            if line.find('<h2>')!=-1:
              # interesting_found = True
              attributes.review = parse_review(line)
            elif line.find('<img')!=-1:
              # interesting_found = True
             attributes.rating = parse_rating(line)
              # if len(rating)>0: 
              #   print rating
            # elif line.find('<b>')!=-1:
            #   interesting_found = True;
            elif line.find('<a href=')!=-1:
              # interesting_found = True;
              attributes.user = parse_user_id_and_name(line)
              #if (_user._id!=-1):
              #   print _user.name
            elif line.find('<small>')!=-1:
              # interesting_found = True
              attributes.date = parse_date(line)
              # if len(date)>0:
              #   print date
            elif line.find('</td>')!=-1: 
              '''Corresponding to comment-summary'''
              # interesting_found = True
              csv_file.write(attributes.to_str()+'\n')
              review_block_found = False
      
      csv_file.close()
      print review_counter, 'reviews written to file'

    response.close()
  except IOError:
    print 'Problem reading url:', url

  return

def main():
  if len(sys.argv)>2:
    url = sys.argv[1]
    csv_file_prefix = sys.argv[2]
    csv_file_name = csv_file_prefix+'.csv'

    print 'url: ', url
    print 'csv file name: ', csv_file_name
    
    parse_and_write_review_blocks(url, csv_file_name)
  else:
    print 'Usage: [python] <script name> <quoted_url> <csv_file_prefix>'

  return

if __name__=='__main__':
  main()

