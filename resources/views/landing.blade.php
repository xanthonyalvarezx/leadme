<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LeadMe - Welcome</title>
    <link rel="stylesheet" href="/css/landing.css">
</head>

<body>
    <div class="main-content">
        <div class="logo-container">
            <img src="{{ asset('images/lead_me_logo.png') }}" alt="LeadMe Logo" class="logo">
        </div>
        <div class="container">
            <div class="card login-card">
                <h2>Login</h2>
                <p>Welcome back! Sign in to your account to continue managing your leads and growing your business.</p>
                <a href="auth/login">Log In</a>
            </div>

            <div class="card register-card">
                <h2>Register</h2>
                <p>Join LeadMe today! Create your account and start building meaningful connections with your leads.</p>
                <a href="auth/register">Get Started</a>
            </div>
        </div>
    </div>
</body>

</html>
