import datetime

from Main.context_processors import getActiveUser
from .models import Visit

# region DateDiffrence
# returns day diffrence between now
# and a given date


def DateDiffrence(Date):
    Now = datetime.datetime.now()
    Date = Date.replace(tzinfo=None)
    print(Date)
    print(Now)
    return (Now - Date).days


# endregion


def VisitPage(request):
    IP = request.session["user_ip"]
    User = getActiveUser(request)
    URL = request.build_absolute_uri()
    Vi = Visit.objects.filter(IP=IP, URL=URL)
    D = 2
    if Vi.count() != 0:
        obj = Vi.last()
        D = DateDiffrence(obj.Created_AT)
    if D > 1:
        V = Visit()
        V.IP = IP
        if User != "":
            V.User = User
        V.URL = URL
        V.save()

    return {"0": D}
