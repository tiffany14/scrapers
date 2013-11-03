import numpy as np

DATUM_SPLIT_SIZE = 18

# INDIVIDUAL KEYS IN EACH DATA POINT DICT
#
# "image_id"                       -> str
# "image_creation_time"            -> int
# "image_comment_count"            -> int
# "tag_list"                       -> list of strs
# "filter_type"                    -> str
# "location_longitude"             -> float
# "location_latitude"              -> float
# "location_name"                  -> str
# "caption_text"                   -> str
# "likes_count"                    -> int
# "user_username"                  -> str
# "user_id"                        -> int
# "comment_time_text_encoding"     -> list of (time,text) tuples
# "user_media_count"               -> int
# "user_followed_by_count"         -> int
# "user_follows_count"             -> int
# "user_followed_by_ids_encoding"  -> list of ints
# "user_follows_ids_encoding"      -> list of ints
#
# (returned data list is a list of dicts, each 
# corresponding to one image's worth of metadata)

def extract_from_tsv(filename, max_limit = None):
  f         = open(filename, 'r')
  key_line  = f.readline()
  key_names = key_line.strip().split('\t')

  data      = []
  count     = 0

  for line in f:
    valid_datum = True
    try:
      d = line.strip().split('\t')

      if len(d) != DATUM_SPLIT_SIZE:
        valid_datum = False

      if d[0] == "image_id":
        valid_datum = False

      datum = {}

      for n in xrange(DATUM_SPLIT_SIZE):
        data_chunk = None
        key_name   = key_names[n]


        if   n == 0:
          data_chunk = str(d[n])
        elif n == 1:
          data_chunk = int(d[n])
        elif n == 2:
          data_chunk = int(d[n])
        elif n == 3:
          if d[n] != '[]':
            data_chunk = eval(d[n])
        elif n == 4:
            data_chunk = str(d[n])
        elif n == 5:
          if d[n] != "-BLANK-":
            data_chunk = float(d[n])
        elif n == 6:
          if d[n] != "-BLANK-":
            data_chunk = float(d[n])
        elif n == 7:
          if d[n] != "-BLANK-":
            data_chunk = str(d[n])
        elif n == 8:
          if d[n] != "CAPTION_TEXT":
            data_chunk = str(d[n])
        elif n == 9:
          data_chunk = int(d[n])
        elif n == 10:
          data_chunk = str(d[n])
        elif n == 11:
          data_chunk = int(d[n])
        elif n == 12:
          try:
            time_text_pairs = d[n].split('{}')
            data_chunk = []
            for pair in time_text_pairs:
              colon_index = pair.find(':')
              time = pair[0:colon_index]
              text = pair[colon_index+1:-1]
              data_chunk.append((time,text))
          except:
            pass
        elif n == 13:
          data_chunk = int(d[n])
        elif n == 14:
          data_chunk = int(d[n])
        elif n == 15:
          data_chunk = int(d[n])
        elif n == 16:
          data_chunk = [ int(x) for x in d[n].split('{}') ]
        else:
          data_chunk = [ int(x) for x in d[n].split('{}') ]

        datum[key_name] = data_chunk

      if valid_datum:
        data.append(datum)
        count += 1
      if max_limit != None and count >= max_limit:
        break

    except:
      pass

  print "Total data points: " + str(count)
  return data

# 'sentiment analysis' w/ tags, captions, comment (time,text) tuples

def sentiment_analysis():

  # BEGIN_YOUR_CODE (around ??? lines of code expected)
  raise Exception("Not implemented yet")
  # END_YOUR_CODE

  return None

# 'location clustering' w/ longitude, latitude, location name

def location_clustering():

  # BEGIN_YOUR_CODE (around ??? lines of code expected)
  raise Exception("Not implemented yet")
  # END_YOUR_CODE
  
  return None

# 'image relevancy' w/ (last comment time - image creation time), comment count, comment (time,text) tuples, followed by count, likes count

def image_relevancy():

  # BEGIN_YOUR_CODE (around ??? lines of code expected)
  raise Exception("Not implemented yet")
  # END_YOUR_CODE
  
  return None

# 'association rules' w/ image, filter, location

def association_rules():

  # BEGIN_YOUR_CODE (around ??? lines of code expected)
  raise Exception("Not implemented yet")
  # END_YOUR_CODE
  
  return None




# NOTES: 
# 
# try PCA to 2 dimensions for some data component
#
# OBVIOUS FEATURES:
#
# filter_type
# likes_count
# image_comment_count
# user_followed_by_count
# user_follows_count
# user_media_count
#
# EXPERIMENTAL FEATURES:
#
# 'network measurements' w/ followed/follows ids
# 'burstiness' w/ comment (time,text) tuples



