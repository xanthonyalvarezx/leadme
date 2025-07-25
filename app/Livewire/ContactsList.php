<?php

namespace App\Livewire;

use App\Models\Contact;
use Livewire\Component;

class ContactsList extends Component
{
    public $search = '';

    public function render()
    {
        $contacts = Contact::query()
            ->when($this->search, function($query) {
                $query->where(function($q) {
                    $q->where('name', 'like', '%' . $this->search . '%')
                      ->orWhere('phone', 'like', '%' . $this->search . '%')
                      ->orWhere('city', 'like', '%' . $this->search . '%')
                      ->orWhere('notes', 'like', '%' . $this->search . '%')
                      ->orWhere('type', 'like', '%' . $this->search . '%');
                });
            })
            ->orderBy('name')
            ->get();

        return view('livewire.contacts-list', [
            'contacts' => $contacts
        ]);
    }

    public function clearSearch()
    {
        $this->search = '';
    }

    public function editContact($id)
    {
        // TODO: Implement edit functionality
        session()->flash('message', 'Edit functionality coming soon!');
    }

    public function deleteContact($id)
    {
        $contact = Contact::find($id);
        if ($contact) {
            $contact->delete();
            session()->flash('success', 'Contact deleted successfully!');
        } else {
            session()->flash('error', 'Contact not found!');
        }
    }

    public function addNote($id)
    {
        // TODO: Implement add note functionality
        session()->flash('message', 'Add note functionality coming soon!');
    }
}
