# -*- coding: utf-8 -*-

from apiclient.discovery import build
#from apiclient.errors import HttpError
#from oauth2client.tools import argparser # removed by Dongho
import argparse
import csv
import unidecode
from textblob import TextBlob

def percentages(part,whole):
    return 100 * float(part)/float(whole)

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyAaLpDXt-NZUTA4k7imkQe4qEINOOlE8rA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(q=options.q, part="id,snippet", maxResults=options.max_results).execute()
    
    # create a CSV output for video list    
    csvFile = open('kaala.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["title","videoId","viewCount","likeCount","dislikeCount","commentCount","favoriteCount","polarity","subjectivity","positive","neutral","negative"])
    
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            #videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  # Dongho 08/10/16
            videoId = search_result["id"]["videoId"]
             
            video_response = youtube.videos().list(id=videoId,part="statistics").execute()
            
            for video_result in video_response.get("items",[]):
               
                viewCount = video_result["statistics"]["viewCount"]
                if 'likeCount' not in video_result["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_result["statistics"]["likeCount"]
                if 'dislikeCount' not in video_result["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_result["statistics"]["dislikeCount"]
                if 'commentCount' not in video_result["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_result["statistics"]["commentCount"]
                if 'favoriteCount' not in video_result["statistics"]:
                    favoriteCount = 0
                else:
                    favoriteCount = video_result["statistics"]["favoriteCount"]
                    
                video_comments = youtube.commentThreads().list(part="snippet",videoId=video_result["id"],textFormat="plainText").execute()

                polarity = 0.00
                subjectivity = 0.00
                Total = 0.00
                for item in video_comments.get("items",[]):
                    comment = item["snippet"]["topLevelComment"]
                    text = comment["snippet"]["textDisplay"]
                    text_blob = TextBlob(text)
                    pol = text_blob.polarity
                    sub = text_blob.subjectivity
        
                    polarity+=pol
                    subjectivity+=sub
                    Total+=1
                    
            polarity=polarity/Total
            subjectivity=subjectivity/Total
            
            if(polarity == 0.00):
                 neutral=1
                 positive=0
                 negative=0
    
            if(polarity < 0.00):
                negative=1
                positive=0
                neutral=0
     
            if(polarity > 0.00):
                positive=1
                neutral=0
                negative=0
            csvWriter.writerow([title,videoId,viewCount,likeCount,dislikeCount,commentCount,favoriteCount,polarity,subjectivity,positive,neutral,negative])
    csvFile.close()
    
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search on YouTube')
    parser.add_argument("--q", help="Search term", default="Google")
    parser.add_argument("--max-results", help="Max results", default=10)
    args = parser.parse_args()
    #try:
    youtube_search(args)
    #except HttpError, e:
    #    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
