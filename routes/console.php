<?php

use Illuminate\Foundation\Inspiring;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Schedule;

Artisan::command('inspire', function () {
    $this->comment(Inspiring::quote());
})->purpose('Display an inspiring quote');

// Schedule the lead scraper to run every night at midnight
Schedule::command('leads:scrape')
    ->dailyAt('00:00')
    ->description('Run lead scraper every night at midnight')
    ->withoutOverlapping();
