import json
import time
import requests
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import quote_plus
from requests.adapters import HTTPAdapter
import datetime
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import pandas as pd

from youtube_api.youtube_api_utils import (
    _load_response,
    parse_yt_datetime,
    _chunker,
)
import youtube_api.parsers as P


__all__ = ['YoutubeDataApi', 'YouTubeDataAPI']

class YouTubeDataAPI:
    def __init__(
        self, key, api_version='3', verify_api_key=True, verbose=False, timeout=20
    ):
        self.key = key
        self.api_version = int(api_version)
        self.verbose = verbose
        self._timeout = timeout

        # check API Key
        if not self.key:
            raise ValueError('No API key used to initate the class.')
        if verify_api_key and not self.verify_key():
            raise ValueError('The API Key is invalid')

        # creates a requests sessions for API calls.
        self._create_session()


    def verify_key(self):
        http_endpoint = ("https://www.googleapis.com/youtube/v{}/playlists"
                         "?part=id&id=UC_x5XG1OV2P6uZZ5FSM9Ttw&"
                         "key={}&maxResults=2".format(self.api_version, self.key))
        response = requests.get(http_endpoint)
        try:
            response.raise_for_status()
            return True
        except:
            return False


    def _create_session(self, max_retries=2, backoff_factor=.5, status_forcelist=[500, 502, 503, 504], **kwargs):
        session = requests.Session()
        retries = Retry(total=max_retries,
                        backoff_factor=backoff_factor,
                        status_forcelist=status_forcelist,
                        **kwargs)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session = session

    def _http_request(self, http_endpoint, timeout_in_n_seconds=False):
        if self.verbose:
            # Print the Http req and replace the API key with a placeholder
            print(http_endpoint.replace(self.key, '{API_KEY_PLACEHOLDER}'))
        response = self.session.get(http_endpoint, timeout=self._timeout)
        response_json = _load_response(response)
        return response_json

    def get_video_metadata_gen(self, video_id, parser=P.parse_video_metadata,
                               part=['statistics','snippet'],  **kwargs):
        part = ','.join(part)
        parser=parser if parser else P.raw_json
        if isinstance(video_id, list) or isinstance(video_id, pd.Series):
            for chunk in _chunker(video_id, 50):
                id_input = ','.join(chunk)
                http_endpoint = ("https://www.googleapis.com/youtube/v{}/videos"
                                 "?part={}"
                                 "&id={}&key={}&maxResults=50".format(
                                    self.api_version, part, id_input, self.key))
                for k,v in kwargs.items():
                    http_endpoint += '&{}={}'.format(k, v)
                response_json = self._http_request(http_endpoint)
                if response_json.get('items'):
                    for item in response_json['items']:
                        yield parser(item)
                else:
                    yield parser(None)
        else:
            raise Expection('This function only takes iterables!')


    def get_video_metadata(self, video_id, parser=P.parse_video_metadata, part=['statistics','snippet'],  **kwargs):
        video_metadata = []
        parser=parser if parser else P.raw_json
        if isinstance(video_id, str):
            part = ','.join(part)
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/videos"
                             "?part={}"
                             "&id={}&key={}&maxResults=2".format(self.api_version,
                                                                 part, video_id,
                                                                 self.key))
            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)
            response_json = self._http_request(http_endpoint)
            if response_json.get('items'):
                video_metadata = parser(response_json['items'][0])

        elif isinstance(video_id, list) or isinstance(video_id, pd.Series):
            for video_meta in self.get_video_metadata_gen(video_id,
                                                          parser=parser,
                                                          part=part,
                                                          **kwargs):
                video_metadata.append(video_meta)
        else:
            raise TypeError("Could not process the type entered!")

        return video_metadata

    def search(self, q=None, channel_id=None,
               max_results=5, order_by="relevance", next_page_token=None,
               published_after=datetime.datetime.timestamp(datetime.datetime(2000,1,1)),
               published_before=datetime.datetime.timestamp(datetime.datetime(3000,1,1)),
               location=None, location_radius='1km', region_code=None,
               safe_search=None, relevance_language=None, event_type=None,
               topic_id=None, video_duration=None, search_type="video",
               parser=P.parse_rec_video_metadata, part=['snippet'],
               **kwargs):
        if search_type not in ["video", "channel", "playlist"]:
            raise Exception("The value you have entered for `type` is not valid!")

        parser=parser if parser else P.raw_json
        part = ','.join(part)
        videos = []
        while True:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/search?"
                             "part={}&type={}&maxResults=50"
                             "&order={}&key={}".format(
                                 self.api_version, part, search_type, order_by, self.key))
            if q:
                if isinstance(q, list):
                    q = '|'.join(q)
                http_endpoint += "&q={}".format(q)

            if published_after:
                if not isinstance(published_after, float) and not isinstance(published_after, datetime.date):
                    raise Exception("published_after must be a timestamp, not a {}".format(type(published_after)))
                
                if isinstance(published_after, float):
                    published_after = datetime.datetime.utcfromtimestamp(published_after)
                _published_after = datetime.datetime.strftime(published_after, "%Y-%m-%dT%H:%M:%SZ")
                http_endpoint += "&publishedAfter={}".format(_published_after)

            if published_before:
                if not isinstance(published_before, float) and not isinstance(published_before, datetime.date):
                    raise Exception("published_before must be a timestamp, not a {}".format(type(published_before)))
                    
                if isinstance(published_before, float):
                    published_before = datetime.datetime.utcfromtimestamp(published_before)
                _published_before = datetime.datetime.strftime(published_before, "%Y-%m-%dT%H:%M:%SZ")
                http_endpoint += "&publishedBefore={}".format(_published_before)

            if channel_id:
                http_endpoint += "&channelId={}".format(channel_id)

            if location:
                if isinstance(location, tuple):
                    location = quote_plus(str(location).strip('()').replace(' ', ''))
                http_endpoint += "&location={}&locationRadius={}".format(location,
                                                                         location_radius)
            if region_code:
                http_endpoint += "&regionCode={}".format(region_code)

            if safe_search:
                if not safe_search in ['moderate', 'strict', 'none']:
                    raise "Not proper safe_search."
                http_endpoint += '&safeSearch={}'.format(safe_search)

            if relevance_language:
                http_endpoint += '&relevanceLanguage={}'.format(relevance_language)

            if event_type:
                if not event_type in ['completed', 'live', 'upcoming']:
                    raise "Not proper event_type!"
                http_endpoint += '&eventType={}'.format(event_type)

            if topic_id:
                http_endpoint += '&topicId={}'.format(topic_id)

            if video_duration:
                if not video_duration in ['short', 'long', 'medium', 'any']:
                    raise "Not proper video_duration"
                http_endpoint += '&videoDuration={}'.format(video_duration)

            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)

            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response_json = self._http_request(http_endpoint)
            if response_json.get('items'):
                for item in response_json.get('items'):
                    videos.append(parser(item))
                if max_results:
                    if len(videos) >= max_results:
                        videos = videos[:max_results]
                        break
                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                    time.sleep(.1)
                else:
                    break
            else:
                break

        return videos

class YoutubeDataApi(YouTubeDataAPI):
    def __init__(self, key, **kwargs):
        super().__init__(key, **kwargs)

def openJson(path):
    with open(path)as f:
        data = json.load(f, strict=False)
        return data

key_path = "apikey.json"
key = openJson(key_path)["key"]
key_word_path = "keywords.json"
key_word_ls = openJson(key_word_path)["keywords"]
yt = YouTubeDataAPI(key)

d = {}
for s in key_word_ls:
    ls = []
    screachs = yt.search(s,max_results=10,parser=None,relevance_language='en')
    for i in screachs:
        ls.append(i['id']['videoId'])

    req = yt.get_video_metadata(ls,part = ["statistics","snippet"])
    list_of_video = []
    
    for i in req:
        list_of_video.append({'title':i['video_title'],'view':i['video_view_count']})

    d[s] = list_of_video
f = open('youtubeRequest.json','w')
json.dump(d,f,indent=1)
f.close()

