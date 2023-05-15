from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from django.views.generic import View

from blog.models import BlogPost,BlogVersions,Comment
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import json
from datetime import datetime


# Create your views here.

#Blogs List API
class GetBlogsAPI(generics.GenericAPIView, LoginRequiredMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    #GET Blogs API
    def get(self,request):
        try:
            blog_posts = list(BlogPost.objects.select_related('author').all().values('title', 'description', 'author__username', 'blog_id'))
            response_data = json.dumps(blog_posts)

            return Response(
                status=status.HTTP_200_OK,
                data={'response_data': response_data},
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={'Error': f"{e}"},
                    content_type='application/json'
                )
        
    #POST Blog API
    def post(self, request):
        post_data = request.POST
        if post_data:
           author = User.objects.get(id=request.user.id)
           title = post_data.get("title", None)
           description = post_data.get("description", None)
           body_text = post_data.get("body_text", None)
           
           try:
               blog_obj = BlogPost(title=title, description=description, body_text=body_text, author=author)
               blog_obj.save()

               return Response(
                status=status.HTTP_200_OK,
                data={'response_data': "blog posted succesfully"},
                content_type='application/json'
            )
           except Exception as e:
               return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={'Error': f"{e}"},
                    content_type='application/json'
                )
               

        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"Error:": "post data not provided"},
                content_type='application/json')

#Blog Details API
class GetBlogDetailsAPI(generics.GenericAPIView, LoginRequiredMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    #Get Blog Details API
    def get(self, request, blog_id):
        blog_posts = list(BlogPost.objects.select_related('author').filter(blog_id=blog_id).values('title', 'description', 'author__username', 'blog_id', 'body_text'))[0]
        response_data = json.dumps(blog_posts)

        return Response(
            status=status.HTTP_200_OK,
            data={'response_data': response_data},
            content_type='application/json'
        )
    
    #Edit Blog Details API
    def put(self, request, blog_id):

        post_data = request.POST
        if post_data:
           title = post_data.get("title", None)
           description = post_data.get("description", None)
           body_text = post_data.get("body_text", None)

           blog_obj = BlogPost.objects.get(blog_id=blog_id)

           #Inserting Data into version Table

           previous_title = blog_obj.title
           previous_description = blog_obj.description
           previous_body_text = blog_obj.body_text

           blog_previous_version_obj = BlogVersions.objects.filter(blog_id=blog_id).order_by('-version').first()

           present_version_no = 1

           if blog_previous_version_obj:
               present_version_no = blog_previous_version_obj.version+1
           
           blog_version_obj = BlogVersions(title=previous_title, description=previous_description, body_text=previous_body_text, version = present_version_no, blog_id=blog_obj)
           blog_version_obj.save()

           #Editing the Blog

           blog_obj.updated_date = datetime.now()
           blog_obj.title = title
           blog_obj.description = description
           blog_obj.body_text = body_text
           blog_obj.save(update_fields=['update_date', 'title','description', 'body_text'])

        return Response(
            status=status.HTTP_200_OK,
            data={'response_data': "updated succesfully"},
            content_type='application/json'
        )
    
    #DELETE Blog API
    def delete(self, request, blog_id):
            blog_obj = BlogPost.objects.get(blog_id=blog_id)
            blog_obj.delete()

            return Response(
            status=status.HTTP_200_OK,
            data={'response_data': "Deleted succesfully"},
            content_type='application/json'
            )

#Comments List API
class GetCommentsForBlogAPI(generics.GenericAPIView, LoginRequiredMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    #Get comments list API
    def get(self, request, blog_id):
        comments = list(Comment.objects.select_related('author').filter(post_id=blog_id).order_by('-creation_date').values('author__username','comment_text'))
        response_data = json.dumps(comments)

        return Response(
            status=status.HTTP_200_OK,
            data={'response_data': response_data},
            content_type='application/json'
        )
    
    #Create a Comment API
    def post(self, request, blog_id):
        post_data = request.POST
        if post_data:
           author = User.objects.get(id=request.user.id)
           comment_text = post_data.get('comment_text',None)
           author_email = author.email
           comment_obj = Comment(author=author,comment_text=comment_text, author_email=author_email, post_id=BlogPost.objects.get(blog_id=blog_id))
           comment_obj.save()
           return Response(
            status=status.HTTP_200_OK,
            data={'response_data': "Comment Posted Succesfully"},
            content_type='application/json'
        )

#Blogs List View
class Index(View,LoginRequiredMixin):
    def get(self,request):
        print(request.user.id)
        return render(request,"blog/blogs_list.html")

#Blog Details View
class BlogDetailView(View, LoginRequiredMixin):
    def get(self,request, blog_id):
        author = BlogPost.objects.get(blog_id=blog_id).author
        check_author_user_same = author==request.user
        return render(request,"blog/blog-detail.html", context={"blog_id":blog_id, "check_author_user_same":check_author_user_same})

#Add Blog View
class AddBlog(View, LoginRequiredMixin):
        def get(self,request):
            return render(request,"blog/createblog.html")

#Edit Blog View    
class EditBlog(View, LoginRequiredMixin):
        def get(self,request,blog_id):
            return render(request,"blog/blog_edit.html", context={"blog_id":blog_id})

#Blog Versions View
class BlogVersionsView(View, LoginRequiredMixin):
    def get(self, request, blog_id):
        blog_versions = list(BlogVersions.objects.filter(blog_id=blog_id).order_by('-version').values())
        my_list_str = [
        {'blog_version_id': item["blog_version_id"], 'blog_id_id': item["blog_id_id"], 'version': item["version"], 'title': item["title"], 'description': item["description"], 'body_text': item["body_text"], 'modified_date': item["modified_date"].isoformat()}
        for item in blog_versions]
        return render(request, "blog/versions.html",context={"blog_id":blog_id, "blog_versions":my_list_str})
    
#Register New User View
class RegisterPageView(View):
    def get(self,request):

        return render(request,"blog/register.html")

#Login User View
class LoginPageView(View):
    def get(self,request):

        return render(request,"blog/login.html")