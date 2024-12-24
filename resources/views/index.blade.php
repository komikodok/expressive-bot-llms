@extends('layouts.app')

@section('title', 'Laravel')

@section('content')
    <!-- Container -->
    <div class="flex h-screen overflow-hidden fade-in-animation">
        @if (session('error'))
            <!-- Overlay -->
            <div id="errorOverlay" class="fixed inset-0 bg-white bg-opacity-70 z-40"></div>
            <!-- Error Message -->
            <div id="errorBox" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="bg-red-600 px-6 py-2 rounded relative flex max-h-32 max-w-[80%] shadow-sm shadow-red-600">
                    <button id="closeError" class="absolute -top-6 -right-4 text-3xl font-bold text-red-800">
                        &times;
                    </button>
                    <span class="text-slate-200 m-auto break-all break-words">{{ session('error') }}</span>
                </div>
            </div>
        @endif
        <!-- Side Bar -->
        <div id="sideBar" class="w-96 h-full max-md:absolute max-md:w-64 max-md:-translate-x-full max-md:transition-all max-md:duration-300 rounded-md overflow-hidden">
            <!-- Header -->
            <header class="bg-slate-100 w-full h-14 flex justify-end items-center rounded-lg p-3 mb-1 shadow-md shadow-gray-300">
                <a href="{{ route('google.redirect') }}" class="w-20 text-center border-2 border-slate-100 ring-2 ring-red-800 bg-red-800 rounded-lg">
                    <span class="text-sm text-slate-200 font-semibold my-auto">Login</span>
                </a>
            </header>
            <!-- Body -->
            <div class="border-x border-gray-300 bg-slate-100 rounded-lg w-full h-full"></div>
        </div>
        <!-- Chatbot -->
        <div id="chatBot" class="w-full h-[98%] md:px-3 lg:px-5 max-md:px-2">
            <!-- Header -->
            <header class="bg-red-900 flex w-full h-14 rounded-lg shadow-md shadow-gray-400">
                <!-- Profile Assistant -->
                <div class="flex ml-5 ">
                    <div class="border border-black rounded-full w-10 h-10 my-auto">
                        <img src="" class="text-xs" alt="Bot Profile">
                    </div>
                    <p class="text-slate-200 text-lg ml-2 my-auto font-extrabold">Assistant</p>
                </div>
                <!-- Side Bar Button -->
                <button id="sideBarButton" class="ml-auto mr-5 md:hidden transition-all duration-400">
                    <svg class="w-6 h-6 text-white m-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    </svg>
                </button>
            </header>
            <!-- Body -->
            <div class="h-5/6 w-full flex p-1 justify-center items-center overflow-hidden">
                <div class="border-opacity-10 border-t-2 border-gray-400 shadow-md shadow-gray-400 rounded-2xl h-full w-full p-2">
                    <!-- Ballon's Chat -->   
                    <div id="chatContainer" class="space-y-1 p-4 h-full overflow-y-scroll flex flex-col" style="scrollbar-width:thin;">
                        <!-- Assistant Message -->
                        <div class="justify-start p-3 flex">
                            <div class="border border-black w-14 h-14 flex rounded-full">
                                <img src="" class="text-md m-auto" alt="Bot Profile">
                            </div>
                            <p class="bg-red-800 text-slate-200 rounded-xl p-3 mx-2 max-w-[80%] break-words break-all">Perkenalkan siapa dirimu, 
                                <a href="{{ route('google.redirect') }}" class="text-blue-400 underline">login sekarang</a>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Chat Form -->
            <form id="chatForm" class="flex mt-0.5 justify-center items-center h-12 w-full overflow-hidden" action="{{ route('index.post') }}" method="POST">
                @csrf
                <input id="messageInput" class="w-full h-full text-start rounded-xl p-2 border-2 border-red-200 focus:outline-red-500" type="text" name="message" placeholder="Message Assistant...">
                <button id="sendButton" class="disabled:opacity-50 disabled:cursor-not-allowed ml-2 flex items-center justify-center text-slate-200 font-semibold rounded-lg bg-red-800 w-16 h-full focus:outline-1 focus:outline-red-900 transition-all duration-300" type="submit" disabled>
                    <span id="sendIcon" class="text-2xl m-auto">↑</span>
                </button>
            </form>
        </div>
    </div>

    <script>
        const postUrl = @json(route('index.post'));
    </script>
    
    <script src={{ asset('js/sidebar.js') }}></script>
    <script src={{ asset('js/chatbot.js') }}></script>
@endsection