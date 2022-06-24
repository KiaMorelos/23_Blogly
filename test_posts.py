from unittest import TestCase
from app import app
from models import db, User, Post, default_image_url

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class FlaskTests(TestCase):

    def setUp(self):
        """Set up tests"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Jane", last_name="Doe", image_url= f"{default_image_url}")

        post = Post(title="A Silent Voice", content="a 2016 Japanese animated drama film produced by Kyoto Animation, directed by Naoko Yamada and written by Reiko Yoshida", user=user)

        db.session.add(user)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id
        self.user_id = user.id


 
    def tearDown(self):
        """Tear Down Tests"""
        db.session.rollback()
    

    def test_view_all_posts(self):
        """Test view for individual posts"""
        with app.test_client() as client:
            res = client.get('/all-posts')
            content = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('All Posts', content)

    def test_view_post(self):
        """Test view for individual posts"""
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}')
            content = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Viewing post: A Silent Voice', content)
            self.assertIn('by Jane Doe', content)


    def test_new_post_form(self):
        """Test view for posts form"""
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}/posts/new')
            content = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Create a post for Jane Doe', content)

    def test_add_post(self):
        with app.test_client() as client:
            """test POST route for a new blog post"""
            d = {"title" : "The Secret of Arietty", "content" : "Is a great movie"}
            res = client.post(f'/users/{self.user_id}/posts/new', data=d, follow_redirects=True)
            content = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('The Secret of Arietty', content)

    