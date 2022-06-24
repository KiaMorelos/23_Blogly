from unittest import TestCase
from app import app
from models import db, User, default_image_url

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class FlaskTests(TestCase):

    def setUp(self):
        """Set up tests"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        User.query.delete()

        user = User(first_name="Jane", last_name="Doe", image_url= f"{default_image_url}")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
 
    def tearDown(self):
        """Tear Down Tests"""
        db.session.rollback()
    

    def test_root(self):
        """Test that root route works, and has expected content"""
        with app.test_client() as client:
            res = client.get('/', follow_redirects=True)
            content = res.data
            self.assertEqual(res.status_code, 200)
            self.assertIn(b'Users', content)

    def test_users(self):
        """Test that users route works, and has expected content"""
        with app.test_client() as client:
            res = client.get('/users', follow_redirects=True)
            content = res.data
            self.assertEqual(res.status_code, 200)
            self.assertIn(b'Users', content)


    def test_add_user_form(self):
        """test make new user form route"""
        with app.test_client() as client:
            res = client.get('/users/new')
            content = res.data
            self.assertEqual(res.status_code, 200)
            self.assertIn(b'Create', content)


    def test_add_user(self):
        with app.test_client() as client:
            """test post route for a new user"""
            d = {"firstname" : "John", "lastname" : "Smith", "url": f"{default_image_url}"}
            res = client.post('/users/new', data=d, follow_redirects=True)
            content = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('John Smith', content)
    
    def test_view_user(self):
        """test view route for existing user"""
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            content = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Viewing: Jane Doe', content)

    
