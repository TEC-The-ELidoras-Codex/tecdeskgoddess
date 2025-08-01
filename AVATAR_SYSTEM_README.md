# TEC BITLyfe Avatar System 🎭

## Overview
The TEC BITLyfe Avatar System enhances the chat experience with visual avatars for both AI characters and users. This system includes built-in character avatars and Ready Player Me integration for custom user avatars.

## Features

### ✨ Built-in Character Avatars
- **TEC AI**: Purple gradient with mystical elements
- **Polkin**: Purple mystic theme with starry effects  
- **Mynx**: Cyan tech mystic with circuit elements
- **Kaelen**: Red code warrior with battle-ready design
- **User Default**: Green explorer theme with connection nodes

### 🎨 Avatar Customization
- Select from pre-built character-themed avatars
- Create custom 3D avatars with Ready Player Me
- Real-time avatar preview in chat messages
- Persistent avatar settings via localStorage

### 🔧 Technical Implementation
- SVG-based avatars for crisp display at any size
- Fallback system for failed avatar loads
- Ready Player Me iframe integration
- localStorage persistence for user preferences

## Usage

### Opening Avatar Customization
1. Click the "Avatar" button in the persona controls
2. Browse available avatar options
3. Select your preferred avatar style
4. Save changes to apply immediately

### Creating Custom Avatars
1. Click "Create Custom" in the avatar panel
2. Ready Player Me interface opens in overlay
3. Design your 3D avatar with full customization
4. Avatar automatically saves when complete

### Avatar Display
- User messages show selected user avatar
- AI character messages show their unique avatars
- Fallback to SVG placeholders if images fail to load
- Responsive design works on all screen sizes

## File Structure

```
assets/face/
├── tec-ai-avatar.svg      # TEC AI character
├── polkin-avatar.svg      # Polkin character  
├── mynx-avatar.svg        # Mynx character
├── kaelen-avatar.svg      # Kaelen character
└── user-default-avatar.svg # Default user avatar
```

## API Integration

### Ready Player Me
- **API Key**: `sk_live_2V_-otfWKLzQdqQMXyRpszayLhBk-c7o_Mji`
- **Subdomain**: `tecdeskgoddess.readyplayer.me`
- **Integration**: iframe with postMessage communication
- **Export Format**: GLB 3D models for avatars

### localStorage Keys
- `userAvatar`: Selected avatar type ('default', 'polkin', 'mynx', 'kaelen', 'custom')
- `customAvatarUrl`: Ready Player Me avatar URL (when avatar type is 'custom')

## Development Notes

### CSS Classes
- `.avatar-panel`: Main customization overlay
- `.avatar-option`: Individual avatar selection buttons  
- `.message-avatar`: Chat message avatar images
- `.avatar-preview-img`: Preview image in customization panel

### JavaScript Functions
- `openAvatarPanel()`: Show customization interface
- `selectAvatar(type)`: Choose avatar type
- `saveAvatarSettings()`: Persist avatar choice
- `openReadyPlayerMe()`: Launch 3D avatar creator
- `getUserAvatar()`: Get current user avatar path

## Browser Compatibility
- Modern browsers with CSS Grid and Flexbox support
- localStorage support required
- iframe compatibility for Ready Player Me
- SVG support (universal in modern browsers)

## Future Enhancements
- [ ] Animated avatar expressions
- [ ] Voice-reactive avatar movements  
- [ ] Avatar clothing/accessory system
- [ ] Social avatar sharing features
- [ ] Avatar-based character interactions

---

**Ready to enhance your TEC BITLyfe experience with personalized avatars!** 🚀
