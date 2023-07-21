from typing import List, Dict, Union, Tuple
from requests import get
from urllib.parse import parse_qs, urlparse, urlencode
import math

def from_dot_string(string: str, Obj: any):
    if string is None or len(string) == 0:
      return None
    
    res = {}
    strings = string.split(".")
    if len(strings) > 1:
      for _string in strings:
        if Obj.get(_string):
          return from_dot_string(string.replace("{}.".format(_string), ""), Obj.get(_string))
    else:
      k = strings[0]
      if Obj.get(k):
        res = Obj.get(k)

    return res

def remapped(mapresult: Dict, data: any):
  if len(mapresult) == 0:
    return data
  
  dct = dict()
  for key in mapresult:
    tpl_val = mapresult[key]
    value = from_dot_string(tpl_val, data)
    if value is None: continue
    dct[key] = value
  
  return dct

def non_paginate_data(url) -> Tuple[List[Dict], Union[str, None], Union[Exception, None]]:
  res = get(url)
  if res.ok is False:
    return ([], "failed", Exception(res.reason))
  try:
    content = res.json()
  except:
    return ([], "failed", Exception("invalid json response"))
  return (content, None, None)

def paginate_data(baseurl: str, params: Dict[str, List[str]], map_result: Dict = {"total": "total", "items": "items"}, page_map: Dict = {"page": "page", "limit": "limit"}):
  
  if params.get("page") is None:
    def_limit = 10
    for p in page_map:
      key = page_map[p]
      val = def_limit
      if p == "page":
        val = 1
      params[key] = val

  link = "{}?{}".format(baseurl, urlencode(params, doseq=True))
  data, msg, error = non_paginate_data(link)

  if msg is not None: return ([], msg, error)
  
  res = remapped(mapresult=map_result, data=data)
  total = res.get("total")
  items = res.get("items")

  query = remapped(mapresult=page_map, data=params)
  page = int(query.get("page"))
  limit = int(query.get("limit"))

  paging = page + 1
  fin = math.ceil(total/limit)
  finished = fin <= page

  if not finished:
    for p in page_map:
      key = page_map[p]
      val = limit
      if p == "page":
        val = paging
      params[key] = val

    get_items, res, exc = paginate_data(baseurl=baseurl, params=params, map_result=map_result, page_map=page_map)
    if res is not None:
      return ([], res, exc)
    
    return (get_items + items, None, None)
  else:
    return (items, None, None)

def download_excel_rawdata(
  url: str, 
  data_mapper: Dict = {},
  page_mapper: Dict = {},
  path_download: str = None,
) -> Tuple[List[Dict], Union[str, None], Union[Exception, None]]:
  
  if len(data_mapper) == 0:
    data, res, exc = non_paginate_data(url)
  else:
    baseUrl = url.split("?")[0]
    parsedUrl = urlparse(url)
    params = parse_qs(parsedUrl.query)
    data, res, exc = paginate_data(baseurl=baseUrl, params=params, map_result=data_mapper, page_map=page_mapper)

  return (data, res, exc)