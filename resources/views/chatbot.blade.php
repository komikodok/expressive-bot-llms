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
            <header class="flex w-full h-12 items-center justify-center shadow-md">
                <p class="text-Black text-lg font-semibold opacity-85">Assistant</p>
                <button class="ml-2 rounded-full">⚙</button>
            </header>
            <!-- Body -->
            <div class="h-5/6 w-full flex p-2.5 justify-center items-center overflow-hidden">
                <div class="border-t-2 border-opacity-10 border-gray-400 shadow-lg shadow-gray-400 rounded-2xl h-full w-full p-2">
                    <!-- Ballon's Chat -->   
                    <div id="chatContainer" class="space-y-1 p-4 h-full overflow-y-scroll flex flex-col" style="scrollbar-width:none;">
                        <!-- User Message -->
                        <div class="self-end p-3 max-w-[70%] gap-2">
                            <div class="border border-black w-14 h-14 rounded-full"></div>
                            <div class="bg-gray-200 rounded-xl p-3 m-auto max-w-full break-words">aaaaasaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</div>
                        </div>
                        <!-- Assistant Message -->
                        <div class="self-start p-3 max-w-[70%] gap-2">
                            <div class="border border-black w-14 h-14 rounded-full"></div>
                            <div class="bg-gray-200 rounded-xl p-3 m-auto max-w-full break-words">aaaaasaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Chat Form -->
            <div class="shadow-xl flex justify-center items-centers w-full">
                <form id="chatForm" class="flex space-x-2 justify-center items-center h-12 w-full" action="{{ route('index.post') }}" method="POST">
                    @csrf
                    <input id="messageInput" class="w-full h-full focus:outline-none text-start shadow-md rounded-l-xl p-2" type="text" name="message" placeholder="Message Assistant...">
                    <button class="text-slate-800 rounded-r-lg border border-black w-16 h-full" type="submit">Send</button>
                </form>
            </div>
        </div>
    </div>

    <script>
        const postUrl = @json(route('index.post'));
    </script>
    
    <script src={{ asset('js/chatbot.js') }}></script>
@endsection