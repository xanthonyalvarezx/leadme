<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>LeadMe | Register</title>
    <link rel="stylesheet" href="/css/register.css">
</head>

<body>
    <div class="container">
        <div class="card">
            <h2>Register</h2>
            <form action="/auth/register" method="POST">
                @csrf
                <input type="text" placeholder="Name" name="name" required>
                <input type="email" placeholder="Email" name="email" required>
                <input type="text" placeholder="Company" name="company" required>
                <input type="tel" placeholder="Phone" name="phone" required>
                <input type="text" placeholder="Address" name="address" required>
                <input type="text" placeholder="City" name="city" required>
                <input type="text" placeholder="State" name="state" required>
                <input type="text" placeholder="Zip Code" name="zip" required>
                <input type="password" placeholder="Password" name="password" required>
                <input type="password" placeholder="Confirm Password" name="confirm_password" required>
                <button type="submit">Create Account</button>
                <p>Already have an account? <a href="/auth/login">Login</a></p>
            </form>
        </div>
    </div>
</body>

</html>
