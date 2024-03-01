from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import feedparser
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure database connection
DATABASE_URI = 'mysql+pymysql://admin:password@mysql:3306/mydatabase'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255), unique=True)
    source = db.Column(db.String(255))  # Source of the article
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # Date when the article was added

FEEDS = {
    'Feedburner - DevOps': 'http://feeds.feedburner.com/DevopsDotCom',
    'Reddit - Programming': 'https://www.reddit.com/r/programming/.rss',
    'Infoq - Cloud': 'https://www.infoq.com/cloud-computing/rss/',
    'Thehackernews - Security': 'https://thehackernews.com/feeds/posts/default',
    'Feedburner - Tech': 'http://feeds.feedburner.com/TechCrunch/'  # Example new feed added
}

def fetch_articles():
    with app.app_context():
        for source, url in FEEDS.items():  # Iterate over the dictionary items
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Check if the article already exists in the database by its link
                if not Article.query.filter_by(link=entry.link).first():
                    # Create a new article with the title, link, and source derived from the key
                    article = Article(title=entry.title, link=entry.link, source=source)
                    # Add the new article to the session
                    db.session.add(article)
            # Commit the session to save all new articles to the database
        db.session.commit()



@app.route('/articles')
def get_articles():
    articles = Article.query.order_by(Article.date_added.desc()).all()
    return jsonify([{'id': article.id, 'title': article.title, 'link': article.link, 'source': article.source, 'date_added': article.date_added.isoformat()} for article in articles])

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_articles, trigger="interval", minutes=5)
    scheduler.start()

    with app.app_context():
        db.create_all()
        fetch_articles()

    atexit.register(lambda: scheduler.shutdown())

    app.run(debug=True, host='0.0.0.0', port=5000)

