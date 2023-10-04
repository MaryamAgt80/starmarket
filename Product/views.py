from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.generic import ListView
from .models import Product, DetailProduct, Comment, DetailPooshak, Categorize_Products, ImageProduct, BrandProduct
from django.shortcuts import render
from django.apps import apps
from django.core.paginator import Paginator
from Order.models import DetilOrder, Order, Like
from django.db.models import Q
from django.db.models import Exists, OuterRef
from django.utils.decorators import method_decorator
from Site_App.models import Slider



@login_required(login_url='login')
def LikeProduct(request: HttpRequest):
    likesproduct = Like.objects.filter(user_id=request.user.id).order_by('-id').product
    return render(request, 'pages/shop.html', {'Product': likesproduct})


@method_decorator(login_required(login_url='login'), name='dispatch')
class LikeProducts(ListView):
    model = Product
    context_object_name = 'Products'
    template_name = 'pages/shop.html'
    paginate_by = 9
    ordering = '-id'

    def get_queryset(self):
        context = super(LikeProducts, self).get_queryset()
        likes = Like.objects.filter(user_id=self.request.user.id)
        ps = context.filter(Exists(likes.filter(product_id=OuterRef('id'))))

        try:
            range_price = self.request.GET.get('range_price')
            min, max = range_price.split(',')
            min = int(min)
            max = int(max)
            max = max - max % 1000
            min = min - min % 1000
            ps = ps.filter(Q(price__gte=min) & Q(price__lte=max))
            self.template_name = 'pages/replace_shop.html'
        except:
            pass
        return ps

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        likes = Like.objects.filter(user_id=self.request.user.id)
        ps = Product.objects.filter(Exists(likes.filter(product_id=OuterRef('id'))))
        if ps.count() > 1:
            data['min_range'] = min_value = ps.order_by('price')[0].price
            data['max_range'] = max_value = ps.order_by('-price')[0].price

        return data


def IndexPage(request):
    sliders = Slider.objects.filter(in_active=True)
    productsBuy = Product.objects.order_by('-count_buy')
    productsOffer = Product.objects.order_by('-offer_price')
    pagebuy = 1
    try:
        pagebuy = request.GET.get('pagebuy')
    except:
        pagebuy = 1
    pageoff = 1
    try:
        pageoff = request.GET.get('pageoff')
    except:
        pageoff = 1

    paginatorBuy = Paginator(productsBuy, per_page=4)
    paginatorOffer = Paginator(productsOffer, per_page=4)
    page_objBuy = paginatorBuy.get_page(pagebuy)
    page_objOff = paginatorOffer.get_page(pageoff)
    return render(request, 'pages/index.html',
                  {'productsBuy': page_objBuy, 'productsOffer': page_objOff,'Slider':sliders})


class ShowAllProduct(ListView):
    model = Product
    template_name = 'pages/shop.html'
    context_object_name = 'Products'
    ordering = ['-id']
    paginate_by = 9

    def get_queryset(self):
        context = super(ShowAllProduct, self).get_queryset()
        try:
            range_price = self.request.GET.get('range_price')
            min, max = range_price.split(',')
            min = int(min)
            max = int(max)
            max = max - max % 1000
            min = min - min % 1000
            context = context.filter(Q(price__gte=min) & Q(price__lte=max))
            self.template_name = 'pages/replace_shop.html'
        except:
            pass
        return context

    def get_context_data(self):
        context = super(ShowAllProduct, self).get_context_data()
        products = Product.objects.all()
        if products.count() > 1:
            context['min_range'] = products.order_by('price')[0].price
            context['max_range'] = products.order_by('-price')[0].price
        return context


class checklike(View):
    def get(self, request: HttpRequest, id):
        product = Product.objects.filter(id=id).first()
        like: Like = Like.objects.filter(product_id=product.id, user_id=request.user.id).first()

        if like is not None:
            product.count_like -= 1
            product.save()
            like.delete()


        else:
            like: Like = Like.objects.create(product_id=product.id, user_id=request.user.id)
            product.count_like += 1
            product.save()
            like.save()

        return JsonResponse({})


