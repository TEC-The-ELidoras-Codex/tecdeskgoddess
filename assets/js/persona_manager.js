// TEC Persona Management JavaScript
class PersonaManager {
    constructor() {
        this.apiBaseUrl = '/api';
        this.authToken = localStorage.getItem('tec_auth_token');
        this.init();
    }
    
    init() {
        this.bindEventListeners();
        this.setupAudioControls();
        this.setupSliders();
    }
    
    bindEventListeners() {
        // Panel visibility
        document.getElementById('closePersonaPanel')?.addEventListener('click', () => {
            this.hidePersonaPanel();
        });
        
        document.getElementById('closeAiSettingsPanel')?.addEventListener('click', () => {
            this.hideAiSettingsPanel();
        });
        
        // Form submissions
        document.getElementById('personaForm')?.addEventListener('submit', (e) => {
            this.handlePersonaSubmit(e);
        });
        
        document.getElementById('aiSettingsForm')?.addEventListener('submit', (e) => {
            this.handleAiSettingsSubmit(e);
        });
        
        // Load buttons
        document.getElementById('loadPersonaButton')?.addEventListener('click', () => {
            this.loadPlayerPersona();
        });
        
        document.getElementById('loadAiSettingsButton')?.addEventListener('click', () => {
            this.loadAiSettings();
        });
        
        // Reset button
        document.getElementById('resetPersonaButton')?.addEventListener('click', () => {
            this.resetPersonaForm();
        });
    }
    
    setupAudioControls() {
        const audioPlayer = document.getElementById('backgroundAudioPlayer');
        const playButton = document.getElementById('playAudioButton');
        const stopButton = document.getElementById('stopAudioButton');
        const audioStatus = document.getElementById('audioStatus');
        
        if (playButton && stopButton && audioPlayer) {
            playButton.addEventListener('click', () => {
                const audioUrl = document.getElementById('backgroundAudioUrl').value;
                if (audioUrl) {
                    audioPlayer.src = audioUrl;
                    audioPlayer.play().then(() => {
                        audioStatus.textContent = 'Playing...';
                        playButton.disabled = true;
                    }).catch(error => {
                        this.showPersonaMessage('Error playing audio: ' + error.message, 'error');
                    });
                } else {
                    this.showPersonaMessage('Please enter an audio URL first', 'error');
                }
            });
            
            stopButton.addEventListener('click', () => {
                audioPlayer.pause();
                audioPlayer.currentTime = 0;
                audioStatus.textContent = 'Stopped';
                playButton.disabled = false;
            });
        }
    }
    
    setupSliders() {
        const creativitySlider = document.getElementById('creativityLevel');
        const creativityValue = document.getElementById('creativityValue');
        
        if (creativitySlider && creativityValue) {
            creativitySlider.addEventListener('input', function() {
                creativityValue.textContent = this.value;
            });
        }
    }
    
    // Panel Management
    showPersonaPanel() {
        const panel = document.getElementById('playerPersonaPanel');
        if (panel) {
            panel.classList.remove('hidden');
            this.loadPlayerPersona();
        }
    }
    
    hidePersonaPanel() {
        const panel = document.getElementById('playerPersonaPanel');
        if (panel) {
            panel.classList.add('hidden');
        }
    }
    
    showAiSettingsPanel() {
        const panel = document.getElementById('aiSettingsPanel');
        if (panel) {
            panel.classList.remove('hidden');
            this.loadAiSettings();
        }
    }
    
    hideAiSettingsPanel() {
        const panel = document.getElementById('aiSettingsPanel');
        if (panel) {
            panel.classList.add('hidden');
        }
    }
    
    // Form Handlers
    async handlePersonaSubmit(e) {
        e.preventDefault();
        
        const personaData = {
            persona_settings: {
                title: document.getElementById('personaTitle').value,
                intro: document.getElementById('personaIntro').value,
                opening: document.getElementById('personaOpening').value,
                tags: document.getElementById('personaTags').value
                    .split(',')
                    .map(tag => tag.trim())
                    .filter(tag => tag),
                appearance_notes: {
                    body_type: document.getElementById('appearanceBodyType').value,
                    age_appearance: document.getElementById('appearanceAge').value,
                    hair: document.getElementById('appearanceHair').value,
                    facial_features: document.getElementById('appearanceFacialFeatures').value,
                    attire: document.getElementById('appearanceAttire').value
                },
                background_audio_url: document.getElementById('backgroundAudioUrl').value,
                permission: document.querySelector('input[name="permission"]:checked')?.value || 'private'
            },
            player_persona_notes: document.getElementById('playerPersonaNotes').value
        };
        
        try {
            const response = await this.apiRequest('/persona/player', 'POST', personaData);
            
            if (response.ok) {
                this.showPersonaMessage('Player persona saved successfully!', 'success');
            } else {
                const error = await response.json();
                this.showPersonaMessage(error.error || 'Failed to save persona', 'error');
            }
        } catch (error) {
            this.showPersonaMessage('Network error: ' + error.message, 'error');
        }
    }
    
