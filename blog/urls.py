from django.urls import path
from django.contrib.auth.decorators import login_required
from blog.views import (Index,BlogDetailView,RegisterPageView,LoginPageView,GetBlogsAPI,
                        AddBlog, GetBlogDetailsAPI, EditBlog, BlogVersionsView, GetCommentsForBlogAPI)


app_name = 'blog'


urlpatterns = [
    path('',login_required(Index.as_view(), login_url="http://127.0.0.1:8000/login/"),name='home'),
    path('blog/<int:blog_id>/',login_required(BlogDetailView.as_view(), login_url="http://127.0.0.1:8000/login/"), name='blog-detail'),
    path('register/',RegisterPageView.as_view(), name='registration'),
    path('login/',LoginPageView.as_view(), name='login'),
    path('create_blog/',login_required(AddBlog.as_view(),login_url="http://127.0.0.1:8000/login/"), name='add-blog'),
    path('get/comments/<int:blog_id>/',GetCommentsForBlogAPI.as_view(),name='get-comments'),
    path('get/blog/version/<int:blog_id>/',login_required(BlogVersionsView.as_view(), login_url="http://127.0.0.1:8000/login/"),name='blog-versions'),
    path('edit_blog/<int:blog_id>/',login_required(EditBlog.as_view(), login_url="http://127.0.0.1:8000/login/"),name='edit-blog'),
    path('get/blogs/api/', GetBlogsAPI.as_view(), name='get-blogs'),
    path('get/api/blog_detail/<int:blog_id>/', GetBlogDetailsAPI.as_view(), name='get-blog-detail-view' ),

]
