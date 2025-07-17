// TEC Persona Integration for Chat Interface
class PersonaChatIntegration {
    constructor() {
        this.currentPersona = null;
        this.currentAiSettings = null;
        this.init();
    }
    
    init() {
        this.loadCurrentPersona();
        this.loadCurrentAiSettings();
        this.setupPersonaButtons();
        this.setupEnhancedChatMode();
    }
    
    setupPersonaButtons() {
        // Add persona buttons to existing UI
        this.addPersonaButtonsToUI();
        
        // Setup event listeners for persona switching
        this.setupPersonaSwitching();
    }
    
    addPersonaButtonsToUI() {
        // Check if buttons already exist
        if (document.getElementById('personaControlsContainer')) {
            return;
        }
        
        // Find the chat controls container
        const chatControls = document.querySelector('.chat-controls') || 
                           document.querySelector('#chatControls') ||
                           document.querySelector('.message-input-container');
        
        if (!chatControls) {
            console.warn('Chat controls container not found');
            return;
        }
        
        // Create persona controls container
        const personaControlsHTML = `
            <div id="personaControlsContainer" class="persona-controls-container mb-4">
                <div class="flex flex-wrap gap-2 items-center">
                    <button id="showPersonaPanelBtn" class="persona-quick-button" title="Configure Your Persona">
                        <i class="fas fa-user-circle mr-2"></i>
                        <span class="persona-btn-text">Your Persona</span>
                    </button>
                    <button id="showAiSettingsPanelBtn" class="persona-quick-button" title="AI Settings">
                        <i class="fas fa-cog mr-2"></i>
                        <span class="persona-btn-text">AI Settings</span>
                    </button>
                    <div class="persona-status-indicator" id="personaStatusIndicator">
                        <i class="fas fa-circle text-gray-500"></i>
                        <span id="personaStatusText">Default Mode</span>
                    </div>
                </div>
            </div>
        `;
        
        // Insert before chat controls
        chatControls.insertAdjacentHTML('beforebegin', personaControlsHTML);
        
        // Bind events
        document.getElementById('showPersonaPanelBtn').addEventListener('click', () => {
            window.showPlayerPersonaPanel();
        });
        
        document.getElementById('showAiSettingsPanelBtn').addEventListener('click', () => {
            window.showAiSettingsPanel();
        });
    }
    
    setupPersonaSwitching() {
        // Listen for persona changes
        document.addEventListener('personaChanged', (event) => {
            this.handlePersonaChange(event.detail);
        });
        
        document.addEventListener('aiSettingsChanged', (event) => {
            this.handleAiSettingsChange(event.detail);
        });
    }
    
    setupEnhancedChatMode() {
        // Override the existing sendMessage function to include persona context
        const originalSendMessage = window.sendMessage;
        if (originalSendMessage) {
            window.sendMessage = async (message) => {
                return this.sendEnhancedMessage(message, originalSendMessage);
            };
        }
        
        // Setup persona-aware message processing
        this.setupPersonaAwareMessaging();
    }
    
    async sendEnhancedMessage(message, originalSendMessage) {
        try {
            // Check if persona mode is enabled
            if (this.currentPersona && this.currentAiSettings) {
                // Use enhanced message processing
                const response = await fetch('/api/chat/enhanced', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('tec_auth_token')}`
                    },
                    body: JSON.stringify({
                        message: message,
                        use_persona: true,
                        persona_context: this.currentPersona,
                        ai_settings: this.currentAiSettings
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    return data.response;
                }
            }
            
            // Fallback to original message processing
            return originalSendMessage(message);
        } catch (error) {
            console.error('Enhanced message error:', error);
            return originalSendMessage(message);
        }
    }
    
    setupPersonaAwareMessaging() {
        // Add persona context to message display
        const originalDisplayMessage = window.displayMessage;
        if (originalDisplayMessage) {
            window.displayMessage = (message, sender, isUser) => {
                if (!isUser && this.currentPersona) {
                    // Add persona styling to AI messages
                    const personaMessage = this.enhanceAiMessage(message);
                    return originalDisplayMessage(personaMessage, sender, isUser);
                }
                return originalDisplayMessage(message, sender, isUser);
            };
        }
    }
    
    enhanceAiMessage(message) {
        // Add persona-specific formatting or context
        if (this.currentPersona?.persona_settings?.opening) {
            // Check if this is the first message in conversation
            const chatHistory = document.getElementById('chatHistory');
            if (chatHistory && chatHistory.children.length === 0) {
                return `${this.currentPersona.persona_settings.opening}\n\n${message}`;
            }
        }
        return message;
    }
    
    async loadCurrentPersona() {
        try {
            const response = await fetch('/api/persona/player', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('tec_auth_token')}`
                }
            });
            
