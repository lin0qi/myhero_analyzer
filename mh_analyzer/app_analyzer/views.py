from __future__ import annotations
from typing import Any, Dict, List, Tuple
from django.http.request import HttpRequest
from django.shortcuts import render
# Create your views here.
from mhlib.data import Data
from mhlib.more_attr.other_attr import CmpAttr
from mhlib.responselib.mh_resp import MhResp

def test(request : HttpRequest) :
    return render(
        request,
        'test.html')

def analyzer(request : HttpRequest) :
    Data.page_view_add()
    Data.store_ip(request.META['REMOTE_ADDR'])
    mr = MhResp(request)

    if request.method == 'GET':
        return render(
            request,
            'show_form.html',
            {
                'p_dict' : mr.cm.property
            }
            )

    elif request.method == 'POST':
        response =  render(
            request, 
            'show_result.html', 
            mr.render_map
            )
        for k, v in mr.cookie_dict.items():
            response.set_cookie(k, v, mr.cookie_time)
        return response
