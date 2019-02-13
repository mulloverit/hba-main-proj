"""Models and database functions for image and user management"""

from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()

### Class establishments ###

class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    sign_up_date = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        """Formatted output when class obj is returned. Does not return email or password."""
        return(f"""<User:
                        user_id={self.user_id},
                        username={self.username}),
                        sign_up_date={self.sign_up_date}""")


class InputImage(db.Model):
    """Input image model."""

    __tablename__ = "input_images"

    im_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    im_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    im_upload_begin_datetime = db.Column(db.String(50), nullable=False)
    im_upload_complete_datetime = db.Column(db.String(50), nullable=False)
    im_size_x = db.Column(db.Integer, nullable=False)
    im_size_y = db.Column(db.Integer, nullable=False)
    im_format = db.Column(db.String(10), nullable=False)
    im_mode = db.Column(db.String(10), nullable=False)
    im_s3_url = db.Column(db.String(500), nullable=False)


    def __repr__(self):
        """Formatted output when class obj is returned. Does not return password."""
        return (f"""<InputImage:
                    im_id={self.im_id}, 
                    im_user_id={self.im_user_id}), 
                    im_upload_begin_datetime={self.im_upload_datetime},
                    im_upload_complete_datetime={self.im_upload_datetime},
                    im_size_x={self.im_size_x},
                    im_size_y={self.im_size_y},
                    im_format={self.im_format},
                    im_mode={self.im_mode},
                    im_s3_url={self.im_s3_url}""")


class DiffImage(db.Model):
    """Input image model."""

    __tablename__ = "diff_images"

    diff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diff_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    im_1_id = db.Column(db.Integer, db.ForeignKey('input_images.im_id'))
    im_2_id = db.Column(db.Integer, db.ForeignKey('input_images.im_id'))
    diff_upload_begin_datetime = db.Column(db.String(50), nullable=False)
    diff_upload_complete_datetime = db.Column(db.String(50), nullable=False)
    diff_size_x = db.Column(db.Integer, nullable=False)
    diff_size_y = db.Column(db.Integer, nullable=False)
    diff_format = db.Column(db.String(10), nullable=False)
    diff_mode = db.Column(db.String(10), nullable=False)
    diff_s3_url = db.Column(db.String(500), nullable=False)


    def __repr__(self):
        """Formatted output when class obj is returned. Does not return password."""
        return (f"""<DiffImage:
                    diff_id={self.diff_id}, 
                    diff_user_id={self.diff_user_id}),
                    im_1_id={self.im_1_id},
                    im_2_id={self.im_2_id},
                    diff_upload_begin_datetime={self.diff_upload_datetime},
                    diff_upload_complete_datetime={self.diff_upload_datetime},
                    diff_size_x={self.diff_size_x},
                    diff_size_y={self.diff_size_y},
                    diff_format={self.diff_format},
                    diff_mode={self.diff_mode},
                    diff_s3_url={self.diff_s3_url}""")


### Helper functions ###

def connect_to_db(app):
    """Connect the database to Flask application"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///imgdiffs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to DB.")