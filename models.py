from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    social_accounts = db.relationship('SocialAccount', backref='user', lazy='dynamic')
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    auto_replies = db.relationship('AutoReply', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256:260000')
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class SocialAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20), nullable=False)  # twitter, facebook, instagram, tiktok, threads
    account_id = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    access_token = db.Column(db.String(500))
    access_token_secret = db.Column(db.String(500))  # For Twitter
    refresh_token = db.Column(db.String(500))  # For platforms that use refresh tokens
    token_expiry = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    posts = db.relationship('Post', backref='social_account', lazy='dynamic')
    auto_replies = db.relationship('AutoReply', backref='social_account', lazy='dynamic')
    
    def __repr__(self):
        return f'<SocialAccount {self.platform}:{self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __table_args__ = (
        db.Index('idx_user_status', 'user_id', 'status'),
        db.Index('idx_posted_time', 'posted_time'),
    )
    __table_args__ = (
        db.Index('idx_user_status', 'user_id', 'status'),
        db.Index('idx_posted_time', 'posted_time'),
    )
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(500))  # URL to stored media
    scheduled_time = db.Column(db.DateTime)
    posted_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, scheduled, posted, failed
    platform_post_id = db.Column(db.String(100))  # ID of the post on the platform
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    social_account_id = db.Column(db.Integer, db.ForeignKey('social_account.id'), nullable=False)
    
    def __repr__(self):
        return f'<Post {self.id} - {self.status}>'

class AutoReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trigger_type = db.Column(db.String(20), nullable=False)  # keyword, message_type, all
    trigger_value = db.Column(db.String(500))  # Keywords or message type
    response_text = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    social_account_id = db.Column(db.Integer, db.ForeignKey('social_account.id'), nullable=False)
    
    def __repr__(self):
        return f'<AutoReply {self.id} - {self.trigger_type}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __table_args__ = (
        db.Index('idx_msg_platform_time', 'platform', 'received_at'),
        db.Index('idx_msg_sender', 'sender_id', 'platform'),
        db.Index('idx_msg_user_replied', 'user_id', 'replied'),
        db.Index('idx_msg_account_time', 'social_account_id', 'received_at')
    )
    platform = db.Column(db.String(20), nullable=False)  # twitter, facebook, instagram, tiktok, threads
    platform_message_id = db.Column(db.String(100), nullable=False)
    sender_id = db.Column(db.String(100), nullable=False)
    sender_name = db.Column(db.String(100))
    content = db.Column(db.Text)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    replied = db.Column(db.Boolean, default=False)
    reply_text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    social_account_id = db.Column(db.Integer, db.ForeignKey('social_account.id'), nullable=False)
    
    def __repr__(self):
        return f'<Message {self.id} from {self.sender_name}>'

class ContentLibrary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(500))
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<ContentLibrary {self.id} - {self.name}>'

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, paused
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship
    campaign_posts = db.relationship('CampaignPost', backref='campaign', lazy='dynamic')
    
    def __repr__(self):
        return f'<Campaign {self.id} - {self.name}>'

class CampaignPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    def __repr__(self):
        return f'<CampaignPost {self.campaign_id} - {self.post_id}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20), nullable=False)  # twitter, facebook, instagram, tiktok, threads
    platform_comment_id = db.Column(db.String(100), nullable=False)
    commenter_id = db.Column(db.String(100), nullable=False)
    commenter_name = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    replied_at = db.Column(db.DateTime)
    reply_content = db.Column(db.Text)
    is_replied = db.Column(db.Boolean, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    social_account_id = db.Column(db.Integer, db.ForeignKey('social_account.id'), nullable=False)
    
    # Relationships
    post = db.relationship('Post', backref=db.backref('post_comments', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('user_comments', lazy='dynamic'))
    social_account = db.relationship('SocialAccount', backref=db.backref('account_comments', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Comment {self.id} by {self.commenter_name}>'
