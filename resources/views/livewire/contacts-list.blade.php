<div>
    <div class="search-container">
        <div class="search-input-wrapper">
            <i class="fa-solid fa-search search-icon"></i>
            <input wire:model.live.debounce.300ms="search" type="text"
                placeholder="Search contacts by name, phone, city, or notes..." class="search-input">
            @if ($search)
                <button wire:click="clearSearch" type="button" class="clear-search-btn">
                    <i class="fa-solid fa-times"></i>
                </button>
            @endif
        </div>
    </div>

    @if (session('success'))
        <div class="alert alert-success">
            {{ session('success') }}
        </div>
    @endif

    @if (session('error'))
        <div class="alert alert-error">
            {{ session('error') }}
        </div>
    @endif

    @if (session('message'))
        <div class="alert alert-info">
            {{ session('message') }}
        </div>
    @endif

    @if ($contacts->count() > 0)
        <div class="contacts-grid">
            @foreach ($contacts as $contact)
                <div class="contact-card">
                    <div class="contact-info">
                        <div class="contact-header">
                            <h2>{{ $contact->name }}</h2>
                            <span class="type-badge type-{{ $contact->type }}">
                                {{ ucfirst(str_replace('_', ' ', $contact->type)) }}
                            </span>
                        </div>

                        <div class="contact-details">
                            @if ($contact->phone)
                                <div class="detail-item">
                                    <i class="fa-solid fa-phone"></i>
                                    <a href="tel:{{ $contact->phone }}">{{ $contact->phone }}</a>
                                </div>
                            @endif

                            @if ($contact->address)
                                <div class="detail-item">
                                    <i class="fa-solid fa-location-dot"></i>
                                    <span>{{ $contact->address }}</span>
                                </div>
                                <div class="detail-item">
                                    <a href="https://www.google.com/maps/dir/?api=1&destination={{ urlencode($contact->address) }}"
                                        target="_blank" class="btn-directions">
                                        <i class="fa-solid fa-directions"></i>
                                        Get Directions
                                    </a>
                                </div>
                            @endif

                            @if ($contact->city)
                                <div class="detail-item">
                                    <i class="fa-solid fa-city"></i>
                                    <span>{{ $contact->city }}</span>
                                </div>
                            @endif

                            @if ($contact->website)
                                <div class="detail-item">
                                    <i class="fa-solid fa-globe"></i>
                                    <a href="{{ $contact->website }}" target="_blank" class="btn-website">Visit
                                        Website</a>
                                </div>
                            @endif

                        </div>

                        <div class="contact-actions">
                            <button wire:click="editContact({{ $contact->id }})" class="btn-edit"
                                wire:loading.attr="disabled">
                                <i class="fa-solid fa-edit"></i>
                                Edit
                            </button>
                            <button wire:click="deleteContact({{ $contact->id }})" class="btn-delete"
                                wire:loading.attr="disabled"
                                onclick="return confirm('Are you sure you want to delete this contact?')">
                                <i class="fa-solid fa-trash"></i>
                                Delete
                            </button>
                        </div>
                    </div>

                    <div class="contact-notes">
                        <h3>Notes</h3>
                        <div class="notes-content">
                            @if ($contact->notes)
                                <p>{{ $contact->notes }}</p>
                            @else
                                <p class="no-notes">No notes added yet.</p>
                            @endif
                        </div>
                        <div class="notes-actions">
                            <button wire:click="addNote({{ $contact->id }})" class="btn-add-note"
                                wire:loading.attr="disabled">
                                <i class="fa-solid fa-plus"></i>
                                Add Note
                            </button>
                        </div>
                    </div>
                </div>
            @endforeach
        </div>
    @else
        <div class="no-contacts">
            @if ($search)
                <h2>No contacts found</h2>
                <p>No contacts match your search criteria</p>
                <button wire:click="clearSearch" class="btn-primary">
                    <i class="fa-solid fa-search"></i>
                    Clear Search
                </button>
            @else
                <h2>No contacts found</h2>
                <p>Start saving contacts from your leads to see them here</p>
                <a href="{{ route('dashboard.leads') }}" class="btn-primary">
                    <i class="fa-solid fa-arrow-left"></i>
                    Go to Leads
                </a>
            @endif
        </div>
    @endif

    <!-- Loading indicator -->
    <div wire:loading class="loading-overlay">
        <div class="loading-spinner">
            <i class="fa-solid fa-spinner fa-spin"></i>
            <span>Searching...</span>
        </div>
    </div>
</div>
