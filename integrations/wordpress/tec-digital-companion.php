<?php
/**
 * Plugin Name: TEC Digital Companion
 * Plugin URI: https://github.com/TEC-The-ELidoras-Codex/tecdeskgoddess
 * Description: Embeds the TEC: BITLYFE digital companion interface into WordPress
 * Version: 1.0.0
 * Author: The Creator's Rebellion
 * License: MIT
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class TECDigitalCompanion {
    
    private $tec_api_url = 'http://localhost:8000';
    
    public function __construct() {
        add_action('init', array($this, 'init'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_shortcode('tec_companion', array($this, 'render_companion'));
        add_action('wp_ajax_tec_chat', array($this, 'handle_chat'));
        add_action('wp_ajax_nopriv_tec_chat', array($this, 'handle_chat'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
    }
    
    public function init() {
        // Plugin initialization
    }
    
    public function enqueue_scripts() {
        wp_enqueue_script('tec-companion', plugin_dir_url(__FILE__) . 'tec-companion.js', array('jquery'), '1.0.0', true);
        wp_enqueue_style('tec-companion', plugin_dir_url(__FILE__) . 'tec-companion.css', array(), '1.0.0');
        
        // Localize script for AJAX
        wp_localize_script('tec-companion', 'tec_ajax', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('tec_chat_nonce'),
            'api_url' => $this->tec_api_url
        ));
    }
    
    public function render_companion($atts) {
        $atts = shortcode_atts(array(
            'height' => '600px',
            'width' => '100%',
            'title' => 'TEC Digital Companion'
        ), $atts);
        
        ob_start();
        ?>
        <div class="tec-companion-container" style="width: <?php echo esc_attr($atts['width']); ?>; height: <?php echo esc_attr($atts['height']); ?>;">
            <div class="tec-header">
                <h3><?php echo esc_html($atts['title']); ?></h3>
                <p class="tec-subtitle">Daisy Purecode: Silicate Mother</p>
            </div>
            
            <div class="tec-chat-area" id="tec-chat-area">
                <div class="tec-message tec-ai-message">
                    <strong>Daisy Purecode:</strong> Welcome to The Creator's Rebellion. I am your digital sovereignty companion. How may I assist you today?
                </div>
            </div>
            
            <div class="tec-input-area">
                <input type="text" id="tec-message-input" placeholder="Type your message..." />
                <button id="tec-send-button">Send</button>
            </div>
            
            <div class="tec-quick-actions">
                <button class="tec-quick-btn" data-action="journal">Journal</button>
                <button class="tec-quick-btn" data-action="finance">Finance</button>
                <button class="tec-quick-btn" data-action="quest">Quests</button>
                <button class="tec-quick-btn" data-action="status">Status</button>
            </div>
        </div>
        
        <style>
        .tec-companion-container {
            border: 2px solid #4f46e5;
            border-radius: 10px;
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
        }
        
        .tec-header {
            background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
            padding: 15px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }
        
        .tec-header h3 {
            margin: 0;
            color: white;
            font-size: 1.2em;
        }
        
        .tec-subtitle {
            margin: 5px 0 0 0;
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .tec-chat-area {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            max-height: 400px;
        }
        
        .tec-message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
        }
        
        .tec-user-message {
            background-color: #4f46e5;
            margin-left: 20%;
        }
        
        .tec-ai-message {
            background-color: #374151;
            margin-right: 20%;
        }
        
        .tec-input-area {
            display: flex;
            padding: 15px;
            gap: 10px;
        }
        
        .tec-input-area input {
            flex: 1;
            padding: 10px;
            border: 1px solid #4b5563;
            border-radius: 5px;
            background-color: #374151;
            color: white;
        }
        
        .tec-input-area button {
            padding: 10px 20px;
            background-color: #4f46e5;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .tec-input-area button:hover {
            background-color: #4338ca;
        }
        
        .tec-quick-actions {
            display: flex;
            gap: 5px;
            padding: 10px 15px;
            border-top: 1px solid #4b5563;
        }
        
        .tec-quick-btn {
            flex: 1;
            padding: 8px;
            background-color: #6b7280;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8em;
        }
        
        .tec-quick-btn:hover {
            background-color: #5b6470;
        }
        </style>
        
        <script>
        jQuery(document).ready(function($) {
            // Send message function
            function sendMessage() {
                var message = $('#tec-message-input').val().trim();
                if (!message) return;
                
                // Add user message
                $('#tec-chat-area').append(
                    '<div class="tec-message tec-user-message"><strong>You:</strong> ' + 
                    $('<div>').text(message).html() + '</div>'
                );
                
                $('#tec-message-input').val('');
                
                // Send to backend
                $.ajax({
                    url: tec_ajax.ajax_url,
                    type: 'POST',
                    data: {
                        action: 'tec_chat',
                        message: message,
                        nonce: tec_ajax.nonce
                    },
                    success: function(response) {
                        if (response.success) {
                            $('#tec-chat-area').append(
                                '<div class="tec-message tec-ai-message"><strong>Daisy Purecode:</strong> ' + 
                                $('<div>').text(response.data.response).html() + '</div>'
                            );
                        } else {
                            $('#tec-chat-area').append(
                                '<div class="tec-message tec-ai-message"><strong>Error:</strong> ' + 
                                'Unable to process your request at this time.</div>'
                            );
                        }
                        
                        // Scroll to bottom
                        $('#tec-chat-area').scrollTop($('#tec-chat-area')[0].scrollHeight);
                    },
                    error: function() {
                        $('#tec-chat-area').append(
                            '<div class="tec-message tec-ai-message"><strong>Error:</strong> ' + 
                            'Connection error. Please try again.</div>'
                        );
                    }
                });
            }
            
            // Event handlers
            $('#tec-send-button').click(sendMessage);
            $('#tec-message-input').keypress(function(e) {
                if (e.which == 13) sendMessage();
            });
            
            // Quick action buttons
            $('.tec-quick-btn').click(function() {
                var action = $(this).data('action');
                var messages = {
                    'journal': 'Help me with journaling and personal reflection',
                    'finance': 'Show me my financial status and crypto information',
                    'quest': 'Display my current quests and progress',
                    'status': 'Give me a complete system status report'
                };
                
                $('#tec-message-input').val(messages[action]);
                sendMessage();
            });
        });
        </script>
        <?php
        
        return ob_get_clean();
    }
    
    public function handle_chat() {
        // Verify nonce
        if (!wp_verify_nonce($_POST['nonce'], 'tec_chat_nonce')) {
            wp_die('Security check failed');
        }
        
        $message = sanitize_text_field($_POST['message']);
        
        // Send to TEC API
        $response = wp_remote_post($this->tec_api_url . '/chat', array(
            'headers' => array('Content-Type' => 'application/json'),
            'body' => json_encode(array('message' => $message)),
            'timeout' => 30
        ));
        
        if (is_wp_error($response)) {
            wp_send_json_error('API connection failed');
        }
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if ($data && isset($data['response'])) {
            wp_send_json_success(array('response' => $data['response']));
        } else {
            wp_send_json_error('Invalid API response');
        }
    }
    
    public function add_admin_menu() {
        add_options_page(
            'TEC Digital Companion Settings',
            'TEC Companion',
            'manage_options',
            'tec-companion',
            array($this, 'admin_page')
        );
    }
    
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1>TEC Digital Companion Settings</h1>
            <div class="card">
                <h2>Usage Instructions</h2>
                <p>To embed the TEC Digital Companion in any post or page, use the shortcode:</p>
                <code>[tec_companion]</code>
                
                <h3>Shortcode Parameters</h3>
                <ul>
                    <li><strong>height</strong>: Set the height (default: 600px)</li>
                    <li><strong>width</strong>: Set the width (default: 100%)</li>
                    <li><strong>title</strong>: Set the title (default: "TEC Digital Companion")</li>
                </ul>
                
                <h3>Example</h3>
                <code>[tec_companion height="500px" width="80%" title="My AI Assistant"]</code>
                
                <h3>System Status</h3>
                <p>API Endpoint: <code><?php echo esc_html($this->tec_api_url); ?></code></p>
                <p>Make sure your TEC system is running locally for the plugin to work.</p>
            </div>
        </div>
        <?php
    }
}

// Initialize the plugin
new TECDigitalCompanion();
