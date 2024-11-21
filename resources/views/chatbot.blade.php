@extends('layouts.app')

@section('title', 'Laravel')
    
@section('content')
    <!-- Container -->
    <div class="flex border border-black h-screen overflow-hidden">
        <!-- Side Bar -->
        <div class="border border-green-400 bg-slate-400 w-96 h-full max-md:!w-0 transition-all duration-500 overflow-hidden">
            <div class="border border-yellow-400 w-full h-full"></div>
        </div>
        <!-- Chatbot -->
        <div class="border border-blue-400 bg-slate-300 w-full h-full">
            <!-- Header -->
            <header class="border border-red-500 flex w-full h-12 items-center justify-center">
                <p class="text-slate-950">Chat with assistant</p>
                <button class="ml-2 rounded-full">⚙</button>
            </header>
            <!-- Body -->
            <div class="border border-purple-950 h-5/6 w-full flex p-2.5 justify-center items-center overflow-hidden">
                <div class="border border-gray-800 rounded-md h-full w-full">
                    <!-- Ballon's Chat -->   
                    <div id="chatContainer" class="space-y-4 p-4 overflow-y-scroll h-full flex flex-col" style="scrollbar-width:none;">
                        <!-- Contoh balon pesan pengguna -->
                        <div class="self-end border border-blue-500 flex p-3 max-w-[70%] shadow-md">
                            <div>User :</div>
                            <div>Halo</div>
                        </div>
                        <!-- Contoh balon pesan bot -->
                        <div class="self-start border border-gray-500 flex p-3 max-w-[70%] shadow-md">
                            <div>Bot :</div>
                            <div>Halo</div>
                        </div>
                    </div>
                </div>  
            </div>
            <!-- Chat Form -->
            <div class="border border-sky-950 flex justify-center items-center w-full">
                <form id="chatForm" class="border border-green-600 flex space-x-2 justify-center items-center h-full w-full" action="{{ route('index.post') }}" method="POST">
                    @csrf
                    <input id="messageInput" class="w-full h-9 text-start rounded-md p-2" type="text" name="message" placeholder="Message Assistant">
                    <button class="text-slate-800 rounded-md" type="submit">Button</button>
                </form>
            </div>
        </div>
    </div>

    <script>
        const postUrl = @json(route('index.post'));
    </script>
    
    <script src={{ asset('js/chatbot.js') }}></script>
@endsection