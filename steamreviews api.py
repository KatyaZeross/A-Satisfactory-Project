from functools import reduce
import steamreviews
import pandas as pd
import numpy as np
import json

app_id = 526870

request_params = dict()


# request_params['start_offset'] = 0
request_params['language'] = 'english'
request_params['review_type'] = 'all'
request_params['purchase_type'] = 'all'
request_params['filter'] = 'recent'

review_dict, query_count = steamreviews.download_reviews_for_app_id(app_id, chosen_request_params=request_params)

with open('data.json', 'w') as fp:
    json.dump(review_dict, fp)
    data = json.load(fp)