            if (response.ok) {
                this.currentPersona = await response.json();
                this.updatePersonaStatus();
            }
        } catch (error) {
            console.error('Error loading persona:', error);
        }
    }
    
    async loadCurrentAiSettings() {
        try {
            const response = await fetch('/api/ai/settings', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('tec_auth_token')}`
                }
            });
            
            if (response.ok) {
                this.currentAiSettings = await response.json();
                this.updatePersonaStatus();
            }
        } catch (error) {
            console.error('Error loading AI settings:', error);
        }
    }
    
    updatePersonaStatus() {
        const statusIndicator = document.getElementById('personaStatusIndicator');
        const statusText = document.getElementById('personaStatusText');
        
        if (!statusIndicator || !statusText) return;
        
        if (this.currentPersona && this.currentAiSettings) {
            const persona = this.currentPersona.persona_settings;
            const aiPersona = this.currentAiSettings.persona_active || 'airth';
            
            statusIndicator.innerHTML = '<i class="fas fa-circle text-green-500"></i>';
            statusText.textContent = `${persona.title || 'Your Persona'} + ${aiPersona}`;
            statusText.title = `Persona: ${persona.title || 'Unnamed'} | AI: ${aiPersona} | Creativity: ${this.currentAiSettings.creativity_level || 0.7}`;
        } else {
            statusIndicator.innerHTML = '<i class="fas fa-circle text-gray-500"></i>';
            statusText.textContent = 'Default Mode';
            statusText.title = 'No persona active';
        }
    }
    
    handlePersonaChange(personaData) {
        this.currentPersona = personaData;
        this.updatePersonaStatus();
        
        // Emit custom event for other components
        document.dispatchEvent(new CustomEvent('tecPersonaUpdated', {
            detail: { persona: personaData }
        }));
    }
    
    handleAiSettingsChange(settingsData) {
        this.currentAiSettings = settingsData;
        this.updatePersonaStatus();
        
        // Emit custom event for other components
        document.dispatchEvent(new CustomEvent('tecAiSettingsUpdated', {
            detail: { settings: settingsData }
        }));
    }
    
    // Method to generate persona-aware prompts
    async generatePersonaPrompt(type, content) {
        try {
            const response = await fetch(`/api/prompt/${type}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('tec_auth_token')}`
                },
                body: JSON.stringify({
                    content: content,
                    use_persona: true
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                return data.prompt;
            }
        } catch (error) {
            console.error('Error generating persona prompt:', error);
        }
        return null;
    }
    
    // Method to get character lore for context
    async getCharacterLore(characterName) {
        try {
            const response = await fetch(`/api/lore/character/${characterName}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('tec_auth_token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                return data.lore;
            }
        } catch (error) {
            console.error('Error getting character lore:', error);
        }
        return null;
    }
    
    // Method to save conversation memory
    async saveConversationMemory(message, response) {
        try {
            await fetch('/api/memory/conversation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('tec_auth_token')}`
                },
                body: JSON.stringify({
                    user_message: message,
                    ai_response: response,
                    timestamp: new Date().toISOString()
                })
            });
        } catch (error) {
            console.error('Error saving conversation memory:', error);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for other components to load
    setTimeout(() => {
        window.personaChatIntegration = new PersonaChatIntegration();
    }, 1000);
});

// Add CSS for persona controls
const personaControlsCSS = `
<style>
.persona-controls-container {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(249, 115, 22, 0.3);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 16px;
}

.persona-quick-button {
    background: linear-gradient(135deg, rgba(249, 115, 22, 0.8) 0%, rgba(234, 88, 12, 0.8) 100%);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
}

.persona-quick-button:hover {
    background: linear-gradient(135deg, rgba(249, 115, 22, 1) 0%, rgba(234, 88, 12, 1) 100%);
    transform: translateY(-1px);
}

.persona-status-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #d1d5db;
    margin-left: auto;
}

.persona-btn-text {
    font-weight: 500;
}

@media (max-width: 640px) {
    .persona-quick-button .persona-btn-text {
        display: none;
    }
}
</style>
`;

// Inject CSS
document.head.insertAdjacentHTML('beforeend', personaControlsCSS);
