/** Better VTOP Frontend - Clean Implementation */

const API_URL = 'http://localhost:5555/api';
let sessionId = 'auto-' + Date.now();

// Elements
const output = document.getElementById('output');
const outputTitle = document.getElementById('outputTitle');
const outputBody = document.getElementById('outputBody');

// Init
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Better VTOP Loaded');
    
    // Attach handlers
    document.querySelectorAll('.card').forEach(card => {
        const btn = card.querySelector('.btn-exec');
        if (btn) {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                handleClick(card);
            });
        }
    });
    
    console.log('✅ Ready');
});

// Handle card click
async function handleClick(card) {
    const type = card.dataset.type;
    const cmd = card.dataset.cmd;
    const feature = card.dataset.feature;
    const mode = card.dataset.mode;
    const title = card.querySelector('h3').textContent;
    
    console.log('▶', type, feature || cmd);
    
    showOutput(title);
    
    try {
        if (type === 'vtop') {
            await runVTOP(cmd);
        } else if (type === 'ai') {
            await runAI(feature);
        } else if (type === 'gemini') {
            await runGemini(feature, mode);
        }
    } catch (err) {
        showError(err.message);
    }
}

// Run VTOP
async function runVTOP(cmd) {
    const res = await fetch(`${API_URL}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, command: cmd })
    });
    
    const data = await res.json();
    if (data.success) displayOutput(data.output);
    else throw new Error(data.error || 'Failed');
}

// Run AI
async function runAI(feature) {
    // Export
    const exp = await fetch(`${API_URL}/ai-export`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
    });
    
    const expData = await exp.json();
    if (!expData.success) throw new Error(expData.error || 'Export failed');
    
    // Run
    const res = await fetch(`${API_URL}/ai-features`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ai_data: expData.data, feature })
    });
    
    const data = await res.json();
    if (data.success) displayOutput(data.output);
    else throw new Error(data.error || 'AI failed');
}

// Run Gemini
async function runGemini(feature, mode) {
    // Special handling for chatbot - open interactive chat
    if (feature === 'chatbot') {
        showChatInterface();
        return;
    }
    
    // Special handling for voice assistant - show instructions
    if (feature === 'voice') {
        showVoiceInstructions();
        return;
    }
    
    // Export
    const exp = await fetch(`${API_URL}/ai-export`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
    });
    
    const expData = await exp.json();
    if (!expData.success) throw new Error(expData.error || 'Export failed');
    
    // Payload
    const payload = { ai_data: expData.data, feature };
    if (mode) payload.mode = mode;
    
    // Run
    const res = await fetch(`${API_URL}/gemini-features`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    
    const data = await res.json();
    if (data.success) displayOutput(data.output);
    else throw new Error(data.error || 'Gemini failed');
}

// Show output
function showOutput(title) {
    outputTitle.textContent = title;
    outputBody.className = 'panel-body';
    outputBody.innerHTML = '<div class="loading"><div class="spinner"></div><p>EXECUTING...</p></div>';
    output.classList.add('active');
}

// Display
function displayOutput(data) {
    outputBody.className = 'panel-body';
    let content = '';
    
    if (typeof data === 'string') {
        content = data;
    } else if (data && typeof data === 'object') {
        content = data.content || JSON.stringify(data, null, 2);
    } else {
        content = String(data);
    }
    
    outputBody.innerHTML = `<pre>${escape(content)}</pre>`;
}

// Error
function showError(msg) {
    outputBody.className = 'panel-body error';
    outputBody.innerHTML = `<div style="padding:2rem;text-align:center;"><h3 style="margin-bottom:1rem;">❌ ERROR</h3><pre>${escape(msg)}</pre></div>`;
}

// Close
function closeOutput() {
    output.classList.remove('active');
}

// Escape
function escape(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Click outside to close
output.addEventListener('click', (e) => {
    if (e.target === output) closeOutput();
});

// ESC to close
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeOutput();
});

// Chat interface
function showChatInterface() {
    outputTitle.textContent = '💬 AI Chatbot';
    outputBody.className = 'panel-body chat-mode';
    outputBody.innerHTML = `
        <div class="chat-container">
            <div class="chat-messages" id="chatMessages">
                <div class="chat-message bot">
                    <strong>AI:</strong> Hello! I'm your CLI-TOP chatbot with full access to your VTOP data. Ask me anything about your academics!
                </div>
            </div>
            <div class="chat-input-container">
                <input type="text" id="chatInput" placeholder="Ask me anything..." />
                <button id="chatSend" class="btn-exec">Send</button>
            </div>
        </div>
    `;
    output.classList.add('active');
    
    // Setup chat handlers
    const chatInput = document.getElementById('chatInput');
    const chatSend = document.getElementById('chatSend');
    const chatMessages = document.getElementById('chatMessages');
    
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message
        const userMsg = document.createElement('div');
        userMsg.className = 'chat-message user';
        userMsg.innerHTML = `<strong>You:</strong> ${escape(message)}`;
        chatMessages.appendChild(userMsg);
        chatInput.value = '';
        
        // Add loading
        const loadingMsg = document.createElement('div');
        loadingMsg.className = 'chat-message bot loading';
        loadingMsg.innerHTML = '<strong>AI:</strong> <span class="typing">Thinking...</span>';
        chatMessages.appendChild(loadingMsg);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        try {
            // Send to backend
            const exp = await fetch(`${API_URL}/ai-export`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId })
            });
            
            const expData = await exp.json();
            if (!expData.success) throw new Error(expData.error);
            
            // Call chat endpoint
            const res = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ai_data: expData.data, message })
            });
            
            const data = await res.json();
            
            // Remove loading
            loadingMsg.remove();
            
            // Add bot response
            const botMsg = document.createElement('div');
            botMsg.className = 'chat-message bot';
            botMsg.innerHTML = `<strong>AI:</strong> ${escape(data.response || data.error || 'No response')}`;
            chatMessages.appendChild(botMsg);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
        } catch (err) {
            loadingMsg.remove();
            const errorMsg = document.createElement('div');
            errorMsg.className = 'chat-message bot error';
            errorMsg.innerHTML = `<strong>Error:</strong> ${escape(err.message)}`;
            chatMessages.appendChild(errorMsg);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    chatInput.focus();
}

// Voice Assistant - Web-based version
let voiceRecognition = null;
let voiceSynthesis = window.speechSynthesis;
let isListening = false;

function showVoiceInstructions() {
    outputTitle.textContent = '🎙️ Voice Assistant';
    outputBody.className = 'panel-body voice-mode';
    outputBody.innerHTML = `
        <div class="voice-container">
            <div class="voice-status">
                <div class="voice-indicator" id="voiceIndicator">
                    <div class="mic-icon">🎤</div>
                    <div class="status-text" id="statusText">Click "Start Listening" to begin</div>
                </div>
            </div>
            
            <div class="voice-controls">
                <button id="startVoice" class="btn-voice btn-start">🎤 Start Listening</button>
                <button id="stopVoice" class="btn-voice btn-stop" style="display:none;">⏹️ Stop</button>
            </div>
            
            <div class="voice-transcript" id="voiceTranscript">
                <h4>📝 Transcript:</h4>
                <div class="transcript-content" id="transcriptContent">
                    <p class="help-text">Try saying:</p>
                    <ul class="voice-commands">
                        <li>"Can I leave classes?"</li>
                        <li>"How am I doing?"</li>
                        <li>"What should I focus on?"</li>
                        <li>"Show my marks"</li>
                        <li>"Check attendance"</li>
                    </ul>
                </div>
            </div>
            
            <div class="voice-response" id="voiceResponse" style="display:none;">
                <h4>🤖 Response:</h4>
                <div class="response-content" id="responseContent"></div>
            </div>
        </div>
    `;
    output.classList.add('active');
    
    // Initialize Web Speech API
    initVoiceRecognition();
}

function initVoiceRecognition() {
    // Check browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        document.getElementById('statusText').textContent = '❌ Voice recognition not supported in this browser';
        document.getElementById('startVoice').disabled = true;
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    voiceRecognition = new SpeechRecognition();
    
    voiceRecognition.continuous = false;
    voiceRecognition.interimResults = true;
    voiceRecognition.lang = 'en-US';
    
    const startBtn = document.getElementById('startVoice');
    const stopBtn = document.getElementById('stopVoice');
    const indicator = document.getElementById('voiceIndicator');
    const statusText = document.getElementById('statusText');
    const transcriptContent = document.getElementById('transcriptContent');
    const responseDiv = document.getElementById('voiceResponse');
    const responseContent = document.getElementById('responseContent');
    
    // Start listening
    startBtn.addEventListener('click', () => {
        voiceRecognition.start();
        isListening = true;
        startBtn.style.display = 'none';
        stopBtn.style.display = 'inline-block';
        indicator.classList.add('listening');
        statusText.textContent = '🎤 Listening... Speak now!';
        transcriptContent.innerHTML = '<p class="interim">Listening...</p>';
    });
    
    // Stop listening
    stopBtn.addEventListener('click', () => {
        voiceRecognition.stop();
        isListening = false;
        startBtn.style.display = 'inline-block';
        stopBtn.style.display = 'none';
        indicator.classList.remove('listening');
        statusText.textContent = 'Click "Start Listening" to begin';
    });
    
    // Handle results
    voiceRecognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }
        
        if (interimTranscript) {
            transcriptContent.innerHTML = `<p class="interim">${escape(interimTranscript)}</p>`;
        }
        
        if (finalTranscript) {
            transcriptContent.innerHTML = `<p class="final">You said: "${escape(finalTranscript)}"</p>`;
            statusText.textContent = '⏳ Processing...';
            indicator.classList.remove('listening');
            indicator.classList.add('processing');
            
            // Process the command
            processVoiceCommand(finalTranscript, responseDiv, responseContent, indicator, statusText, startBtn, stopBtn);
        }
    };
    
    // Handle errors
    voiceRecognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        isListening = false;
        startBtn.style.display = 'inline-block';
        stopBtn.style.display = 'none';
        indicator.classList.remove('listening', 'processing');
        
        if (event.error === 'no-speech') {
            statusText.textContent = '❌ No speech detected. Try again!';
        } else if (event.error === 'not-allowed') {
            statusText.textContent = '❌ Microphone access denied';
        } else {
            statusText.textContent = `❌ Error: ${event.error}`;
        }
    };
    
    // Handle end
    voiceRecognition.onend = () => {
        if (isListening) {
            // Restart if manually stopped
            isListening = false;
            startBtn.style.display = 'inline-block';
            stopBtn.style.display = 'none';
            indicator.classList.remove('listening');
        }
    };
}

async function processVoiceCommand(command, responseDiv, responseContent, indicator, statusText, startBtn, stopBtn) {
    try {
        const commandLower = command.toLowerCase();
        
        // Parse smart commands
        let action = null;
        
        if (commandLower.includes('can i leave') || commandLower.includes('should i skip') || commandLower.includes('can i skip')) {
            action = { type: 'smart', name: 'attendance_advice' };
        } else if (commandLower.includes('how am i doing') || commandLower.includes('am i doing well')) {
            action = { type: 'smart', name: 'performance_overview' };
        } else if (commandLower.includes('what should i focus') || commandLower.includes('what to study')) {
            action = { type: 'smart', name: 'focus_advisor' };
        } else if (commandLower.includes('will i pass') || commandLower.includes('exam ready')) {
            action = { type: 'smart', name: 'exam_prediction' };
        } else if (commandLower.includes('marks') || commandLower.includes('score')) {
            action = { type: 'vtop', cmd: 'marks view' };
        } else if (commandLower.includes('attendance')) {
            action = { type: 'vtop', cmd: 'attendance calculator' };
        } else if (commandLower.includes('grade')) {
            action = { type: 'vtop', cmd: 'grades view' };
        } else if (commandLower.includes('cgpa')) {
            action = { type: 'vtop', cmd: 'cgpa view' };
        } else if (commandLower.includes('run all ai')) {
            action = { type: 'ai', feature: 'all' };
        } else {
            // Default to chat
            action = { type: 'chat', message: command };
        }
        
        // Execute action
        let result;
        if (action.type === 'smart') {
            result = await executeSmartCommand(action.name);
        } else if (action.type === 'vtop') {
            result = await executeVTOPCommand(action.cmd);
        } else if (action.type === 'ai') {
            result = await executeAIFeature(action.feature);
        } else if (action.type === 'chat') {
            result = await executeChatCommand(action.message);
        }
        
        // Display result
        responseDiv.style.display = 'block';
        responseContent.innerHTML = `<pre>${escape(result)}</pre>`;
        
        // Speak response (first 200 chars)
        const summary = result.substring(0, 200).replace(/[^\w\s.,!?]/g, '');
        speak(summary);
        
        // Update UI
        indicator.classList.remove('processing');
        statusText.textContent = '✅ Complete! Say something else or click Start Listening';
        startBtn.style.display = 'inline-block';
        stopBtn.style.display = 'none';
        
    } catch (error) {
        responseDiv.style.display = 'block';
        responseContent.innerHTML = `<p class="error">❌ Error: ${escape(error.message)}</p>`;
        indicator.classList.remove('processing');
        statusText.textContent = '❌ Error occurred. Try again!';
        startBtn.style.display = 'inline-block';
        stopBtn.style.display = 'none';
        
        speak('An error occurred. Please try again.');
    }
}

async function executeSmartCommand(smartType) {
    // Export data first
    const exp = await fetch(`${API_URL}/ai-export`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
    });
    
    const expData = await exp.json();
    if (!expData.success) throw new Error(expData.error);
    
    // Call smart command endpoint
    const res = await fetch(`${API_URL}/smart-command`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ai_data: expData.data, smart_type: smartType })
    });
    
    const data = await res.json();
    if (!data.success) throw new Error(data.error);
    
    return typeof data.output === 'object' ? data.output.content : data.output;
}

async function executeVTOPCommand(cmd) {
    const res = await fetch(`${API_URL}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, command: cmd })
    });
    
    const data = await res.json();
    if (!data.success) throw new Error(data.error);
    
    return typeof data.output === 'object' ? data.output.content : data.output;
}

async function executeAIFeature(feature) {
    const exp = await fetch(`${API_URL}/ai-export`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
    });
    
    const expData = await exp.json();
    if (!expData.success) throw new Error(expData.error);
    
    const res = await fetch(`${API_URL}/ai-features`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ai_data: expData.data, feature })
    });
    
    const data = await res.json();
    if (!data.success) throw new Error(data.error);
    
    return typeof data.output === 'object' ? data.output.content : data.output;
}

async function executeChatCommand(message) {
    const exp = await fetch(`${API_URL}/ai-export`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
    });
    
    const expData = await exp.json();
    if (!expData.success) throw new Error(expData.error);
    
    const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ai_data: expData.data, message })
    });
    
    const data = await res.json();
    if (!data.success) throw new Error(data.error);
    
    return data.response || 'No response';
}

function speak(text) {
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        speechSynthesis.speak(utterance);
    }
}

console.log('%c╔══════════════════════════════════════╗\n║   BETTER VTOP v2.0                ║\n║   Neo-Brutalism + AI + Gemini     ║\n╚══════════════════════════════════════╝', 'color:#FF6B9D;font-weight:bold;font-size:14px;');
