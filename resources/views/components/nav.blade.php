<nav>
    <div class="nav-container">
        <div class="logo">
            <a href="/">LeadMe</a>
        </div>
        <div class="nav-links">
            <a href="/dashboard" class="{{ request()->is('dashboard') ? 'active' : '' }}">Home</a>
            <a href="/dashboard/leads" class="{{ request()->is('dashboard/leads*') ? 'active' : '' }}">Leads</a>
            <a href="/dashboard/analytics"
                class="{{ request()->is('dashboard/analytics*') ? 'active' : '' }}">Analytics</a>
            <a href="/dashboard/settings"
                class="{{ request()->is('dashboard/settings*') ? 'active' : '' }}">Settings</a>
        </div>
    </div>
</nav>
