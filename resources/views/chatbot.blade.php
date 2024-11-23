@extends('layouts.app')

@section('title', 'Laravel')
    
@section('content')
    <!-- Container -->
    <div class="flex h-screen overflow-hidden">
        <!-- Side Bar -->
        <div class="border border-green-400 bg-slate-400 w-96 h-full max-md:!w-0 transition-all duration-500 overflow-hidden">
            <div class="border border-yellow-400 w-full h-full"></div>
        </div>
        <!-- Chatbot -->
        <div class="w-full h-full">
            <!-- Header -->
            <header class="bg-red-900 flex w-full h-12 items-center justify-center rounded-lg shadow-md shadow-gray-400">
                <p class="text-slate-200 text-lg font-extrabold">Assistant</p>
                <button class="ml-2 rounded-full">⚙</button>
            </header>
            <!-- Body -->
            <div class="h-5/6 w-full flex p-2.5 justify-center items-center overflow-hidden">
                <div class="border-opacity-10 border-t-2 border-gray-400 shadow-md shadow-gray-400 rounded-2xl h-full w-full p-2">
                    <!-- Ballon's Chat -->   
                    <div id="chatContainer" class="space-y-1 p-4 h-full overflow-y-scroll flex flex-col" style="scrollbar-width:thin;">
                        <!-- User Message -->
                        <div class="self-end justify-end p-3 flex">
                            <div class="bg-gray-200 rounded-xl p-3 mx-2 max-w-[80%] break-words break-all">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi corrupti voluptates odit quod beatae at natus, sapiente odio molestiae totam doloribus blanditiis ipsum alias, fugit molestias officia. Sit, ipsam placeat. Lorem ipsum dolor sit amet consectetur adipisicing elit. Harum eos esse quas doloribus laboriosam aliquid, dicta quo beatae saepe repudiandae repellat at non nam quidem debitis voluptates hic magni fugit.</div>
                            <div class="border border-black w-14 h-14 rounded-full"></div>
                        </div>
                        <!-- Assistant Message -->
                        <div class="self-start justify-start p-3 flex">
                            <div class="border border-black w-14 h-14 rounded-full"></div>
                            <div class="bg-red-800 text-slate-200 rounded-xl p-3 mx-2 max-w-[80%] break-words break-all">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi corrupti voluptates odit quod beatae at natus, sapiente odio molestiae totam doloribus blanditiis ipsum alias, fugit molestias officia. Sit, ipsam placeat. Lorem ipsum dolor sit amet consectetur adipisicing elit. Harum eos esse quas doloribus laboriosam aliquid, dicta quo beatae saepe repudiandae repellat at non nam quidem debitis voluptates hic magni fugit.</div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Chat Form -->
            <form id="chatForm" class="flex space-x-2 justify-center items-center h-12 w-full overflow-hidden" action="{{ route('index.post') }}" method="POST">
                @csrf
                <input id="messageInput" class="w-full h-full text-start rounded-xl p-2 border-2 border-red-200 focus:outline-red-500" type="text" name="message" placeholder="Message Assistant...">
                <button id="sendButton" class="text-slate-200 font-semibold rounded-lg bg-red-800 w-16 h-full focus:outline-none" type="submit">Send</button>
            </form>
        </div>
    </div>

    <script>
        const postUrl = @json(route('index.post'));
    </script>
    
    <script src={{ asset('js/chatbot.js') }}></script>
@endsection