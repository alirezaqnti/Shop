# region import
from django.core.cache import cache
from django.core import serializers
from django.core.paginator import Paginator
from django.views.generic import TemplateView, FormView
from django.db.models import Q
from Main.permissions import IsUserLoggedIn
from Main.context_processors import getActiveUser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from Products.serializers import (
    ProductToPreviewSerializer,
    ProductSerializer,
    FiltersSerializer,
    VarietySerializer,
    CategorySerializer,
)
from django.http import JsonResponse
from Products.models import (
    Category,
    Product,
    ProductImage,
    ProductToPreview,
    Variety,
    ProductComment,
    ProductTag,
    ProductStat,
    Filters,
    TopSellToPreview,
    VarietySub,
    CommentTip,
    QuantityNotify,
    NotifyNumber,
)
import json
from Analytic.views import VisitPage
from django.shortcuts import redirect, render

# endregion

# region ProductPage


class ProductPage(TemplateView):
    template_name = "Main/Product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs["slug"]
        Def = VarietySub.objects.get(RPVS=slug)
        print("DEF:", Def)
        PRD = (
            Product.objects.filter(Slug=Def.Variety.Product.Slug)
            .prefetch_related(
                "image_prd",
                "tech_prd",
                "variety_product",
                "tag_prd",
            )
            .first()
        )
        print("PRD:", PRD)
        vars = PRD.variety_product.filter(Active=True)
        try:
            var = Def.Variety
            VarietySubs = VarietySub.objects.filter(Variety=var)
        except:
            PRD = (
                Product.objects.filter(Slug=slug)
                .prefetch_related(
                    "image_prd",
                    "tech_prd",
                    "variety_product",
                    "tag_prd",
                )
                .first()
            )
            vars = PRD.variety_product.filter(Active=True)
            var = vars.first()
            VarietySubs = VarietySub.objects.filter(Variety=var)
            Def = VarietySubs.exclude(Quantity=0).first()
            if Def == None:
                Def = VarietySubs.first()

        D = VisitPage(self.request)
        D = D["0"]
        if D > 1:
            # TODO GOOGLE ANALYTICS API SERVICE
            PRD.Visit += 1
            PRD.save()
        # try:
        # except:
        #     # TODO 404page
        #     pass

        Pics = PRD.image_prd.all().order_by("Primary")
        Cms = (
            ProductComment.objects.filter(Product=PRD)
            .prefetch_related("comment_tip")
            .order_by("Created_at")
        )
        Tags = PRD.tag_prd.all()
        context["SelectedVar"] = var.RPV
        context["Vars"] = vars
        context["Var"] = var
        context["Subs"] = VarietySubs
        context["Def"] = Def
        context["Pictures"] = Pics
        context["Comments"] = Cms
        context["Tags"] = Tags
        context["PRD"] = PRD
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        User = getActiveUser(request)
        Pr = context["Product"]
        stars = request.POST.get("stars", None)
        STR = request.POST.getlist("STR", None)
        Weak = request.POST.getlist("Weak", None)
        text = request.POST.get("text", None)
        Comment = ProductComment()
        Comment.Product = Pr
        Comment.User = User
        Comment.Text = text
        Comment.Rate = stars
        Comment.save()
        for item in Weak:
            tip = CommentTip()
            tip.Comment = Comment
            tip.Type = False
            tip.Value = item
            tip.save()
        for item in STR:
            tip = CommentTip()
            tip.Comment = Comment
            tip.Type = True
            tip.Value = item
            tip.save()
        return redirect("ProductPage", kwargs["slug"])
        # return reverse_lazy("ProductPage", kwargs={"slug": kwargs["slug"]})


class GetVariety(RetrieveAPIView):
    lookup_field = "RPV"
    queryset = Variety.objects.all()
    serializer_class = VarietySerializer


# endregion

# region GetProductsToPreview


class GetProductsToPreview(ListAPIView):
    serializer_class = ProductToPreviewSerializer
    queryset = ProductToPreview.objects.filter(Active=True)


# endregion

# region GetTopSellToPreview


class GetTopSellToPreview(ListAPIView):
    serializer_class = ProductToPreviewSerializer
    queryset = TopSellToPreview.objects.filter(Active=True)


# endregion

# region GetSimilarToPreview


