<nav>
    <div class="nav-container">
        <div class="logo">
            <a href="/dashboard"><img src="{{ asset('images/lead_me_logo.png') }}" alt="LeadMe Logo"></a>
        </div>

        <!-- Hamburger Menu Button -->
        <div class="hamburger-menu">
            <div class="hamburger-icon">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>

        <div class="nav-links">
            <a href="/dashboard" class="{{ request()->is('dashboard') ? 'active' : '' }}">Home</a>
            <a href="/dashboard/leads" class="{{ request()->is('dashboard/leads*') ? 'active' : '' }}">Leads</a>
            <a href="/dashboard/contacts"
                class="{{ request()->is('dashboard/contacts*') ? 'active' : '' }}">Contacts</a>
            <a href="/dashboard/analytics"
                class="{{ request()->is('dashboard/analytics*') ? 'active' : '' }}">Analytics</a>
            <a href="/dashboard/settings"
                class="{{ request()->is('dashboard/settings*') ? 'active' : '' }}">Settings</a>
            <form action="/auth/logout" method="POST" style="display: inline;">
                @csrf
                <button type="submit" class="logout-btn">Logout</button>
            </form>
        </div>

        <!-- Mobile Menu Overlay -->
        <div class="mobile-overlay"></div>
    </div>
</nav>
