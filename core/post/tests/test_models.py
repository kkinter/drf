import pytest
from core.fixtures.user import user
from core.post.models import Post


@pytest.mark.django_db
def test_create_post(user):
    post = Post.objects.create(author=user, body="Test post body")

    assert post.body == "Test post body"
    assert post.author == user
