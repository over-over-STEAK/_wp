<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Blog Signup</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>Login</h1>
            <nav>
                <a href="{{ url_for('post.index') }}" class="btn">Home</a>
                <a href="{{ url_for('auth.signup') }}" class="btn">Sign Up</a>
            </nav>
        </header>

        <main>
            <div class="form-container">
                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        {% for category, message in messages %}
                            <div class="flash-message {{ category }}">{{ message }}</div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}

                <form action="{{ url_for('auth.login') }}" method="post" autocomplete="off">
                    {# CSRF token if using Flask-WTF #}
                    {% if csrf_token %}
                        {{ csrf_token() }}
                    {% endif %}

                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" id="username" name="username" required value="{{ username | default('') }}">
                    </div>

                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" required>
                    </div>

                    <button type="submit" class="btn">Login</button>
                </form>
            </div>
        </main>
    </div>
</body>
</html>
