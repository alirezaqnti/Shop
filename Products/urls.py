from django.urls import path
from . import views

urlpatterns = [
    # path('',views.Products,name='Product_home'),
    path("<slug:slug>", views.ProductPage.as_view(), name="ProductPage"),
    path("results/", views.SearchView.as_view(), name="SearchView"),
    path("getvariety/<str:RPV>", views.GetVariety.as_view(), name="GetVariety"),
    path(
        "getproductstopreview/", views.GetProductsToPreview.as_view(), name="GetProductsToPreview"
    ),
    path("getsearchresult/", views.GetSearchResult.as_view(), name="GetSearchResult"),
    path("getproduct-varieties/", views.GetProductVarieties.as_view(), name="GetProductVarieties"),
    path("gettopsellpreview/", views.GetTopSellToPreview.as_view(), name="GetTopSellToPreview"),
    path(
        "getsimilartopreview/<slug:slug>",
        views.GetSimilarToPreview.as_view(),
        name="GetSimilarToPreview",
    ),
    path("getsearchengine/", views.SearchEngine.as_view(), name="SearchEngine"),
    path("getcategories/", views.CategoryMasterAPI.as_view(), name="GetCategories"),
    path("getfilters/", views.GetFilters.as_view(), name="GetFilters"),
    path("notify/", views.SetProductNotify.as_view(), name="SetProductNotify"),
    path("remove-from-compare/", views.RemoveFromCompare.as_view(), name="RemoveFromCompare"),
    path("add-to-compare/", views.AddToCompare.as_view(), name="AddToCompare"),
    path("compare-check/", views.CompareCheckView.as_view(), name="CompareCheck"),
    path("compare/", views.Compare.as_view(), name="Compare"),
]
