<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Signup</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>Blog Posts</h1>
            <nav>
                {% if user is defined and user %}
                    <span class="welcome-message">Welcome, {{ user.username }}!</span>
                    <a href="{{ url_for('post.new_post') }}" class="btn">New Post</a>
                    <a href="{{ url_for('auth.logout') }}" class="btn">Logout</a>
                {% else %}
                    <a href="{{ url_for('auth.login') }}" class="btn">Login</a>
                    <a href="{{ url_for('auth.signup') }}" class="btn">Sign Up</a>
                {% endif %}
            </nav>
        </header>

        <main>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <section class="flash-container">
                        {% for category, message in messages %}
                            <div class="flash-message {{ category }}">{{ message }}</div>
                        {% endfor %}
                    </section>
                {% endif %}
            {% endwith %}

            {% if posts %}
                {% for post in posts %}
                    <div class="post">
                        <h2>{{ post.title }}</h2>
                        <p class="post-meta">
                            Posted by {{ post.author.username }} on {{ post.created_at.strftime('%Y-%m-%d %H:%M:%S') }}
                        </p>
                        <div class="post-content">
                            {{ post.content }}
                        </div>
                        {% if user and post.user_id == user.id %}
                            <form action="{{ url_for('post.delete_post', post_id=post.id) }}" method="post" onsubmit="return confirm('Are you sure you want to delete this post?');">
                                {{ csrf_token() }}
                                <button type="submit" class="delete-btn">Delete Post</button>
                            </form>
                        {% endif %}
                    </div>
                {% endfor %}
            {% else %}
                <p class="no-posts">No posts yet. Be the first to create one!</p>
            {% endif %}
        </main>
    </div>
</body>
</html>
