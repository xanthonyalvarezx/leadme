<?php

namespace App\Http\Controllers;

use App\Models\Job;
use App\Models\Contact;
use Illuminate\Http\Request;
use App\Models\PropertyManager;
use Illuminate\Support\Facades\Log;

class PageController extends Controller
{

    public function login()
    {
        return view('auth.login');
    }

    public function register()
    {


        return view('auth.register');
    }
    public function landing()
    {
        return View('landing');
    }

    public function home()
    {
        return view('dashboard.home');
    }
    public function contacts()
    {
        return view('dashboard.contacts');
    }

    public function leads(Request $request)
    {
        $query = PropertyManager::where('active', true);

        // Debug logging
        Log::info('Leads request', [
            'city' => $request->city,
            'type' => $request->type,
            'all_params' => $request->all()
        ]);

        // Filter by city if provided
        if ($request->filled('city')) {
            $query->where('city', $request->city);
            Log::info('Filtering by city: ' . $request->city);
        }

        // Filter by type if provided
        if ($request->filled('type')) {
            $query->where('type', $request->type);
            Log::info('Filtering by type: ' . $request->type);
        }

        // Get unique cities for filter dropdown (only active)
        $cities = PropertyManager::where('active', true)->distinct()->pluck('city')->filter()->sort()->values();

        // Get unique types for filter dropdown (only active)
        $types = PropertyManager::where('active', true)->distinct()->pluck('type')->filter()->sort()->values();

        $property_managers = $query->orderBy('created_at', 'desc')->paginate(12);

        // Preserve filter parameters in pagination links
        if ($request->filled('city')) {
            $property_managers->appends(['city' => $request->city]);
        }
        if ($request->filled('type')) {
            $property_managers->appends(['type' => $request->type]);
        }

        Log::info('Query results', [
            'total' => $property_managers->total(),
            'count' => $property_managers->count(),
            'cities_count' => $cities->count(),
            'types_count' => $types->count()
        ]);

        return view('dashboard.leads', [
            'property_managers' => $property_managers,
            'cities' => $cities,
            'types' => $types,
            'selectedCity' => $request->city,
            'selectedType' => $request->type
        ]);
    }
}
