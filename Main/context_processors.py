from Users.models import UserInfo
from Warehouse.models import Cart, CartProduct, WishList
from Products.models import ProductImage, VarietySub, Category

# from Main.models import QuickOffer
import operator
from core.settings import MEDIA_URL
from django_redis import get_redis_connection
from django.core.cache import cache

CACHE_TTL = 60 * 5


def getSession(request):
    context = {}
    user = getActiveUser(request)
    if user != "":
        name = user.Name
        ProfileImage = str(user.ProfileImage)
        Session = {
            "name": name,
            "ProfileImage": ProfileImage,
        }
        context["Session"] = Session
    return context


def getActiveUser(request, *args, **kwargs):
    request = request
    try:
        id = request.session["User_id"]
        user = UserInfo.objects.get(slug=id)
    except:
        user = ""
    return user


def getCart(request, *args, **kwargs):
    if not "cart" in cache:
        context = {}
        try:
            user = getActiveUser(request)
            cr = (
                Cart.objects.filter(User=user, status=0, Active=True)
                .prefetch_related("cartproduct_cart")
                .first()
            )
            co = cr.cartproduct_cart.filter(Active=True)
            data = []
            for item in co:
                Variety = item.Variety.Variety
                pic = ProductImage.objects.filter(Product=Variety.Product, Primary=True).first()
                dic = {
                    "Name": Variety.Product.Name,
                    "Pic": str(pic.Image),
                    "Max": item.Variety.Quantity,
                    "slug": item.slug,
                    "Fee": item.Fee,
                    "Quantity": item.Quantity,
                    "Amount": item.Amount,
                    "discount": item.discount,
                    "Offless": item.Offless,
                    "RCP": item.RCP,
                    "Size": item.Variety.Size,
                    "RPVS": item.Variety.RPVS,
                }
                if Variety.ColorCode:
                    dic["ColorCode"] = Variety.ColorCode
                    dic["ColorName"] = Variety.ColorName
                data.append(dic)
            context["count"] = co.count()
            context["Pros"] = data
            context["RC"] = cr.RC
            context["Amount"] = cr.Amount
            context["TotalPrice"] = cr.TotalPrice
            context["TotalDiscount"] = cr.TotalDiscount
            context["ShippingPrice"] = cr.ShippingPrice
        except:
            context["Pros"] = []
            context["RC"] = 0
            context["count"] = 0
            context["Amount"] = 0
            context["TotalPrice"] = 0
            context["TotalDiscount"] = 0
            context["ShippingPrice"] = 0
        try:
            wh = WishList.objects.filter(User=user)
            wishes = []
            for item in wh:
                pic = ProductImage.objects.filter(
                    Product=item.Variety.Variety.Product, Primary=True
                ).first()
                dic = {
                    "Name": item.Variety.Variety.Product.Name,
                    "Pic": str(pic.Image),
                    "RW": item.RW,
                    "Color": item.Variety.Variety.ColorCode,
                    "Size": item.Variety.Size,
                }
                wishes.append(dic)
            context["WishPros"] = wishes
            context["WishCount"] = wh.count()

        except:
            context["WishCount"] = 0
            context["WishPros"] = []
        cache.set("cart", context, timeout=CACHE_TTL)
    else:
        context = cache.get("cart")
    return context


def Categories(request):
    cats = Category.objects.filter(level=0).order_by("order")
    # if not "cats" in cache:
    #     subcats = []
    #     for item in cats:
    #         for cat in Category.objects.filter(parent_id=item.id):
    #             subcats.append(cat)
    #             for sub in Category.objects.filter(parent_id=cat.id):
    #                 subcats.append(sub)
    #         subcats.append(item)
    #     cats = sorted(subcats, key=operator.attrgetter("order"))
    #     res = [item.to_json() for item in cats]
    #     cache.set("cats", res, timeout=CACHE_TTL)
    # else:
    #     res = cache.get("cats")
    return cats.get_descendants(include_self=True)


# # region getIP
# # save user ip address in sessions


def getIP(request):
    try:
        request.session["user_ip"]
    except:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        request.session["user_ip"] = ip
    return


# # endregion


def Con(request):
    getIP(request)
    #     get_redis_connection("default")
    Bs = getCart(request)
    #     QOffers = QuickOffer.objects.filter(Active=True)[:2]
    context = {}
    context["Cat"] = Categories(request)
    context["MEDIA_URL"] = MEDIA_URL
    context["count"] = Bs["count"]
    context["Pros"] = Bs["Pros"]
    context["Amount"] = Bs["Amount"]
    context["TotalPrice"] = Bs["TotalPrice"]
    context["TotalDiscount"] = Bs["TotalDiscount"]
    context["ShippingPrice"] = Bs["ShippingPrice"]
    context["WishPros"] = Bs["WishPros"]
    context["WishCount"] = Bs["WishCount"]
    #     context["QOffer"] = QOffers
    context["Session"] = getSession(request)
    return context
