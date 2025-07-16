<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>LeadMe | {{ $title }}</title>
    <link rel="stylesheet" href="/css/nav.css">
    <link rel="stylesheet" href="/css/footer.css">
    <link rel="stylesheet" href="/css/leads.css">
    @stack('styles')
</head>

<body>
    @include('components.nav')
    <main>
        {{ $slot }}
    </main>
    @include('components.footer')
</body>

</html>
