from urllib2 import urlopen
import csv
import json
import argparse
from time import sleep

# parser = argparse.ArgumentParser(description='Process String Arguments')

NUMBER_OF_CALLS  = 2000        # Each image takes up about 3 API calls for auxiliary information, and one full cycle costs about 50 API calls since popular media returns about 16 images
NO_INFORMATIONS  = "-BLANK-"
C_TIME_TEXT_ENC  = "{}"

base_url         = 'https://api.instagram.com/v1'
authorization_t  = '?access_token='
# Info Types
media_by_popular = '/media/popular'
media_by_id      = '/media/{}'
users_by_id      = '/users/{}'
users_follows    = '/users/{}/follows'
users_followers  = '/users/{}/followed-by'

def construct_url(base, info_type, access_token, num_id = ''):
  info_and_id = info_type.replace('{}', num_id)
  return base + info_and_id + access_token

def insta_pull(address):
  # url = 'https://api.instagram.com/v1/media/popular?access_token=616157282.1fb234f.92d22888661747c2b364e0e65d96180e'
  # return json.loads(urlopen(url).read())
  return json.loads(urlopen(address).read())

with open("instascrape.tsv", "a") as f:
  fieldnames = ("image_id",
                "image_creation_time",
                "image_comment_count",
                "tag_list",
                "filter_type",
                "location_longitude",
                "location_latitude",
                "location_name",
                "caption_text",
                "likes_count",
                "user_username",
                "user_id",
                "comment_time_text_encoding",
                "user_media_count",
                "user_followed_by_count",
                "user_follows_count",
                "user_followed_by_ids_encoding",
                "user_follows_ids_encoding")
  output = csv.writer(f, delimiter="\t")
  output.writerow(fieldnames)

  api_calls_left = NUMBER_OF_CALLS

  while (api_calls_left > 0):
    print "API Calls Remaining: " + str(api_calls_left)

    #try:
    popular_url  = construct_url(base_url, media_by_popular, authorization_t)
    popular_pull = insta_pull(popular_url)
    api_calls_left -= 1

    popular_data = popular_pull["data"]
    for popular_datum in popular_data:
      image_id            = str(popular_datum["id"])
      image_creation_time = str(popular_datum["created_time"])
      image_comment_count = str(popular_datum["comments"]["count"])
      tag_list            = str(popular_datum["tags"])
      filter_type         = str(popular_datum["filter"])

      location_longitude = NO_INFORMATIONS
      location_latitude  = NO_INFORMATIONS
      location_name      = NO_INFORMATIONS
      if popular_datum["location"] != None:
        loc_keys            = popular_datum["location"].keys()
        location_longitude  = popular_datum["location"]["longitude"] if "longitude" in loc_keys else location_longitude
        location_latitude   = popular_datum["location"]["latitude"] if "latitude" in loc_keys else location_latitude
        location_name       = popular_datum["location"]["name"] if "name" in loc_keys else location_name

      caption_text        = "CAPTION_TEXT"
      try:
        caption_text      = str(popular_datum["caption"]["text"])
      except:
        pass
      likes_count         = str(popular_datum["likes"]["count"])
      user_id             = str(popular_datum["user"]["id"])
      user_username       = user_id + ":USERNAME" 
      try:
        user_username     = str(popular_datum["user"]["username"])
      except:
        pass

      comment_creation_time_text_encode = []
      for comment_data in popular_datum["comments"]["data"]:
        try:
          time_text_combo = str(comment_data["created_time"]) + ":" + str(comment_data["text"])
          comment_creation_time_text_encode.append(time_text_combo)
        except:
          pass
      comment_time_text_encoding = C_TIME_TEXT_ENC.join(comment_creation_time_text_encode)

      user_url  = construct_url(base_url, users_by_id, authorization_t, user_id)
      user_pull = insta_pull(user_url)
      api_calls_left -= 1

      # user general info
      user_data              = user_pull["data"]
      user_media_count       = str(user_data["counts"]["media"])
      user_followed_by_count = str(user_data["counts"]["followed_by"])
      user_follows_count     = str(user_data["counts"]["follows"])

      # user followed-by ids
      user_followed_by_url   = construct_url(base_url, users_followers, authorization_t, user_id)
      user_followed_by_pull  = insta_pull(user_followed_by_url)
      api_calls_left -= 1

      user_followed_data     = user_followed_by_pull["data"]

      follower_ids = []
      for follower in user_followed_data:
        follower_ids.append(follower["id"])
      user_followed_by_ids_encoding = C_TIME_TEXT_ENC.join(follower_ids) # only seems to give limited amount

      # user follows ids
      user_follows_url  = construct_url(base_url, users_follows, authorization_t, user_id)
      user_follows_pull = insta_pull(user_follows_url)
      api_calls_left -= 1

      user_follows_data = user_follows_pull["data"]

      follows_ids = []
      for follow in user_follows_data:
        follows_ids.append(follow["id"])
      user_follows_ids_encoding = C_TIME_TEXT_ENC.join(follows_ids) # only seems to give limited amount

      try:
        output.writerow([image_id,
                         image_creation_time,
                         image_comment_count,
                         tag_list,
                         filter_type,
                         location_longitude,
                         location_latitude,
                         location_name,
                         caption_text,
                         likes_count,
                         user_username,
                         user_id,
                         comment_time_text_encoding,
                         user_media_count,
                         user_followed_by_count,
                         user_follows_count,
                         user_followed_by_ids_encoding,
                         user_follows_ids_encoding])
      except:
        pass
    #except:
      #pass

print "ALERT: Done Writing File."









# GET Popular Media
# base_url = 'https://api.instagram.com/v1/media/popular?access_token='

# GET Media by ID
# base_url = 'https://api.instagram.com/v1/media/{insert Media ID}?access_token='

# GET User by ID
# base_url = 'https://api.instagram.com/v1/users/{insert User ID}?access_token=616157282.1fb234f.92d22888661747c2b364e0e65d96180e'

# GET User's Follows
# base_url = 'https://api.instagram.com/v1/users/{insert User ID}/follows?access_token='

# GET User's Followers
# base_url = 'https://api.instagram.com/v1/users/{insert User ID}/followed-by?access_token='



# return    -> meta, data
# data      -> list of data of individual photos
# data[0]   -> dict of data for individual photo
# firstData -> user_has_liked,
#              attribution,
#              tags,
#              user,
#              comments,
#              filter,
#              images,
#              link,
#              location,
#              created_time,
#              users_in_photo,
#              caption,
#              type,
#              id,
#              likes
#              
#              user_has_liked -> true or false
#              attribution    -> some kind of value
#              tags           -> list of tags
#              user           -> username        -> string name
#                                website         -> string link
#                                profile_picture -> string link
#                                full_name       -> string name
#                                id              -> string num
#              comments       -> count, data, dict of comment + stuff
#              filter         -> string name
#              images         -> different images sizes and links
#              link           -> link to instagram photo
#              location       -> some kind of value
#              created_time   -> some number representation
#              users_in_photo -> list of users
#              caption        -> dict of caption metadata
#              type           -> image or video I suppose
#              id             -> image id?
#              likes          -> dict of likes metadata