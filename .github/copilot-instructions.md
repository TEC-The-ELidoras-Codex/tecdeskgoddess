# Copilot Instructions for TEC Life & Finance Codebase

## Overview
This document provides guidance for AI coding agents working on the TEC Life & Finance project. The goal is to ensure productive contributions by outlining the project's architecture, workflows, conventions, and integration points.

---

## Big Picture Architecture

### Major Components
1. **Frontend**
   - Built with React.js and styled using Tailwind CSS.
   - Key features include:
     - AI Chatbot (Gemini API integration).
     - Journaling and generative tools.
     - Finance tracking and gamification.
   - Located in `blueprints/`.

2. **Backend**
   - Python-based services for complex logic and integrations.
   - Firebase is used for Firestore, Authentication, and Cloud Storage.
   - Key backend modules:
     - `tec_tools/agentic_processor.py`: Core AI processing.
     - `tec_tools/analysis.py`: Data analysis utilities.
     - `tec_tools/api.py`: API endpoints.

3. **Assets**
   - Media files (audio, face images) stored in `assets/`.

4. **Hardware Integration**
   - Placeholder for future smartwatch and IoT integrations.
   - Located in `hardware/`.

---

## Developer Workflows

### Build and Run
- **Frontend**: React app setup is not yet included but will follow standard React workflows.
- **Backend**:
  - Install dependencies: `pip install -r requirements.txt`
  - Run backend services: `python -m tec_tools.api`

### Testing
- No explicit test framework is set up yet. Future tests should be added to `tests/`.

### Debugging
- Use logging in Python modules (`logging` library) for backend debugging.
- React debugging can be done using browser developer tools.

---

## Project-Specific Conventions

1. **Modular Design Philosophy**
   - Each feature is treated as a "module" with iterative development stages: Raw → Once Cooked → Twice Baked → Final Form.

2. **Data Sovereignty**
   - Emphasis on user control over data. Avoid hardcoding sensitive data or relying on external APIs without fallback mechanisms.

3. **Gamification Elements**
   - Follow RPG mechanics for gamified features (e.g., XP, levels, biomes).

---

## Integration Points

1. **Gemini API**
   - Used for AI chatbot and generative tools.
   - API calls are handled in `tec_tools/agentic_processor.py`.

2. **Firebase**
   - Firestore for database, Auth for user authentication.
   - Configuration is expected in `firebaseConfig` (not yet implemented).

3. **Future Integrations**
   - Eleven Labs API for Text-to-Speech.
   - Smartwatch data integration in `hardware/`.

---

## Key Files and Directories
- `README.md`: Comprehensive project overview.
- `tec_tools/`: Core backend logic.
- `blueprints/`: Placeholder for frontend components.
- `assets/`: Media and static files.
- `hardware/`: Future hardware integration modules.

---

## Example Tasks for Copilot
1. **Add a new journaling feature**
   - Extend `tec_tools/lore_extractor.py` to analyze journal entries.
   - Update `blueprints/` with a React component for the journaling UI.

2. **Integrate a new API**
   - Add API logic in `tec_tools/api.py`.
   - Document the integration in `README.md`.

3. **Enhance gamification**
   - Add new RPG mechanics (e.g., badges, quests) in `tec_tools/`.
   - Update frontend to display gamification progress.

---

## Notes for AI Agents
- Always follow the modular design philosophy.
- Prioritize user data sovereignty and security.
- Document any new features or changes in `README.md`.

---

For further clarification, consult the `README.md` or ask for specific guidance.
