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
from Products.models import *
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
        try:
            Def = VarietySub.objects.get(RPVS=slug)
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
            vars = PRD.variety_product.filter(Active=True)
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
        CM = []
        [CM.append(x.toJson()) for x in Cms]
        Tags = PRD.tag_prd.all()
        context["SelectedVar"] = var.RPV
        context["Vars"] = vars
        context["Var"] = var
        context["Subs"] = VarietySubs
        context["Def"] = Def
        context["Pictures"] = Pics
        context["Comments"] = CM
        context["Tags"] = Tags
        context["PRD"] = PRD
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        User = getActiveUser(request)
        Pr = context["PRD"]
        stars = request.POST.get("stars", None)
        print("stars:", stars)
        STR = request.POST.getlist("STR", None)
        print("STR:", STR)
        Weak = request.POST.getlist("Weak", None)
        print("Weak:", Weak)
        text = request.POST.get("text", None)
        print("text:", text)
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
            Category__in=Category.objects.get(pk=Pr.Category.pk).get_descendants(
                include_self=True
            )
        ).exclude(pk=Pr.pk)
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
                VarietySubs = VarietySub.objects.filter(
                    Variety=Var, Active=True
                ).exclude(Quantity=0)
                for size in VarietySubs:
                    res.append(size.toJson())
        return Response({"Products": res})


# endregion

# region GetSearchResult


class GetSearchResult(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        kwargs = self.request.GET
        res = (
            Product.objects.filter(Status=ProductStat.valid)
            .prefetch_related("image_prd", "variety_product")
            .order_by("-Created_at_g")
        )
        try:
            txt = kwargs["متن"]
            res = self.TxtFilter(res, txt)
        except:
            pass
        exc = [
            "size",
            "brand",
            "tag",
            "discount",
            "exist",
            "price",
            "limit",
            "دسته بندی",
        ]
        cat = kwargs.get("دسته بندی")
        if cat != None:
            res = self.categoryFilter(res, cat)
            keys = []
            Fils = []
            for i in kwargs:
                keys.append(i)
            for i in keys:
                if not i in exc:
                    Fils.append([i, kwargs[i]])
            print("Fils:", Fils)
            arr = []
            for item in Fils:
                F = Filters.objects.filter(
                    Name=item[0], Category__pk=cat
                ).prefetch_related("val_filter")
                for fi in F:
                    vals = fi.val_filter.filter(Title=item[1])
                    for v in vals:
                        for P in res:
                            try:
                                ProductFilter.objects.get(Filter=v, Product=P)
                                arr.append(P)
                            except:
                                pass
                res = arr
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
        up = name.upper()
        low = name.lower()
        for item in list:
            if item.Name.__contains__(up) or item.Name.__contains__(low):
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
                vrs = Variety.objects.filter(
                    Product=item, Active=True, Status=ProductStat.valid
                )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
            vrs = Variety.objects.filter(
                Product=item, Active=True, Status=ProductStat.valid
            )
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
        cat = self.request.GET.get("دسته بندی")
        # region
        keys = []
        Filter = []
        kw = self.request.GET
        for i in kw:
            keys.append(i)
        for i in keys:
            if i != "limit" and i != "دسته بندی":
                key = i
                value = kw[i]
                if i == "size":
                    key = "سایز"
                elif i == "brand":
                    key = "برند"
                elif i == "tag":
                    key = "برچسب"
                elif i == "discount":
                    key = "تخفیف دار"
                    value = "بله"
                elif i == "exist":
                    key = "فقط موجود"
                    value = "بله"
                elif i == "price":
                    key = "قیمت"
                Filter.append({"key": key, "value": value})
        context["Filter"] = Filter
        # endregion
        Dyn = []
        if cat != None:
            Cats = Category.objects.get(Active=True, pk=cat).get_descendants(
                include_self=True
            )
            Filter.append({"key": "دسته بندی", "value": Cats[0].Name, "type": "cat"})
            Fils = Filters.objects.filter(Category__pk=int(cat)).prefetch_related(
                "val_filter"
            )
            for item in Fils:
                F = {"Title": item.Name}
                F_V = []
                vals = item.val_filter.all()
                for v in vals:
                    F_V.append(v.Title)
                F["Vals"] = F_V
                Dyn.append(F)
        context["Dynamics"] = Dyn
        return context


# endregion

# region getSubCat
# returns a dictionary of categories that have the same given parent id


class GetCategories(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data["id"]
        cat = Category.objects.get(pk=int(id)).get_descendants(include_self=False)
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
        res = {}
        Products = []
        Cats = []
        if txt != "":
            up = txt.upper()
            low = txt.lower()
            pr = Product.objects.filter(
                Q(Name__contains=up) | Q(Name__contains=low)
            ).prefetch_related("image_prd")
            if pr.count() != 0:
                for item in pr:
                    pic = item.image_prd.filter(Primary=True).first()
                    Products.append(
                        {
                            "URL": f"/products/{item.Slug}",
                            "Name": item.Name,
                            "Image": str(pic.Image),
                        }
                    )
            cat = Category.objects.filter(Q(Name__contains=up) | Q(Name__contains=low))
            if cat.count() != 0:
                for item in cat:
                    c = item.get_ancestors(ascending=False, include_self=False)
                    Anc = ""
                    for i, a in enumerate(c):
                        if i == (c.count() - 1):
                            Anc += a.Name
                        else:
                            Anc += a.Name
                    Cats.append(
                        {
                            "URL": f"/products/results/?cat={item.pk}",
                            "Name": item.Name,
                            "Anc": Anc,
                        }
                    )
        res["Products"] = Products
        res["Cats"] = Cats
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
            print(Si)
        except:
            return Response({"stat": 500, "report": "اطلاعات ارسالی صحیح نیست"})

        if "compareList" in cache:
            CL = cache.get("compareList")
        else:
            CL = {}
        if len(CL) >= 4:
            return Response(
                {
                    "stat": 500,
                    "report": "حد مجاز اضافه کردن محصول 4 آیتم است",
                    "list": CL,
                }
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
        context["List"] = sorted(CL.items())
        return context

    def get(self, request, *args, **kwargs):
        stat = CompareCheck()
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
