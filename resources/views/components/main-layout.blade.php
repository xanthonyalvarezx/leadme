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
    <link rel="stylesheet" href="/css/contacts.css">
    <link rel="stylesheet" href="/css/mobile.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    @stack('styles')
    <script src="/js/nav.js" defer></script>
    @livewireStyles
</head>

<body>
    @include('components.nav')
    <main>
        {{ $slot }}
    </main>
    @include('components.footer')
    @livewireScripts
</body>

</html>
