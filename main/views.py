
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.forms import CreatePostForm, UpdatePostForm
from main.models import Category, Post

#
# def index_page(request):
#     categories = Category.objects.all()
#     return render(request, 'main/index.html', {'categories': categories})


#Not Actual
#TODO : Переписать эту вьюшку при помощи классов
#TODO: Список постов по категориям
#TODO: Переходы по страницам
#TODO :Регистрация ,  активация ,  логин , логаут
#TODO: HTML- письмо



#Actual
#TODO Добавить посты
#TODO: Создание и редактировани и удаление постов
#TODO Смена и восстановление пароля
#TODO: Филтрация , поиск ,  сортировка
#TODO:  Пагинация
#TODO: Переиспользование шаблонов
#TODO: Проверка прав
#TODO: Избранное
#TODO: Дизайн


class CreateNewPostView(CreateView):
    queryset = Post.objects.all()
    template_name = 'main/create_post.html'
    form_class = CreatePostForm

class EditPostView(UpdateView):
    queryset = Post.objects.all()
    template_name = 'main/edit_post.html'
    form_class = UpdatePostForm

class DeletePostView(DeleteView):
    queryset = Post.objects.all()
    template_name = 'main/delete_post.html'




class IndexPageView(ListView):
    queryset = Category.objects.all()
    template_name = 'main/index.html'
    context_object_name = 'categories'


class PostsListView(ListView):
    queryset = Post.objects.all()
    template_name = 'main/posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category')
        return queryset.filter(category_id=category_id)


class PostDetailsView(DetailView):
    queryset = Post.objects.all()
    template_name = 'main/post_details.html'







