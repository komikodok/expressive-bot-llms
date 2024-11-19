@extends('layouts.app')

@section('title', 'Laravel')
    
@section('content')
    <!-- Container -->
    <div class="flex border border-black h-screen overflow-hidden">
        <!-- Side Bar -->
        <div class="border border-green-400 w-96 h-full max-md:!w-0 overflow-hidedn">
            <div class="border border-yellow-400 bg-slate-400 w-full h-full"></div>
        </div>
        <!-- Chatbot -->
        <div class="border border-blue-400 w-full">
            <!-- Header -->
            <header class="border border-red-500 flex w-full h-12 items-center justify-center">
                <p class="text-slate-950">Chat with assistant</p>
                <button class="ml-2 rounded-full">⚙</button>
            </header>
            <!-- Body -->
            <div class="border border-purple-950 h-5/6 w-full flex p-4 justify-center items-center overflow-hidden">
                <div class="border border-gray-800 h-full w-full"></div>
            </div>
            <!-- Form Chat -->
            <div class="border border-sky-950 h-full w-full">

            </div>
        </div>
    </div>
@endsection