from Users.models import UserInfo
from Warehouse.models import Cart, CartProduct, WishList
from Products.models import ProductImage, VarietySub, Category
from Main.models import Offers
from Main.serializers import OfferSerializer

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
    cache.delete("cart")
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
                pic = ProductImage.objects.filter(
                    Product=Variety.Product, Primary=True
                ).first()
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
            context["TotalDiscount"] = cr.TotalDiscount
            context["ShippingPrice"] = cr.ShippingPrice
            context["TotalPrice"] = cr.TotalPrice
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
            print("WH:", wh)
            wishes = []
            for item in wh:
                Var = item.Variety.Variety
                PRD = Var.Product
                pic = ProductImage.objects.filter(Product=PRD, Primary=True).first()
                dic = {
                    "Slug": PRD.Slug,
                    "Name": PRD.Name,
                    "Pic": str(pic.Image),
                    "RW": item.RW,
                    "ColorCode": Var.ColorCode,
                    "ColorName": Var.ColorName,
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
    print(context)
    return context


def Categories(request):
    if not "cats" in cache:
        cats = Category.objects.filter(level=0).order_by("order")
        res = []
        for item in cats:
            parent = item
            p = {}
            c_list = []
            p["Parent"] = parent.to_json()
            children = parent.get_children()
            for child in children:
                c = {}
                g_list = []
                c["Parent"] = child.to_json()
                grands = child.get_children()
                for grand in grands:
                    g_list.append(grand.to_json())
                c["Children"] = g_list
                c_list.append(c)
            p["Children"] = c_list
            res.append(p)
        cache.set("cats", res, timeout=60 * 60)
    else:
        res = cache.get("cats")
    return res


def GetOffers():
    if not "offers" in cache:
        Offer = Offers.objects.filter(Active=True)
        Dis = Offer.filter(Type="2")
        Sel = Offer.filter(Type="3")
        POP = Offer.filter(Type="1")
        Discount = []
        Select = []
        POPUP = []
        res = {}
        for item in Dis:
            Discount.append(OfferSerializer(instance=item).data)
        for item in Sel:
            Select.append(OfferSerializer(instance=item).data)
        for item in POP:
            PR = item.Product
            IM = ProductImage.objects.get(Product=PR, Primary=True)

            POPUP.append(
                {
                    "productname": PR.Name,
                    "productlink": f"products/{PR.Slug}",
                    "productimage": str(IM.Image),
                }
            )

        res["Discount"] = Discount
        res["Select"] = Select
        res["POPUP"] = POPUP
        cache.set("offers", res, 60 * 60)
    else:
        res = cache.get("offers")

    return res


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
    get_redis_connection("default")
    Bs = getCart(request)
    QOffers = GetOffers()
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
    context["Offers"] = QOffers
    context["Session"] = getSession(request)
    return context
