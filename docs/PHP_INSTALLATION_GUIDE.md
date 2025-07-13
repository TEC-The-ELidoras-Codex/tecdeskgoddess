# TEC PHP Installation Guide for Windows

## Quick PHP Installation Options

### Option 1: Using Chocolatey (Recommended)
1. Install Chocolatey if you don't have it:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. Install PHP:
   ```powershell
   choco install php
   ```

3. Verify installation:
   ```powershell
   php --version
   ```

### Option 2: Manual PHP Installation
1. Download PHP from: https://windows.php.net/download/
   - Choose "Non Thread Safe" version
   - Download the ZIP file

2. Extract to `C:\php`

3. Add to PATH:
   - Open System Properties → Environment Variables
   - Add `C:\php` to your PATH variable

4. Create php.ini:
   - Copy `php.ini-development` to `php.ini`
   - Edit as needed

### Option 3: Use XAMPP (Includes Apache, MySQL, PHP)
1. Download XAMPP: https://www.apachefriends.org/
2. Install and run
3. PHP will be at: `C:\xampp\php\php.exe`

### Option 4: Use Local WordPress Development (Recommended for WordPress)
1. Install Local by Flywheel: https://localwp.com/
2. Includes PHP, MySQL, and WordPress automatically
3. Perfect for WordPress plugin development

## VS Code Configuration

After installing PHP, configure VS Code:

1. Open VS Code Settings (Ctrl+,)
2. Search for "php.validate.executablePath"
3. Set the path to your PHP executable:
   - Chocolatey: Usually auto-detected
   - Manual: `C:\php\php.exe`
   - XAMPP: `C:\xampp\php\php.exe`
   - Local: `C:\Users\{username}\AppData\Roaming\Local\lightning-services\php-8.0.13+6\bin\win32\php.exe`

## Alternative: Disable PHP Validation

If you don't need PHP validation (since TEC is primarily Python):

1. Open VS Code Settings
2. Search for "php.validate.enable"
3. Set to `false`

## For TEC Development

Since TEC is primarily a Python project, you can:

1. **Disable PHP validation** (simplest)
2. **Use the WordPress plugin as-is** - it will work on any WordPress site with PHP
3. **Focus on the Python backend** - that's where the main functionality is

## Testing the WordPress Plugin

To test the WordPress plugin without local PHP:

1. Upload to a live WordPress site
2. Use a WordPress hosting service with staging
3. Install Local by Flywheel for local WordPress development

The plugin code is complete and ready to use - you just need a WordPress environment to run it in.
