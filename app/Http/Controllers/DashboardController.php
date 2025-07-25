<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Contact;
use App\Models\PropertyManager;

class DashboardController extends Controller
{
    public function saveContact(Request $request)
    {
        $request->validate([
            'contact_id' => 'required|exists:property_managers,id',
            'notes' => 'nullable|string|max:1000',
        ]);

        // Get the original contact data from property_managers table
        $propertyManager = PropertyManager::findOrFail($request->contact_id);

        // Check if contact already exists
        $existingContact = Contact::where('name', $propertyManager->name)
            ->where('phone', $propertyManager->phone)
            ->first();

        if ($existingContact) {
            return redirect()->back()->with('error', 'This contact has already been saved.');
        }

        // Create new contact
        Contact::create([
            'name' => $propertyManager->name,
            'phone' => $propertyManager->phone,
            'address' => $propertyManager->address,
            'website' => $propertyManager->website,
            'yellowpages_profile' => $propertyManager->yellowpages_profile,
            'city' => $propertyManager->city,
            'type' => $propertyManager->type,
            'notes' => $request->notes,
        ]);

        // Set the property manager as inactive
        $propertyManager->update(['active' => false]);

        return redirect()->back()->with('success', 'Contact saved successfully!');
    }

    public function removeLead($id)
    {
        $propertyManager = PropertyManager::findOrFail($id);

        // Set the property manager as inactive instead of deleting
        $propertyManager->update(['active' => false]);

        return redirect()->back()->with('success', 'Lead removed successfully!');
    }
}