class DetailProductClass(View):
    def get(self, request: HttpRequest, id):

        product: Product = Product.objects.filter(id=id).first()
        if product is not None:

            min_price = 0.8 * product.price
            max_price = 1.2 * product.price
            similar_products = Product.objects.filter(
                (Q(price__gte=min_price) & Q(price__lte=max_price) & ~Q(id=product.id)),
                name_class=product.name_class)
            n = similar_products.count()
            if n >= 9:
                similar_products = similar_products[:9]
            else:
                min_price = 0.6 * product.price
                max_price = 1.4 * product.price
                similar_products = Product.objects.filter(
                    (Q(price__gte=min_price) & Q(price__lte=max_price) & ~Q(id=product.id)),
                    name_class=product.name_class)
                n = similar_products.count()
                if n >= 9:
                    similar_products = similar_products[:10]

            like_status = False
            paginator3 = Paginator(similar_products, per_page=3)
            pagesimilar = 1
            try:
                pagesimilar = request.GET.get('pagesimilar')
            except:
                pagesimilar = 1
            page_similr = paginator3.get_page(pagesimilar)
            if request.user.is_authenticated:
                like_product: Like = Like.objects.filter(user_id=request.user.id, product_id=id).first()
                if like_product:
                    like_status = True
            comments = Comment.objects.filter(product_id=id)
            detail_product = product.ProductMain.all()
            detail_product = list(detail_product)
            image_product = ImageProduct.objects.filter(product_image_id=product.id)
            detail_product = detail_product + list(image_product)
            paginator = Paginator(detail_product, per_page=3)
            page = 1
            try:
                page = request.GET.get('page')
            except:
                page = 1

            page_obj = paginator.get_page(page)

            Nclass = apps.get_model('Product', product.name_class)
            ProductDetail: Nclass = Nclass.objects.filter(product_id=id).first()
            fields = Nclass._meta.fields
            mylist = []
            for item in fields:
                field_object = Nclass._meta.get_field(item.name)
                field_value = field_object.value_from_object(ProductDetail)
                mylist.append([field_value, item.verbose_name])
            mylist = mylist[2:]
            # websites=Site_Another.objects.all()

            return render(request, 'pages/product-details.html',
                          {'Product': ProductDetail, 'websites':'','Comments': comments, 'page_obj': page_obj, 'fields': mylist,
                           'like_status': like_status, 'page_similr': page_similr,'name_product':product.name})
        return render(request, 'pages/404.html')

    def post(self, request: HttpRequest, id):
        message = ''
        state = 'error'
        product: Product = Product.objects.filter(id=id).first()
        if request.user.is_authenticated:
            OrederUser, status = Order.objects.get_or_create(user_id=request.user.id, status=0)
            OrederUser.save()
            if request.POST.get('Count') and request.POST.get('DetailID'):
                count = int(request.POST.get('Count'))
                DetailID = int(request.POST.get('DetailID'))
                if product.name_class == 'Pooshak':
                    if request.POST.get('PooshakID'):
                        PooshakID = int(request.POST.get('PooshakID'))
                        order_detail = OrederUser.ordermain.filter(detail_product_id=DetailID,
                                                                   detail_pooshak=PooshakID).first()
                        if order_detail is not None:
                            order_detail.count += count
                            if order_detail.count <= order_detail.detail_pooshak.count:
                                order_detail.save()
                                message = 'محصول مورد نظر شما در سبد خرید افزوده شد'
                                state = 'success'
                            else:
                                message = 'محصول مورد نظر شما به تعداد خواسته شده موجود نیست'
                        else:
                            product_detail: DetailProduct = DetailProduct.objects.filter(id=DetailID).first()
                            detail_pooshak: DetailPooshak = DetailPooshak.objects.filter(id=PooshakID).first()
                            if product_detail is not None and detail_pooshak is not None:
                                if count < detail_pooshak.count:
                                    order_detail: DetilOrder = DetilOrder.objects.create(detail_pooshak_id=PooshakID,
                                                                                         detail_product_id=DetailID,
                                                                                         count=count,
                                                                                         order_main_id=OrederUser.id)
                                    order_detail.save()
                                    message = 'محصول شما به سبد خرید افزوده شد'
                                    state = 'success'
                                else:
                                    message = 'عدم موجودی انبار'
                            else:
                                message = 'خطا در عملیات'
                    else:
                        message = 'تمام فیلد ها مققدار دهی نشده است!'
                else:
                    order_detail = OrederUser.ordermain.filter(detail_product_id=DetailID).first()
                    if order_detail is not None:
                        order_detail.count += count
                        if order_detail.count <= order_detail.detail_product.count:
                            order_detail.save()
                            message = 'محصول مورد نظر شما در سبد خرید افزوده شد'
                            state = 'success'
                        else:
                            message = 'محصول مورد نظر شما به تعداد خواسته شده موجود نیست'
                    else:
                        product_detail: DetailProduct = DetailProduct.objects.filter(id=DetailID).first()
                        if product_detail is not None:
                            if count < product_detail.count:
                                order_detail: DetilOrder = DetilOrder.objects.create(detail_product_id=DetailID,
                                                                                     count=count,
                                                                                     order_main_id=OrederUser.id)
                                order_detail.save()
                                message = 'محصول شما به سبد خرید افزوده شد'
                                state = 'success'
                            else:
                                message = 'عدم موجودی انبار'
                        else:
                            message = 'خطا در عملیات'
            else:
                message = 'تمام فیلد ها مقدر دهی نشده است!'
        else:
            message = 'برای افزودن به سبد خرید وارد سایت شوید'

        return JsonResponse({'message': message, 'state': state})


