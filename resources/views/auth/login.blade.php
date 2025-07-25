<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>LeadMe | Login</title>
    <link rel="stylesheet" href="/css/login.css">
</head>

<body>
    <div class="container">
        <div class="card">
            <h2>Login</h2>
            <form action="/auth/submitlogin" method="POST">
                @csrf
                <input type="email" placeholder="Email" name="email" required>
                <input type="password" placeholder="Password" name="password" required>
                <button type="submit">Sign In</button>
                <p>Don't have an account? <a href="/auth/register">Register</a></p>
            </form>
        </div>
    </div>
</body>

</html>
