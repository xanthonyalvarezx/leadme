<?php

namespace App\Http\Controllers;

use App\Models\Job;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class JobController extends Controller
{
    /**
     * Create a new job from scraper data
     */
    public function createFromScraper(Request $request): JsonResponse
    {
        $request->validate([
            'title' => 'required|string|max:255',
            'details' => 'required|string',
            'link' => 'required|url',
            'posted_date' => 'required|string',
        ]);

        try {
            // Check if job already exists based on title and details
            $existingJob = Job::where('title', $request->title)
                ->where('details', $request->details)
                ->first();

            if ($existingJob) {
                return response()->json([
                    'success' => false,
                    'message' => 'Job already exists',
                    'job' => $existingJob
                ], 409); // Conflict status code
            }

            $job = Job::create([
                'title' => $request->title,
                'details' => $request->details,
                'link' => $request->link,
                'posted_date' => $request->posted_date,
            ]);

            return response()->json([
                'success' => true,
                'message' => 'Job created successfully',
                'job' => $job
            ], 201);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Failed to create job',
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * Get all jobs
     */
    public function index(): JsonResponse
    {
        $jobs = Job::orderBy('created_at', 'desc')->get();

        return response()->json([
            'success' => true,
            'jobs' => $jobs
        ]);
    }

    /**
     * Get a specific job
     */
    public function show($id): JsonResponse
    {
        $job = Job::find($id);

        if (!$job) {
            return response()->json([
                'success' => false,
                'message' => 'Job not found'
            ], 404);
        }

        return response()->json([
            'success' => true,
            'job' => $job
        ]);
    }
}