class ShowBrand(ListView):
    model = Product
    template_name = 'pages/shop.html'
    context_object_name = 'Products'
    paginate_by = 9

    def get_queryset(self):
        context = super(ShowBrand, self).get_queryset()
        ps = context.filter(brand_p__url_field=self.kwargs['brand'])
        try:
            range_price = self.request.GET.get('range_price')
            min, max = range_price.split(',')
            min = int(min)
            max = int(max)
            max = max - max % 1000
            min = min - min % 1000
            ps = ps.filter(Q(price__gte=min) & Q(price__lte=max))
            self.template_name = 'pages/replace_shop.html'
        except:
            pass
        return ps

    def get_context_data(self):
        context = super(ShowBrand, self).get_context_data()
        ps = Product.objects.filter(brand_p__url_field=self.kwargs['brand'])
        if ps.count() > 1:
            context['min_range'] = min_value = ps.order_by('price')[0].price
            context['max_range'] = max_value = ps.order_by('-price')[0].price
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class NewComment(View):
    def post(self, request: HttpRequest):
        status = False
        if request.POST.get('id') and request.POST.get('Fname') and request.POST.get('Lname') and request.POST.get(
                'TextComment'):
            id = int(request.POST.get('id'))
            fname = request.POST.get('Fname')
            lname = request.POST.get('Lname')
            comment_text = request.POST.get('TextComment')
            product: Product = Product.objects.filter(id=id).first()
            if product is not None:
                comment = Comment.objects.create(user_id=request.user.id, product_id=id, massege=comment_text,
                                                 name=fname, lname=lname)
                status = True
                comment.save()
        return JsonResponse({'status': status})


def render_categorize(request):
    categorize = Categorize_Products.objects.filter(is_active=True, parent=None)
    return render(request, 'pages/render_categorize.html', {'Categorize': categorize})


class ShowProductCategorize(ListView):
    model = Product
    context_object_name = 'Products'
    template_name = 'pages/shop.html'
    paginate_by = 2

    def get_queryset(self):
        query = super(ShowProductCategorize, self).get_queryset()
        cate = self.kwargs.get("cate")
        categorize: Categorize_Products = Categorize_Products.objects.filter(cate_name=cate).first()
        list_cate = []
        if categorize:
            list_cate.append(categorize.cate_name)
            for item in categorize.subset.all():
                list_cate.append(item.cate_name)
            query = query.filter(categorize__in=list_cate)
        try:
            range_price = self.request.GET.get('range_price')
            min, max = range_price.split(',')
            min = int(min)
            max = int(max)
            max = max - max % 1000
            min = min - min % 1000
            query = query.filter(Q(price__gte=min) & Q(price__lte=max))
            self.template_name = 'pages/replace_shop.html'
        except:
            pass
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cate = self.kwargs["cate"]
        categorize: Categorize_Products = Categorize_Products.objects.filter(cate_name=cate).first()
        list_cate = []
        if categorize:
            list_cate.append(categorize.cate_name)
            for item in categorize.subset.all():
                list_cate.append(item.cate_name)
            query = Product.objects.filter(categorize__in=list_cate)
        if query.count() > 1:
            context['min_range'] = min_value = query.order_by('price')[0].price
            context['max_range'] = max_value = query.order_by('-price')[0].price

        return context


def render_cate_base(request):
    categorize = Categorize_Products.objects.filter(is_active=True, parent=None)
    return render(request, 'pages/render_categorize_base.html', {'Categorize': categorize})


def render_cate_index(request):
    categorize = Categorize_Products.objects.filter(is_active=True, parent=None)
    return render(request, 'pages/render_categorize_index.html', {'Categorize': categorize})


class ShowSearchProducts(ListView):
    model = Product
    template_name = 'pages/shop.html'
    ordering = '-id'
    context_object_name = 'Products'
    paginate_by = 9

    def get_queryset(self):
        context = super(ShowSearchProducts, self).get_queryset()
        pk = self.kwargs['search']
        context = context.filter(name__contains=pk)
        try:
            range_price = self.request.GET.get('range_price')
            print(range_price)
            min, max = range_price.split(',')
            min = int(min)
            max = int(max)
            max = max - max % 1000
            min = min - min % 1000
            context = context.filter(Q(price__gte=min) & Q(price__lte=max))
            self.template_name = 'pages/replace_shop.html'
        except:
            pass
        return context

    def get_context_data(self):
        context = super(ShowSearchProducts, self).get_context_data()
        pk = self.kwargs['search']
        ps = Product.objects.filter(name__contains=pk)
        if ps.count() > 1:
            context['min_range'] = min_value = ps.order_by('price')[0].price
            context['max_range'] = max_value = ps.order_by('-price')[0].price
        return context


def render_brands(request:HttpRequest):
    Brands = BrandProduct.objects.all()
    return render(request, 'pages/brands.html', {'Brands': Brands})


def render_brands_pages(request):
    Brands = BrandProduct.objects.all()
    Brands_list = Paginator(Brands, 4)
    page = 1
    try:
        page = int(request.GET.get('br_page'))
    except:
        page = 1
    Brands_page = Brands_list.get_page(page)
    return render(request, 'pages/render_brands.html', {'Brands': Brands_page})

    return render(request, 'pages/brands.html', {'Brands': Brands})
