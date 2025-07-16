<x-main-layout title="My Leads">
    <div class="leads-container">
        <div class="leads-header">
            <h1>My Leads</h1>
            <p>Discover handyman opportunities</p>
        </div>

        @if ($jobs->count() > 0)
            <div class="leads-grid">
                @foreach ($jobs as $job)
                    <div class="lead-card">
                        <h2>{{ $job->title }}</h2>
                        <div class="lead-details">
                            <p>{{ $job->details }}</p>
                        </div>
                        <div class="lead-meta">
                            <span class="lead-date">{{ $job->posted_date ?: 'No date' }}</span>
                            <a href="{{ $job->link }}" target="_blank" class="lead-link">View Job</a>
                        </div>
                        <div class="lead-actions">
                            <button class="btn-add-job">Add to My Jobs</button>
                            <button class="btn-remove">Remove</button>
                        </div>
                    </div>
                @endforeach
            </div>

            <!-- Pagination -->
            <div class="pagination-container">
                @if ($jobs->hasPages())
                    <div class="pagination">
                        {{-- Previous Page Link --}}
                        @if ($jobs->onFirstPage())
                            <span class="page-link disabled">Previous</span>
                        @else
                            <a href="{{ $jobs->previousPageUrl() }}" class="page-link">Previous</a>
                        @endif

                        {{-- Pagination Elements --}}
                        @foreach ($jobs->getUrlRange(1, $jobs->lastPage()) as $page => $url)
                            @if ($page == $jobs->currentPage())
                                <span class="page-link active">{{ $page }}</span>
                            @else
                                <a href="{{ $url }}" class="page-link">{{ $page }}</a>
                            @endif
                        @endforeach

                        {{-- Next Page Link --}}
                        @if ($jobs->hasMorePages())
                            <a href="{{ $jobs->nextPageUrl() }}" class="page-link">Next</a>
                        @else
                            <span class="page-link disabled">Next</span>
                        @endif
                    </div>

                    <div class="pagination-info">
                        Showing {{ $jobs->firstItem() }} to {{ $jobs->lastItem() }} of {{ $jobs->total() }} results
                    </div>
                @endif
            </div>
        @else
            <div class="no-leads">
                <h2>No leads found</h2>
                <p>Start scraping handyman jobs to see leads here</p>
                <button class="refresh-btn" onclick="window.location.reload()">Refresh Page</button>
            </div>
        @endif
    </div>
</x-main-layout>
