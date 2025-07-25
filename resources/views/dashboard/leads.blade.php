<x-main-layout title="My Leads">
    @php
        $version = time(); // Force cache refresh
    @endphp
    <div class="leads-container">


        <div class="leads-header">
            <h1>My Leads</h1>

            <!-- Filters -->
            <div class="filter-section">
                <form method="GET" action="{{ route('dashboard.leads') }}" class="filter-form" id="filterForm">
                    <div class="filter-group">
                        <label for="city">Filter by City:</label>
                        <select name="city" id="city">
                            <option value="">All Cities</option>
                            @foreach ($cities as $city)
                                <option value="{{ $city }}" {{ $selectedCity == $city ? 'selected' : '' }}>
                                    {{ $city }}
                                </option>
                            @endforeach
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="type">Filter by Type:</label>
                        <select name="type" id="type">
                            <option value="">All Types</option>
                            @foreach ($types as $type)
                                <option value="{{ $type }}" {{ $selectedType == $type ? 'selected' : '' }}>
                                    {{ ucfirst(str_replace('_', ' ', $type)) }}
                                </option>
                            @endforeach
                        </select>
                    </div>

                    <button type="submit" class="filter-btn">Apply Filters</button>
                </form>
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
            @if ($property_managers->count() > 0)
                <div class="leads-grid">
                    @foreach ($property_managers as $property_manager)
                        <div class="lead-card">
                            <h2>{{ $property_manager->name }}</h2>
                            <div class="lead-details">
                                <p><strong>Type:</strong> <span
                                        class="type-badge type-{{ $property_manager->type }}">{{ ucfirst(str_replace('_', ' ', $property_manager->type)) }}</span>
                                </p>
                                <p><strong>City:</strong> {{ $property_manager->city ?? 'N/A' }}</p>
                                <p><strong>Phone:</strong> <a
                                        href="tel:{{ $property_manager->phone }}">{{ $property_manager->phone ?? 'N/A' }}</a>
                                </p>
                                <p><strong>Address:</strong> {{ $property_manager->address ?? 'N/A' }}</p>
                                <p><strong>Website:</strong> {{ $property_manager->website ?? 'N/A' }}</p>
                            </div>
                            <div class="lead-meta">
                                <a href="{{ $property_manager->yellowpages_profile }}" target="_blank"
                                    class="lead-link">View
                                    Profile</a>
                            </div>
                            <div class="lead-actions">
                                <form action="/dashboard/saveContact" method="post" class="save-contact-form">
                                    @csrf
                                    <button type="button" class="save-contact-btn"
                                        onclick="openSaveContactModal({{ $property_manager->id }}, {{ json_encode($property_manager->name) }}, {{ json_encode($property_manager->name) }}, {{ json_encode($property_manager->phone) }}, {{ json_encode($property_manager->email ?? 'N/A') }}, {{ json_encode($property_manager->address) }}, {{ json_encode($property_manager->city) }}, {{ json_encode($property_manager->state ?? 'N/A') }}, {{ json_encode($property_manager->zip ?? 'N/A') }}, {{ json_encode($property_manager->type) }})">
                                        <i class="fa-solid fa-save"></i>
                                        Save Contact
                                    </button>
                                </form>
                                <a href="/dashboard/removeLead/{{ $property_manager->id }}" class="remove-lead-btn">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                            </div>
                        </div>
                    @endforeach
                </div>
                <!-- Pagination -->
                <div class="pagination-container">
                    @if ($property_managers->hasPages())
                        <div class="pagination">
                            {{-- Previous Page Link --}}
                            @if ($property_managers->onFirstPage())
                                <span class="page-link disabled">Previous</span>
                            @else
                                <a href="{{ $property_managers->previousPageUrl() }}" class="page-link">Previous</a>
                            @endif

                            {{-- Page Numbers Container --}}
                            <div class="page-numbers">
                                {{-- Compact Pagination Elements --}}
                                @php
                                    $currentPage = $property_managers->currentPage();
                                    $lastPage = $property_managers->lastPage();
                                    $showPages = 2; // Show 2 pages on each side

                                    $start = max(1, $currentPage - $showPages);
                                    $end = min($lastPage, $currentPage + $showPages);

                                    // Only show first page if we're far from it
$showFirst = $start > 2;

