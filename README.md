# Chess Game

A complete, feature-rich chess game built with Python and Pygame. This implementation includes all standard chess rules with a modern, intuitive interface.

## Features

### 🎮 Core Gameplay
- **Complete chess implementation** with all 6 piece types
- **Turn-based gameplay** with alternating white/black moves
- **Drag-and-drop interface** for intuitive piece movement
- **Move validation** - only legal chess moves are allowed
- **Piece capture** with visual and audio feedback

### ♟️ Advanced Chess Rules
- **Check detection** - prevents moves that put/leave king in check
- **Checkmate detection** - game ends when king is checkmated
- **Stalemate detection** - game ends in draw when no legal moves exist
- **Castling** - both queen-side (O-O-O) and king-side (O-O) castling
- **En passant** - pawn capture rule for double moves
- **Pawn promotion** - automatic promotion to Queen when reaching opposite end

### 🎨 Visual Features
- **Board flipping** - board rotates 180° when it's black's turn
- **Multiple themes** - 5 different color schemes (green, brown, blue, gray, pink)
- **Move indicators** - highlights valid moves when dragging pieces
- **Last move highlighting** - shows the previous move on the board
- **Hover effects** - visual feedback when moving mouse over squares
- **Check indicator** - red border around king when in check
- **Game over screen** - displays winner or stalemate with restart option

### 🔊 Audio
- **Move sounds** - different sounds for regular moves and captures
- **Sound effects** - enhances the gaming experience

### 🎯 Controls

#### Mouse Controls
- **Click and drag** - Move pieces on the board
- **Hover** - Visual feedback when moving mouse over squares

#### Keyboard Controls
- **T key** - Toggle between board themes (5 different color schemes)
- **R key** - Reset/restart the current game
- **Escape** - Quit the game
- **Close window** - Exit the application

#### Theme Options
1. **Green** - Classic green and brown chess board
2. **Brown** - Warm brown and tan colors
3. **Blue** - Cool blue and gray tones
4. **Gray** - Modern gray and dark gray
5. **Pink** - Light pink and white theme

## Installation

### Prerequisites
- Python 3.7 or higher
- Pygame

### Setup
1. Clone or download this repository
2. Navigate to the project directory
3. Install Pygame:
   ```bash
   pip install pygame
   ```
4. Run the game:
   ```bash
   python src/main.py
   ```

## Project Structure

```
CHESS/
├── src/
│   ├── main.py          # Main game loop and event handling
│   ├── game.py          # Game state management and UI rendering
│   ├── board.py         # Chess board logic and move validation
│   ├── piece.py         # Piece classes and movement rules
│   ├── square.py        # Square representation and utilities
│   ├── move.py          # Move class and validation
│   ├── dragger.py       # Drag-and-drop functionality
│   ├── config.py        # Game configuration and themes
│   ├── theme.py         # Theme management
│   ├── color.py         # Color utilities
│   └── sound.py         # Audio management
├── assets/
│   ├── images/
│   │   ├── imgs-80px/   # 80px piece images
│   │   └── imgs-128px/  # 128px piece images (for dragging)
│   └── sounds/
│       ├── move.wav     # Move sound effect
│       └── capture.wav  # Capture sound effect
└── README.md
```

## How to Play

### Basic Gameplay
1. **Start the game** - White moves first
2. **Click and drag** pieces to move them
3. **Valid moves** are highlighted when you start dragging
4. **Board flips** automatically when it's black's turn
5. **Game ends** when checkmate or stalemate occurs

### Advanced Features
- **Castling**: Move king two squares toward rook (if conditions are met)
- **En passant**: Capture pawn that just moved two squares
- **Check**: King is under attack - must move to safety
- **Checkmate**: King is under attack with no escape
- **Stalemate**: No legal moves but king is not in check

### Visual Indicators
- **Green highlights**: Valid moves when dragging
- **Red border**: King in check
- **Gray border**: Last move made
- **Hover effect**: Square under mouse cursor

## Technical Details

### Architecture
- **Modular design** with separate classes for each component
- **Event-driven** architecture using Pygame events
- **State management** for game progression
- **Coordinate conversion** for board flipping

### Key Algorithms
- **Move validation** with check detection
- **Path finding** for sliding pieces (queen, rook, bishop)
- **Checkmate detection** with move generation
- **Coordinate transformation** for board flipping

### Performance
- **Efficient move calculation** with early termination
- **Optimized rendering** with minimal redraws
- **Smooth 60 FPS** gameplay

## Customization

### Adding New Themes
Edit `src/config.py` to add new color schemes:
```python
new_theme = Theme(
    light_bg, dark_bg,      # Board colors
    light_trace, dark_trace, # Last move colors
    light_moves, dark_moves  # Valid move colors
)
```

### Modifying Piece Images
Replace images in `assets/images/` directories:
- `imgs-80px/` for normal display
- `imgs-128px/` for dragging (larger size)

## Troubleshooting

### Common Issues
1. **Pygame not found**: Install with `pip install pygame`
2. **Images not loading**: Check file paths in `assets/images/`
3. **Sounds not playing**: Check file paths in `assets/sounds/`

### Performance Issues
- Ensure you have sufficient RAM (minimum 4GB recommended)
- Close other applications if experiencing lag
- Update graphics drivers if needed

## Contributing

Feel free to contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute.

## Acknowledgments

- Chess piece images sourced from open-source chess sets
- Sound effects from free sound libraries
- Built with Pygame community resources

---

**Enjoy playing chess!** ♟️