class GetSimilarToPreview(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        pr = self.kwargs["slug"]
        Pr = Product.objects.get(Slug=pr)
        res = Product.objects.filter(
            Category__in=Category.objects.get(pk=Pr.Category.pk).get_descendants(include_self=True)
        ).exclude(pk=Pr.pk)
        print(pr)
        return res


# endregion

# region GetProductVarieties


class GetProductVarieties(APIView):
    def post(self, request, *args, **kwargs):
        txt = request.data["Txt"]
        Pr = Product.objects.filter(Q(Name__contains=txt) | Q(RP=txt)).prefetch_related(
            "variety_product"
        )
        Si = VarietySub.objects.filter(RPVS=txt)
        res = []
        if Si.count() != 0:
            res.append(Si.first().toJson())
        for item in Pr:
            for Var in item.variety_product.all():
                VarietySubs = VarietySub.objects.filter(Variety=Var, Active=True).exclude(
                    Quantity=0
                )
                for size in VarietySubs:
                    res.append(size.toJson())
        print(res)
        return Response({"Products": res})


# endregion

# region GetSearchResult


class GetSearchResult(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        kwargs = self.request.GET
        res = Product.objects.filter(Status=ProductStat.valid).order_by("-Created_at_g")
        try:
            txt = kwargs["txt"]
            res = self.TxtFilter(res, txt)
        except:
            pass
        cat = kwargs.get("cat")
        if cat != None:
            res = self.categoryFilter(res, cat)

            try:
                mat = kwargs["mat"]
                res = self.MaterialFilter(res, mat)
            except:
                pass
            try:
                type = kwargs["type"]
                res = self.typeFilter(res, type)
            except:
                pass
            try:
                Usage = kwargs["usage"]
                res = self.UsageFilter(res, Usage)
            except:
                pass
            try:
                heels = kwargs["heels"]
                res = self.heelsFilter(res, heels)
            except:
                pass
            try:
                ties = kwargs["shoelace"]
                res = self.tiesFilter(res, ties)
            except:
                pass
            try:
                hands = kwargs["strap"]
                res = self.handsFilter(res, hands)
            except:
                pass
            try:
                forms = kwargs["forms"]
                res = self.formsFilter(res, forms)
            except:
                pass

        try:
            color = kwargs["color"]
            res = self.ColorFilter(res, color)
        except:
            pass
        try:
            size = kwargs["size"]
            res = self.SizeFilter(res, size)
        except:
            pass
        try:
            brand = kwargs["brand"]
            res = self.brandFilter(res, brand)
        except:
            pass
        try:
            tag = kwargs["tag"]
            res = self.tagsearchFilter(res, tag)
        except:
            pass
        try:
            discount = kwargs["discount"]
            if discount == "true":
                res = self.discountFilter(res)
        except:
            pass
        try:
            exist = kwargs["exist"]
            if exist == "true":
                res = self.existancFilter(res)
        except:
            pass
        try:
            price = kwargs["price"]
            price = price.split(",")
            min = price[0]
            max = price[1]
            res = self.priceFilter(res, min, max)
        except:
            pass
        return res

    # region filters

    # region priceFilter
    # returns a list of products in a price range
    # product will be chosen from a given list as well as minimum & maximum price

    def priceFilter(self, list, min, max):
        arr = []
        for i in list:
            for item in VarietySub.objects.filter(Variety__Product=i):
                if item.FinalPrice >= int(min) and item.FinalPrice <= int(max):
                    if not i in arr:
                        arr.append(i)
        return arr

    # endregion

    # region brandFilter
    # returns a list of products that are made from a brand
    # product will be chosen from a given list as well as brand name

    def brandFilter(self, list, word):
        arr = []
        word = word.split(",")
        for item in list:
            if item.Brand.Name == word:
                arr.append(item)
        return arr

    # endregion

    # region keysearchFilter
    # returns a list of products that contains a given string in their name
    # product will be chosen from a given list as well as string

    def TxtFilter(self, list, name):
        arr = []
        for item in list:
            if item.Name.__contains__(name):
                arr.append(item)
        return arr

    # endregion

    # region tagsearchFilter
    # returns a list of products that have a certain tag in their tags list
    # product will be chosen from a given list as well as tag name

    def tagsearchFilter(self, list, tags):
        arr = []
        for item in list:
            tgs = ProductTag.objects.filter(Product=item)
            for tg in tgs:
                for tag in tags:
                    if tag == tg.Title:
                        if not item in arr:
                            arr.append(item)
        return arr

    # endregion

    # region discountFilter
    # returns a list of products that have discount
    # product will be chosen from a given list

    def discountFilter(self, list):
        arr = []
        for item in list:
            if item.Discount > 0:
                if not item in arr:
                    arr.append(item)
            else:
                vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
                for vr in vrs:
                    sizes = VarietySub.objects.filter(Variety=vr).order_by("Size")
                    for size in sizes:
                        if size.Discount > 0:
                            if not item in arr:
                                arr.append(item)
        return arr

    # endregion

    # region existancFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def existancFilter(self, list):
        arr = []
        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                sizes = VarietySub.objects.filter(Variety=vr).order_by("Size")
                for size in sizes:
                    if size.Quantity > 0:
                        if not item in arr:
                            arr.append(item)
        return arr

    # endregion

    # region ColorFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def ColorFilter(self, list, colors):
        arr = []
        colors = colors.split(",")
        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                for cl in colors:
                    if cl == vr.ColorCode:
                        if not item in arr:
                            arr.append(item)
        return arr

    # endregion

    # region SizeFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def SizeFilter(self, list, si):
        arr = []
        si = si.split(",")
        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                sizes = VarietySub.objects.filter(Variety=vr).order_by("Size")
                for size in sizes:
                    if size.Size in si:
                        if not item in arr:
                            arr.append(item)
        return arr

    # endregion

    # region typeFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def typeFilter(self, list, types):
        arr = []
        types = types.split(",")
        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                try:
                    if vr.Type.Name in types:
                        if not item in arr:
                            arr.append(item)
                except:
                    pass
        return arr

    # endregion

    # region UsageFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def UsageFilter(self, list, Usages):
        arr = []
        Usages = Usages.split(",")

        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                try:
                    if vr.Usage.Name in Usages:
                        if not item in arr:
                            arr.append(item)
                except:
                    pass
        return arr

    # endregion

    # region heelsFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def heelsFilter(self, list, heels):
        heels = heels.split(",")
        arr = []
        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                try:
                    if vr.Heel.Name in heels:
                        if not item in arr:
                            arr.append(item)
                except:
                    pass
        return arr

    # endregion

    # region tiesFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def tiesFilter(self, list, ties):
        arr = []
        ties = ties.split(",")

        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                try:
                    if vr.Tie.Name in ties:
                        if not item in arr:
                            arr.append(item)
                except:
                    pass
        return arr

    # endregion

    # region handsFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def handsFilter(self, list, hands):
        hands = hands.split(",")
        arr = []
        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                try:
                    if vr.Handle.Name in hands:
                        if not item in arr:
                            arr.append(item)
                except:
                    pass
        return arr

    # endregion

    # region formsFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def formsFilter(self, list, forms):
        forms = forms.split(",")
        arr = []
        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                try:
                    if vr.Form.Name in forms:
                        if not item in arr:
                            arr.append(item)
                except:
                    pass
        return arr

    # endregion

    # region MaterialFilter
    # returns a list of products that are available to purchase
    # product will be chosen from a given list

    def MaterialFilter(self, list, mat):
        mat = mat.split(",")
        arr = []
        for item in list:
            vrs = Variety.objects.filter(Product=item, Active=True, Status=ProductStat.valid)
            for vr in vrs:
                try:
                    if vr.Material.Name in mat:
                        if not item in arr:
                            arr.append(item)
                except:
                    pass
        return arr

    # endregion

    # region categoryFilter
    # returns a list of products that are in a specific Category
    # product will be chosen from a given list as well as Category

    def categoryFilter(self, list, cat):
        Pr = Product.objects.filter(
            Category__in=Category.objects.get(pk=cat).get_descendants(include_self=True)
        )
        return Pr

    # endregion

    # endregion


# endregion

# region SearchView


class SearchView(TemplateView):
    template_name = "Main/Search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = self.request.GET.get("cat")
        si = self.request.GET.get("size")
        txt = self.request.GET.get("txt")
        c = self.request.GET.get("color")
        b = self.request.GET.get("brand")
        m = self.request.GET.get("mat")
        ty = self.request.GET.get("type")
        u = self.request.GET.get("usage")
        h = self.request.GET.get("heels")
        S = self.request.GET.get("shoelace")
        h = self.request.GET.get("strap")
        f = self.request.GET.get("forms")
        t = self.request.GET.get("tag")
        d = self.request.GET.get("discount")
        e = self.request.GET.get("exist")
        price = self.request.GET.get("price")

        Filter = []
        # region
        if d != None:
            if d == "true":
                d = "تخفیف دار"
            Filter.append({"key": "تخفیف", "value": d, "type": "discount"})

        if e != None:
            if e == "true":
                e = "موحود"
            Filter.append({"key": "موجود بودن", "value": e, "type": "exist"})

        if price != None:
            Filter.append({"key": " قیمت", "value": price, "type": "price"})

        if si != None:
            Filter.append({"key": "سایز", "value": si, "type": "size"})

        if txt != None:
            Filter.append({"key": "متن", "value": txt, "type": "txt"})

        if c != None:
            Filter.append({"key": "رنگ", "value": c, "type": "color"})

        if b != None:
            Filter.append({"key": "برند", "value": b, "type": "brand"})

        if m != None:
            Filter.append({"key": "جنس", "value": m, "type": "mat"})

        if ty != None:
            Filter.append({"key": "نوع", "value": ty, "type": "type"})

        if u != None:
            Filter.append({"key": "مورد استفاده", "value ": u, "type": "usage"})

        if h != None:
            Filter.append({"key": "پاشنه", "value": h, "type": "heels"})

        if S != None:
            Filter.append({"key": "بند", "value": S, "type": "shoelace"})

        if h != None:
            Filter.append({"key": "دستگیره", "value": h, "type": "strap"})

        if f != None:
            Filter.append({"key": "فرم", "value": f, "type": "forms"})

        if t != None:
            Filter.append({"key": "برچسب", "value": t, "type": "tag"})
        context["Filter"] = Filter
        # endregion
        if cat != None:
            Cats = Category.objects.get(Active=True, pk=cat).get_descendants(include_self=True)
            Filter.append({"key": "دسته بندی", "value": Cats[0].Name, "type": "cat"})
            Color = []
            Brand = []
            Material = []
            Type = []
            Usage = []
            Heels = []
            Shoelace = []
            Strap = []
            Form = []
            for c in Cats:
                Fil = Filters.objects.filter(Category=c)
                for item in Fil:
                    if item.Type == 0:
                        if not item in Color:
                            Color.append(item)
                    elif item.Type == 1:
                        if not item in Brand:
                            Brand.append(item)
                    elif item.Type == 2:
                        if not item in Material:
                            Material.append(item)
                    elif item.Type == 3:
                        if not item in Type:
                            Type.append(item)
                    elif item.Type == 4:
                        if not item in Usage:
                            Usage.append(item)
                    elif item.Type == 5:
                        if not item in Heels:
                            Heels.append(item)
                    elif item.Type == 6:
                        if not item in Shoelace:
                            Shoelace.append(item)
                    elif item.Type == 7:
                        if not item in Strap:
                            Strap.append(item)
                    elif item.Type == 8:
                        if not item in Form:
                            Form.append(item)
            context["Color"] = Color
            context["Brand"] = Brand
            context["Material"] = Material
            context["Type"] = Type
            context["Usage"] = Usage
            context["Heels"] = Heels
            context["Shoelace"] = Shoelace
            context["Strap"] = Strap
            context["Form"] = Form

        return context


# endregion

# region getSubCat
# returns a dictionary of categories that have the same given parent id


class GetCategories(APIView):
    def post(self, request, *args, **kwargs):
        cat = Category.objects.filter(parent=None)
        cats = []
        for item in cat:
            cats.append(
                {
                    "id": item.id,
                    "name": item.Name,
                }
            )
        stat = 200
        cats.reverse()
        context = {"cats": cats, "stat": stat}
        return Response(context)


# endregion

# region CategoryMasterAPI


class CategoryMasterAPI(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        cat = Category.objects.filter(parent=None)
        return cat


# endregion

# region SearchEngine


class SearchEngine(APIView):
    def post(self, request, *args, **kwargs):
        txt = request.data["Txt"]
        if txt != "":
            res = []
            pr = Product.objects.filter(Name__contains=txt)
            if pr.count() != 0:
                for item in pr:
                    pic = ProductImage.objects.get(Product=item, Primary=True)
                    Name = f'<a href="/products/{item.Slug}"><img src="/media/{pic.Image}" width="50" height="50" /><b>{item.Name}</b></a>'
                    res.append(
                        {
                            "Name": Name,
                        }
                    )
            cat = Category.objects.filter(Name__contains=txt)
            if cat.count() != 0:
                for item in cat:
                    c = item.get_ancestors(ascending=False, include_self=False)
                    print(c)
                    Anc = ""
                    for i, a in enumerate(c):
                        if i == (c.count() - 1):
                            Anc += f"<small>{a.Name}<small>"
                        else:
                            Anc += f"<small>{a.Name}،<small>"
                    Name = f'<a href="/products/results/?cat={item.pk}"><b><i class="flaticon-square"></i> {item.Name}</b><small>/در دسته بندی </small><br>{Anc}</a>'
                    res.append(
                        {
                            "Name": Name,
                        }
                    )

        return Response(res)


# endregion

# region SetProductNotify


class SetProductNotify(APIView):
    def post(self, request, *args, **kwargs):
        report = ""
        stat = 500
        User = getActiveUser(request)
        RPVS = request.data["RPVS"]

        if User == "":
            report = "برای ادامه وارد حساب کاربری خود شوید"
            stat = 300
        else:
            Si = VarietySub.objects.get(RPVS=RPVS)
            try:
                QN = QuantityNotify.objects.get(Product=Si)
            except:
                QN = QuantityNotify()
                QN.Product = Si
                QN.save()
            try:
                NN = NotifyNumber.objects.get(User=User)
                if NN.Active == True:
                    report = "درخواست شما قبلا ثبت شده است"
                    stat = 201
                else:
                    NN.Active = True
                    NN.save()
                    stat = 200
                    report = "درخواست شما ثبت شد"
            except:
                NN = NotifyNumber()
                NN.QN = QN
                NN.User = User
                stat = 200
                report = "درخواست شما ثبت شد"

        context = {"report": report, "stat": stat}
        return Response(context)


# endregion

# region Compare

# region AddToCompare


class AddToCompare(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data["RPVS"]
        Si = VarietySub.objects.get(RPVS=data)
        try:
            print("DATA:", data)
        except:
            return Response({"stat": 500, "report": "اطلاعات ارسالی صحیح نیست"})

        if "compareList" in cache:
            CL = cache.get("compareList")
            print("compareList", CL)
        else:
            CL = {}
        if len(CL) >= 4:
            return Response(
                {"stat": 500, "report": "حد مجاز اضافه کردن محصول 4 آیتم است", "list": CL}
            )

        try:
            CL[data]
            return Response({"stat": 201, "report": "قبلا وارد شده است", "list": CL})
        except:
            CL[data] = Si.toJson()
            cache.set("compareList", CL, (60 * 20))
            return Response({"stat": 200, "report": "با موفقیت اضافه شد", "list": CL})


# endregion


# region CompareCheck


class CompareCheckView(APIView):
    def post(self, request, *args, **kwargs):
        stat = CompareCheck()
        return Response({"stat": stat})


def CompareCheck():
    if "compareList" in cache:
        CL = cache.get("compareList")
        print("CL:", len(CL))
        if len(CL) > 1:
            return 200
        else:
            return 201
    else:
        return 201


# endregion


# region Compare


class Compare(TemplateView):
    template_name = "Main/Compare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        CL = cache.get("compareList")
        print(CL)
        context["List"] = sorted(CL.items())
        return context

    def get(self, request, *args, **kwargs):
        stat = CompareCheck()
        print("STAT:", self.request.META["HTTP_REFERER"])
        if stat == 201:
            if "products/compare/" in self.request.META["HTTP_REFERER"]:
                url = "/products/results/"
            else:
                url = self.request.META["HTTP_REFERER"]
            return redirect(url)
        else:
            return render(request, self.template_name, self.get_context_data())


# endregion


# region RemoveFromCompare


class RemoveFromCompare(APIView):
    def post(self, request, *args, **kwargs):
        stat = CompareCheck()
        if stat == 200:
            CL = cache.get("compareList")
            data = request.data["RPVS"]
            try:
                del CL[data]
                cache.set("compareList", CL, (60 * 30))
                return Response({"stat": 200})
            except:
                return Response({"stat": 500, "report": "اطلاعات ارسالی صحیح نیست"})
        else:
            return Response({"stat": 500, "report": "اطلاعات ارسالی صحیح نیست"})


# endregion

# endregion

# region GetFilters


class GetFilters(APIView):
    def post(self, request, *args, **kwargs):
        PK = request.data["PK"]
        Fils = Filters.objects.filter(Category_id=PK).prefetch_related("val_filter")
        res = []
        for fil in Fils:
            vals = fil.val_filter.all()
            for val in vals:
                res.append({"PK": val.pk, "Title": f"<b>{fil.Name}</b> / {val.Title}"})
        return Response({"Data": res})


# endregion
