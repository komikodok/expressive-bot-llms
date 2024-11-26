@extends('layouts.app')

@section('title', 'Laravel')
    
@section('content')
    <!-- Container -->
    <div class="flex h-screen overflow-hidden">
        <!-- Side Bar -->
        <div id="sideBar" class="w-96 h-full md:static max-md:absolute max-md:w-64 max-md:-translate-x-full rounded-md overflow-hidden">
            <!-- Header -->
            <header class="bg-slate-100 w-full h-14 flex justify-end rounded-lg p-3 mb-1 shadow-md shadow-gray-300"></header>
            <!-- Body -->
            <div class="border-x border-gray-300 bg-slate-100 rounded-lg w-full h-full"></div>
        </div>
        <!-- Chatbot -->
        <div class="w-full h-full md:px-5 max-md:px-2">
            <!-- Header -->
            <header class="bg-red-900 flex w-full h-14 rounded-lg shadow-md shadow-gray-400">
                <div class="border border-black rounded-full w-10 h-10 ml-5 my-auto">
                    <img src="" class="text-xs" alt="Bot Profile">
                </div>
                <p class="text-slate-200 text-lg ml-2 my-auto font-extrabold">Assistant</p>
                <button id="sideBarButton" class="rounded-full h-14 w-14 ml-auto mr-5 md:hidden">
                    <svg class="w-6 h-6 text-white m-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    </svg>
                </button>
            </header>
            <!-- Body -->
            <div class="h-5/6 w-full flex p-2.5 justify-center items-center overflow-hidden">
                <div class="border-opacity-10 border-t-2 border-gray-400 shadow-md shadow-gray-400 rounded-2xl h-full w-full p-2">
                    <!-- Ballon's Chat -->   
                    <div id="chatContainer" class="space-y-1 p-4 h-full overflow-y-scroll flex flex-col" style="scrollbar-width:thin;">
                        <!-- User Message -->
                        <div class="justify-end p-3 flex">
                            <div class="bg-gray-200 rounded-xl p-3 mx-2 max-w-[80%] break-words break-all">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi corrupti voluptates odit quod beatae at natus, sapiente odio molestiae totam doloribus blanditiis ipsum alias, fugit molestias officia. Sit, ipsam placeat. Lorem ipsum dolor sit amet consectetur adipisicing elit. Harum eos esse quas doloribus laboriosam aliquid, dicta quo beatae saepe repudiandae repellat at non nam quidem debitis voluptates hic magni fugit.</div>
                            <div class="border border-black w-14 h-14 rounded-full">
                                <img src="" class="text-md m-auto" alt="User Profile">
                            </div>
                        </div>
                        <!-- Assistant Message -->
                        <div class="justify-start p-3 flex">
                            <div class="border border-black w-14 h-14 flex rounded-full">
                                <img src="" class="text-md m-auto" alt="Bot Profile">
                            </div>
                            <div class="bg-red-800 text-slate-200 rounded-xl p-3 mx-2 max-w-[80%] break-words break-all">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi corrupti voluptates odit quod beatae at natus, sapiente odio molestiae totam doloribus blanditiis ipsum alias, fugit molestias officia. Sit, ipsam placeat. Lorem ipsum dolor sit amet consectetur adipisicing elit. Harum eos esse quas doloribus laboriosam aliquid, dicta quo beatae saepe repudiandae repellat at non nam quidem debitis voluptates hic magni fugit.</div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Chat Form -->
            <form id="chatForm" class="flex space-x-2 justify-center items-center h-12 w-full overflow-hidden" action="{{ route('index.post') }}" method="POST">
                @csrf
                <input id="messageInput" class="w-full h-full text-start rounded-xl p-2 border-2 border-red-200 focus:outline-red-500" type="text" name="message" placeholder="Message Assistant...">
                <button id="sendButton" class="disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center text-slate-200 font-semibold rounded-lg bg-red-800 w-16 h-full focus:outline-1 focus:outline-red-900 transition-all duration-300" type="submit" disabled>
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