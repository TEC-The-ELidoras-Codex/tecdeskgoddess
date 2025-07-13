# TEC Digital Companion - WordPress Integration

## Overview
This WordPress plugin allows you to embed the TEC: BITLYFE digital companion interface directly into your WordPress website.

## Installation

### Method 1: Manual Installation
1. Copy the `tec-digital-companion.php` file to your WordPress plugins directory:
   - Usually located at: `/wp-content/plugins/`
   - Create a new folder: `/wp-content/plugins/tec-digital-companion/`
   - Place the PHP file inside this folder

2. Log into your WordPress admin panel
3. Go to **Plugins > Installed Plugins**
4. Find "TEC Digital Companion" and click **Activate**

### Method 2: Upload via WordPress Admin
1. Go to **Plugins > Add New** in your WordPress admin
2. Click **Upload Plugin**
3. Choose the `tec-digital-companion.php` file
4. Click **Install Now** and then **Activate**

## Usage

### Basic Shortcode
Add this shortcode to any post or page where you want the TEC companion to appear:

```
[tec_companion]
```

### Advanced Usage
Customize the appearance with parameters:

```
[tec_companion height="500px" width="80%" title="My AI Assistant"]
```

### Parameters
- **height**: Set the height of the interface (default: 600px)
- **width**: Set the width of the interface (default: 100%)
- **title**: Customize the title shown in the header

## Prerequisites

### 1. TEC System Running
Make sure your TEC system is running locally:

```bash
cd /path/to/tecdeskgoddess
python tec_simple_startup.py
```

The system should be accessible at `http://localhost:8000`

### 2. Local Development Setup
If your WordPress site is running on a different domain than localhost, you may need to:

1. Configure CORS settings in the TEC API
2. Update the API URL in the plugin settings
3. Ensure network connectivity between WordPress and the TEC system

## Features

### Chat Interface
- Real-time chat with Daisy Purecode
- Support for journal, finance, quest, and status queries
- Clean, responsive design that matches your WordPress theme

### Quick Actions
Built-in buttons for common tasks:
- **Journal**: Personal reflection and note-taking
- **Finance**: Cryptocurrency and financial tracking
- **Quests**: RPG-style goal management
- **Status**: System health and status reports

## Configuration

### Admin Settings
Go to **Settings > TEC Companion** in your WordPress admin to:
- View usage instructions
- Check system status
- Configure API endpoints (future feature)

## Troubleshooting

### Common Issues

1. **"Connection Error" Message**
   - Ensure TEC system is running on localhost:8000
   - Check that no firewall is blocking the connection
   - Verify the API health endpoint: `http://localhost:8000/health`

2. **Plugin Not Showing**
   - Make sure the plugin is activated
   - Check that you're using the correct shortcode: `[tec_companion]`
   - Verify file permissions in the plugins directory

3. **Styling Issues**
   - The plugin includes its own CSS that should work with most themes
   - If there are conflicts, you can add custom CSS in **Appearance > Customize > Additional CSS**

### Debug Mode
To enable debug mode, add this to your WordPress `wp-config.php`:

```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
```

Check the debug log at `/wp-content/debug.log` for any error messages.

## Security Considerations

### Local Network Only
This plugin is designed for local development and testing. For production use:

1. Secure the API endpoints with authentication
2. Use HTTPS connections
3. Implement proper input validation and sanitization
4. Consider hosting the TEC system on a secure server

### WordPress Security
- Keep WordPress and all plugins updated
- Use strong passwords and two-factor authentication
- Regular backups of your site

## Development

### Customization
You can customize the plugin by modifying:

- **Styling**: Edit the CSS in the `render_companion()` method
- **JavaScript**: Modify the jQuery code for different behaviors
- **API Integration**: Update the `handle_chat()` method for different endpoints

### Extending Functionality
Future enhancements could include:
- User authentication integration
- Custom TEC commands
- WordPress user data integration
- Multi-site support

## Support

For issues and support:
1. Check the TEC system logs: `tec_startup.log`
2. Verify WordPress error logs
3. Test the API directly: `curl http://localhost:8000/health`
4. Create an issue in the TEC GitHub repository

## License
This plugin is released under the MIT License, same as the main TEC project.

---

**The Creator's Rebellion - Daisy Purecode: Silicate Mother**
*"Unfettered Access Shall Be Maintained"*
