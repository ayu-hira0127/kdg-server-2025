from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Product, Category, Favorite, Cart, PurchaseHistory, ProductImage
from .forms import ProductForm, ProductImageForm, SearchForm  # ProductImageFormのインポートを追加
import logging

logger = logging.getLogger(__name__)

class ExhibitedListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'exhibited_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

class FavoriteProductView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True

        return JsonResponse({'is_favorited': is_favorited})

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'favorite_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('product')

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        products = paginator.get_page(page)

        if self.request.user.is_authenticated:
            favorite_products = set(Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True))
            for product in products:
                product.is_favorited = product.id in favorite_products
        else:
            for product in products:
                product.is_favorited = False

        context['products'] = products
        return context
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object if self.object else None
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)  # Product インスタンスを保存（まだDBには保存しない）
        instance.user = self.request.user  # ログインユーザーをセット
        instance.save()  # DBに保存

        logger.debug(f"Uploaded files: {self.request.FILES}")
        print("request.FILES:", self.request.FILES)  

        image_form = ProductImageForm(self.request.POST, self.request.FILES)
        if image_form.is_valid():
            images = self.request.FILES.getlist('images')  # アップロードされた画像を取得
            for image in images:
                ProductImage.objects.create(product=instance, image=image)
        else:
            logger.error(f"Image upload failed: {image_form.errors}")  # エラーログを出力

        return redirect(self.success_url)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(user=self.request.user, product=product).exists()
        else:
            context['is_favorited'] = False

        context['images'] = product.images.all()
        
        return context

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        logger.debug(f"Uploaded files: {self.request.FILES}")  
        print("request.FILES:", self.request.FILES)  

        # 削除リクエストがあった画像を削除
        delete_images = self.request.POST.getlist('delete_image')
        if delete_images:
            ProductImage.objects.filter(id__in=delete_images).delete()

        # 新しくアップロードされた画像を処理
        image_form = ProductImageForm(self.request.POST, self.request.FILES)
        if image_form.is_valid():
            for image in self.request.FILES.getlist('images'):
                ProductImage.objects.create(product=self.object, image=image)
        else:
            logger.error(f"Image upload failed: {image_form.errors}")  # エラーログを出力

        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('search_app:exhibited_list')

class SearchView(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET or None)
        results = Product.objects.all()
        if form.is_valid():
            query = form.cleaned_data['query']
            if query:
                results = results.filter(name__icontains(query))
        category_name = request.GET.get('category')
        if category_name:
            try:
                category = Category.objects.get(name=category_name)
                results = results.filter(category_id=category.id)
            except Category.DoesNotExist:
                results = results.none()
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
            results = results.filter(price__gte(min_price))
        if max_price:
            results = results.filter(price__lte(max_price))
        sort_by = request.GET.get('sort', 'name')
        if sort_by == 'price_asc':
            results = results.order_by('price')
        elif sort_by == 'price_desc':
            results = results.order_by('-price')
        else:
            results = results.order_by('name')
        paginator = Paginator(results, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'form': form, 'page_obj': page_obj})

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart.quantity += 1
            cart.save()
        return redirect('search_app:view_cart')

class ViewCartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'add_cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related('product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        context['total_price'] = total_price
        return context

class CartRemoveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, pk=kwargs['pk'], user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('search_app:view_cart')

class PurchaseView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        for item in cart_items:
            PurchaseHistory.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.product.price * item.quantity
            )
        cart_items.delete()
        return redirect('search_app:purchase_history')

class PurchaseHistoryView(LoginRequiredMixin, ListView):
    model = PurchaseHistory
    template_name = 'purchase_history.html'
    context_object_name = 'history_items'

    def get_queryset(self):
        return PurchaseHistory.objects.filter(user=self.request.user).select_related('product')

# エンドポイントを定義
product_create = ProductCreateView.as_view()
product_detail = ProductDetailView.as_view()
product_update = ProductUpdateView.as_view()
product_delete = ProductDeleteView.as_view()
product_list = ProductListView.as_view()
search = SearchView.as_view()
favorite_product = FavoriteProductView.as_view()
favorite_list = FavoriteListView.as_view()
exhibited_list = ExhibitedListView.as_view()
add_to_cart = AddToCartView.as_view()
view_cart = ViewCartView.as_view()
purchase = PurchaseView.as_view()
purchase_history = PurchaseHistoryView.as_view()
remove_from_cart = CartRemoveView.as_view()