// Only show last page if we're far from it
                                    $showLast = $end < $lastPage - 1;
                                @endphp

                                {{-- First page if far from current --}}
                                @if ($showFirst)
                                    <a href="{{ $property_managers->url(1) }}" class="page-link">1</a>
                                    <span class="pagination-ellipsis">...</span>
                                @endif

                                {{-- Page numbers around current --}}
                                @for ($page = $start; $page <= $end; $page++)
                                    @if ($page == $currentPage)
                                        <span class="page-link active">{{ $page }}</span>
                                    @else
                                        <a href="{{ $property_managers->url($page) }}"
                                            class="page-link">{{ $page }}</a>
                                    @endif
                                @endfor

                                {{-- Last page if far from current --}}
                                @if ($showLast)
                                    <span class="pagination-ellipsis">...</span>
                                    <a href="{{ $property_managers->url($lastPage) }}"
                                        class="page-link">{{ $lastPage }}</a>
                                @endif



                            </div>

                            {{-- Next Page Link --}}
                            @if ($property_managers->hasMorePages())
                                <a href="{{ $property_managers->nextPageUrl() }}" class="page-link">Next</a>
                            @else
                                <span class="page-link disabled">Next</span>
                            @endif
                        </div>

                        <div class="pagination-info">
                            Showing {{ $property_managers->firstItem() }} to {{ $property_managers->lastItem() }}
                            of
                            {{ $property_managers->total() }} results
                        </div>
                    @endif
                </div>
            @else
                <div class="no-leads">
                    <h2>No leads found</h2>
                    <p>Start searching leads here</p>
                    <button class="refresh-btn" onclick="window.location.reload()">Refresh Page</button>
                </div>
            @endif
        </div>

        <!-- Save Contact Modal -->
        <div id="saveContactModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Save Contact</h2>
                    <span class="close" onclick="closeSaveContactModal()">&times;</span>
                </div>
                <div class="modal-body">
                    <form id="saveContactForm" action="/dashboard/saveContact" method="post">
                        @csrf
                        <input type="hidden" id="contactId" name="contact_id">

                        <div class="contact-details">
                            <h3>Contact Information</h3>
                            <div class="detail-grid">
                                <div class="detail-item">
                                    <label>Name:</label>
                                    <span id="modalCompanyName"></span>
                                </div>
                                <div class="detail-item">
                                    <label>Contact:</label>
                                    <span id="modalContactName"></span>
                                </div>
                                <div class="detail-item">
                                    <label>Phone:</label>
                                    <span id="modalPhone"></span>
                                </div>
                                <div class="detail-item">
                                    <label>Email:</label>
                                    <span id="modalEmail"></span>
                                </div>
                                <div class="detail-item">
                                    <label>Address:</label>
                                    <span id="modalAddress"></span>
                                </div>
                                <div class="detail-item">
                                    <label>City:</label>
                                    <span id="modalCity"></span>
                                </div>
                                <div class="detail-item">
                                    <label>State:</label>
                                    <span id="modalState"></span>
                                </div>
                                <div class="detail-item">
                                    <label>ZIP:</label>
                                    <span id="modalZip"></span>
                                </div>
                                <div class="detail-item">
                                    <label>Type:</label>
                                    <span id="modalType"></span>
                                </div>
                            </div>
                        </div>

                        <div class="notes-section">
                            <label for="notes">Notes:</label>
                            <textarea id="notes" name="notes" rows="4" placeholder="Add any notes about this contact..."></textarea>
                        </div>

                        <div class="modal-actions">
                            <button type="button" class="btn-cancel"
                                onclick="closeSaveContactModal()">Cancel</button>
                            <button type="submit" class="btn-save">Save Contact</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <script>
            // Modal functions
            function openSaveContactModal(id, companyName, contactName, phone, email, address, city, state, zip, type) {
                try {
                    document.getElementById('contactId').value = id || '';
                    document.getElementById('modalCompanyName').textContent = companyName || 'N/A';
                    document.getElementById('modalContactName').textContent = contactName || 'N/A';
                    document.getElementById('modalPhone').textContent = phone || 'N/A';
                    document.getElementById('modalEmail').textContent = email || 'N/A';
                    document.getElementById('modalAddress').textContent = address || 'N/A';
                    document.getElementById('modalCity').textContent = city || 'N/A';
                    document.getElementById('modalState').textContent = state || 'N/A';
                    document.getElementById('modalZip').textContent = zip || 'N/A';
                    document.getElementById('modalType').textContent = type || 'N/A';
                    document.getElementById('saveContactModal').style.display = 'block';
                } catch (error) {
                    console.error('Error opening modal:', error);
                    alert('Error opening contact details. Please try again.');
                }
            }

            function closeSaveContactModal() {
                document.getElementById('saveContactModal').style.display = 'none';
                document.getElementById('notes').value = '';
            }

            // Close modal when clicking outside
            window.onclick = function(event) {
                const modal = document.getElementById('saveContactModal');
                if (event.target === modal) {
                    closeSaveContactModal();
                }
            }

            // Debug form submission
            document.getElementById('filterForm').addEventListener('submit', function(e) {
                console.log('Form submitted');
                console.log('City:', document.getElementById('city').value);
                console.log('Type:', document.getElementById('type').value);
            });
        </script>
</x-main-layout>
