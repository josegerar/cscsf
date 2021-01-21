from django.shortcuts import render

def mainIndex(request):
    data = {
        "urls": [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            }
        ],
        "usertitle": "Representante Técnico"
    }
    return render(request, 'rp/homerp.html', data)