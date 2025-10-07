Mouse Input Controller System
This project component provides the fundamental logic for capturing and translating standard mouse inputs into application actions, suitable for interactive environments, simulations, and games.

🕹️ Mouse Controller Overview
The controller is designed for high-responsiveness, mapping core mouse events to critical user interactions such as selection, movement, and camera/view adjustments.

💻 Technical Implementation
The mouse controller logic is implemented using standard JavaScript event listeners attached to the primary <canvas> or rendering container.

The system relies on monitoring three key phases to manage state:

mousedown: Initiates a control sequence and records the starting coordinates.

mousemove: Calculates the delta (change in position) only when a button is actively held down, providing smooth drag/panning functionality.

mouseup: Terminates the active control sequence (e.g., stopping rotation or releasing a dragged object).
