<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;

class RunLeadScraper extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'leads:scrape';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Run the combined lead scraper to collect property managers and realtors';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $this->info('Starting scheduled lead scraping...');

        try {
            // Get the path to the combined scraper script
            $script = base_path('app/selenium/combined_scrape.py');

            // Check if the script exists
            if (!file_exists($script)) {
                $this->error("Script not found: {$script}");
                return 1;
            }

            $this->info('Running combined scraper...');

            // Run the Python script with UTF-8 encoding
            $command = "python -X utf8 " . escapeshellarg($script);
            $output = [];
            $returnCode = 0;

            exec($command . " 2>&1", $output, $returnCode);

            // Log the output
            $outputString = implode("\n", $output);
            Log::info('Lead scraper executed', [
                'script' => $script,
                'return_code' => $returnCode,
                'output' => $outputString
            ]);

            if ($returnCode === 0) {
                $this->info('Lead scraping completed successfully!');
                $this->info('Check the logs for detailed output.');
                return 0;
            } else {
                $this->error('Lead scraping failed!');
                $this->error('Output: ' . $outputString);
                return 1;
            }
        } catch (\Exception $e) {
            $this->error('Error running lead scraper: ' . $e->getMessage());
            Log::error('Lead scraper error', [
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);
            return 1;
        }
    }
}
