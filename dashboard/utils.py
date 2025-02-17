from activity.models import ItemOperation, Comment
from activity.serializers import CommentSerializer
from course.models import Course
from course.serializers import CourseSerializer
from cms.models import Blog, WorkSample, Post, Story, Service
from cms.serializers import ServiceSerializer, StorySerializer, PostSerializer, BlogSerializer, WorkSampleSerializer
from django.contrib.auth.models import User


def retrieve_saved_items(user):
    """
    Retrieve saved items for a given user and organize them by object type.
    """
    saved_operations = ItemOperation.objects.filter(
        user=user,
        item_operation_type=3,
        is_deleted=False
    )

    saved_data = {
        "courses": [],
        "blogs": [],
        "work_samples": [],
        "posts": [],
        "stories": [],
        "services": []
    }

    for operation in saved_operations:
        related_id = operation.related_id
        if operation.object_type == 1:  # Course
            item = Course.objects.filter(id=related_id).first()
            if item:
                saved_data["courses"].append(CourseSerializer(item).data)
        elif operation.object_type == 2:  # Blog
            item = Blog.objects.filter(id=related_id).first()
            if item:
                saved_data["blogs"].append(BlogSerializer(item).data)
        elif operation.object_type == 3:  # WorkSample
            item = WorkSample.objects.filter(id=related_id).first()
            if item:
                saved_data["work_samples"].append(WorkSampleSerializer(item).data)
        elif operation.object_type == 4:  # Post
            item = Post.objects.filter(id=related_id).first()
            if item:
                saved_data["posts"].append(PostSerializer(item).data)
        elif operation.object_type == 5:  # Story
            item = Story.objects.filter(id=related_id).first()
            if item:
                saved_data["stories"].append(StorySerializer(item).data)
        elif operation.object_type == 6:  # Service
            item = Service.objects.filter(id=related_id).first()
            if item:
                saved_data["services"].append(ServiceSerializer(item).data)

    return saved_data


def retrieve_comments(user):
    """
    Retrieve comments for a given user and organize them by object type.
    """
    user_comments = Comment.objects.filter(
        user=user,
        comment_type=1,  # 'نظر' type
        is_deleted=False,
        status=True
    )

    comments_data = {
        "all_comments": user_comments.count(),
        "true_comments": user_comments.filter(status=True).count(),
        "false_comments": user_comments.filter(status=False).count(),
        "courses": [],
        "blogs": [],
        "work_samples": [],
        "posts": [],
        "stories": [],
        "services": []
    }

    for comment in user_comments:
        serialized_comment = CommentSerializer(comment).data
        related_id = comment.related_id

        # Replace 'user' ID with serialized user object
        if isinstance(comment.user, int):
            comment_user = User.objects.filter(id=comment.user).first()
            if comment_user:
                serialized_comment['user'] = {
                    "id": comment_user.id,
                    "username": comment_user.username,  # Add fields as needed
                }
            else:
                serialized_comment['user'] = None  # Handle missing user
        else:
            serialized_comment['user'] = comment.user  # Already a User instance

        # Fetch related object data and add extra fields like 'english_title'
        if comment.object_type == 1:  # Course
            related_object = Course.objects.filter(id=related_id).first()
            if related_object:
                serialized_comment['english_title'] = related_object.english_title
            comments_data["courses"].append(serialized_comment)

        elif comment.object_type == 2:  # Blog
            related_object = Blog.objects.filter(id=related_id).first()
            if related_object:
                serialized_comment['english_title'] = related_object.english_title
            comments_data["blogs"].append(serialized_comment)

        elif comment.object_type == 3:  # WorkSample
            related_object = WorkSample.objects.filter(id=related_id).first()
            if related_object:
                serialized_comment['english_title'] = related_object.title
            comments_data["work_samples"].append(serialized_comment)

        elif comment.object_type == 4:  # Post
            related_object = Post.objects.filter(id=related_id).first()
            if related_object:
                serialized_comment['english_title'] = related_object.english_title
            comments_data["posts"].append(serialized_comment)

        elif comment.object_type == 5:  # Story
            related_object = Story.objects.filter(id=related_id).first()
            if related_object:
                serialized_comment['english_title'] = related_object.title
            comments_data["stories"].append(serialized_comment)

        elif comment.object_type == 6:  # Service
            related_object = Service.objects.filter(id=related_id).first()
            if related_object:
                serialized_comment['english_title'] = related_object.title
            comments_data["services"].append(serialized_comment)

    return comments_data
