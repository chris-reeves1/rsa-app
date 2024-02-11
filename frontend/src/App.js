import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetch('/articles')
      .then(response => response.json())
      .then(data => setArticles(data))
      .catch(error => console.error('Error fetching articles:', error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Tech Articles Feed</h1>
      </header>
      <main>
        {articles.map((article) => (
          <div key={article.id} className="article">
            <h2>{article.title}</h2>
            <span className="article-source">({article.source})</span>
            <p>Added on: {new Date(article.date_added).toLocaleDateString()}</p>
            <a href={article.link} target="_blank" rel="noopener noreferrer">Read more</a>
          </div>
        ))}
      </main>
    </div>
  );
}

export default App;

