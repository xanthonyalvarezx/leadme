<?php

namespace App\Http\Controllers;

use App\Models\Job;
use Illuminate\Http\Request;

class PageController extends Controller
{
    public function landing()
    {
        return View('landing');
    }

    public function home()
    {
        return view('dashboard.home');
    }

    public function leads()
    {
        $jobs = Job::orderBy('created_at', 'desc')->paginate(12);
        return view('dashboard.leads', compact('jobs'));
    }
}
