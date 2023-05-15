from django.urls import path
from blog.views import (Index,BlogDetailView,RegisterPageView,LoginPageView,GetBlogsAPI,
                        AddBlog, GetBlogDetailsAPI, EditBlog, BlogVersionsView, GetCommentsForBlogAPI)

app_name = 'blog'


urlpatterns = [
    path('',Index.as_view(),name='home'),
    path('blog/<int:blog_id>/',BlogDetailView.as_view(), name='blog-detail'),
    path('register/',RegisterPageView.as_view(), name='registration'),
    path('login/',LoginPageView.as_view(), name='login'),
    path('create_blog/',AddBlog.as_view(), name='add-blog'),
    path('get/comments/<int:blog_id>/',GetCommentsForBlogAPI.as_view(),name='get-comments'),
    path('get/blog/version/<int:blog_id>/',BlogVersionsView.as_view(),name='blog-versions'),
    path('edit_blog/<int:blog_id>/',EditBlog.as_view(),name='edit-blog'),
    path('get/blogs/api/', GetBlogsAPI.as_view(), name='get-blogs'),
    path('get/api/blog_detail/<int:blog_id>/', GetBlogDetailsAPI.as_view(), name='get-blog-detail-view' ),

]