    async handleAiSettingsSubmit(e) {
        e.preventDefault();
        
        const aiSettings = {
            persona_active: document.getElementById('activePersona').value,
            creativity_level: parseFloat(document.getElementById('creativityLevel').value),
            memory_length: document.getElementById('memoryLength').value,
            reasoning_mode: document.getElementById('reasoningMode').checked,
            voice_enabled: document.getElementById('voiceEnabled').checked
        };
        
        try {
            const response = await this.apiRequest('/ai/settings', 'POST', aiSettings);
            
            if (response.ok) {
                this.showAiSettingsMessage('AI settings saved successfully!', 'success');
            } else {
                const error = await response.json();
                this.showAiSettingsMessage(error.error || 'Failed to save settings', 'error');
            }
        } catch (error) {
            this.showAiSettingsMessage('Network error: ' + error.message, 'error');
        }
    }
    
    // Data Loading
    async loadPlayerPersona() {
        try {
            const response = await this.apiRequest('/persona/player', 'GET');
            
            if (response.ok) {
                const persona = await response.json();
                this.populatePersonaForm(persona);
            }
        } catch (error) {
            console.error('Error loading persona:', error);
        }
    }
    
    async loadAiSettings() {
        try {
            const response = await this.apiRequest('/ai/settings', 'GET');
            
            if (response.ok) {
                const settings = await response.json();
                this.populateAiSettingsForm(settings);
            }
        } catch (error) {
            console.error('Error loading AI settings:', error);
        }
    }
    
    // Form Population
    populatePersonaForm(persona) {
        const settings = persona.persona_settings || {};
        
        document.getElementById('personaTitle').value = settings.title || '';
        document.getElementById('personaIntro').value = settings.intro || '';
        document.getElementById('personaOpening').value = settings.opening || '';
        document.getElementById('personaTags').value = settings.tags ? settings.tags.join(', ') : '';
        document.getElementById('appearanceBodyType').value = settings.appearance_notes?.body_type || '';
        document.getElementById('appearanceAge').value = settings.appearance_notes?.age_appearance || '';
        document.getElementById('appearanceHair').value = settings.appearance_notes?.hair || '';
        document.getElementById('appearanceFacialFeatures').value = settings.appearance_notes?.facial_features || '';
        document.getElementById('appearanceAttire').value = settings.appearance_notes?.attire || '';
        document.getElementById('backgroundAudioUrl').value = settings.background_audio_url || '';
        document.getElementById('playerPersonaNotes').value = persona.player_persona_notes || '';
        
        // Set permission radio button
        const permissionRadio = document.querySelector(`input[name="permission"][value="${settings.permission || 'private'}"]`);
        if (permissionRadio) {
            permissionRadio.checked = true;
        }
    }
    
    populateAiSettingsForm(settings) {
        document.getElementById('activePersona').value = settings.persona_active || 'airth';
        document.getElementById('creativityLevel').value = settings.creativity_level || 0.7;
        document.getElementById('creativityValue').textContent = settings.creativity_level || 0.7;
        document.getElementById('memoryLength').value = settings.memory_length || 'default';
        document.getElementById('reasoningMode').checked = settings.reasoning_mode || false;
        document.getElementById('voiceEnabled').checked = settings.voice_enabled || false;
    }
    
    // Utility Methods
    async apiRequest(endpoint, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.authToken}`
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        return fetch(this.apiBaseUrl + endpoint, options);
    }
    
    resetPersonaForm() {
        if (confirm('Are you sure you want to reset all persona data?')) {
            document.getElementById('personaForm').reset();
            document.getElementById('permissionPrivate').checked = true;
        }
    }
    
    // Message Display
    showPersonaMessage(message, type) {
        this.showMessage('persona', message, type);
    }
    
    showAiSettingsMessage(message, type) {
        this.showMessage('aiSettings', message, type);
    }
    
    showMessage(context, message, type) {
        const messagesDiv = document.getElementById(`${context}StatusMessages`);
        const successDiv = document.getElementById(`${context}SuccessMessage`);
        const errorDiv = document.getElementById(`${context}ErrorMessage`);
        
        if (!messagesDiv || !successDiv || !errorDiv) return;
        
        messagesDiv.classList.remove('hidden');
        
        if (type === 'success') {
            successDiv.classList.remove('hidden');
            errorDiv.classList.add('hidden');
            document.getElementById(`${context}SuccessText`).textContent = message;
        } else {
            errorDiv.classList.remove('hidden');
            successDiv.classList.add('hidden');
            document.getElementById(`${context}ErrorText`).textContent = message;
        }
        
        setTimeout(() => {
            messagesDiv.classList.add('hidden');
        }, 5000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.personaManager = new PersonaManager();
    
    // Expose global functions for external use
    window.showPlayerPersonaPanel = () => window.personaManager.showPersonaPanel();
    window.showAiSettingsPanel = () => window.personaManager.showAiSettingsPanel();
});
