# SACO AI Assistant Frontend

The web interface for the SACO AI Assistant. Built with NextJS and some nice UI components from Aceternity UI.

## What this does

This is the frontend that users interact with. You type in an address, adjust the search radius, and it shows you nearby amenities with AI analysis. The interface updates in real-time as the backend processes your request.

## Features

### Main functionality
- **Address input**: Type any US address with dynamic placeholders
- **Radius control**: Slider to adjust search area (100m - 5km)
- **Real-time progress**: Shows what's happening as it processes
- **Amenity display**: Organized results with pagination
- **AI analysis**: Expandable cards with location insights
- **Location details**: Shows coordinates and search info

### UI stuff
- **Animated background**: Google Gemini effect that responds to loading
- **Large title text**: "SACO AI ASSISTANT" with gradient animations
- **Dynamic subtitle**: Rotates through different phrases
- **Interactive input**: Address field with canvas animations
- **Progress loader**: Multi-step indicator with real-time updates
- **Glowing effects**: Buttons and cards have subtle glow
- **Glass design**: Modern glassmorphism throughout
- **Grid layout**: Organized amenity display
- **Expandable sections**: Collapsible AI analysis

### Performance
- **Live updates**: Frontend updates as backend processes
- **Caching**: Results cached for faster repeat searches
- **Error handling**: Graceful fallbacks when things go wrong
- **Mobile friendly**: Works on phones and tablets

## Components used

I used these Aceternity UI components:
- **Google Gemini Effect**: Animated SVG background
- **Text Hover Effect**: Large text with gradient animations
- **Layout Text Flip**: Rotating subtitle text
- **Placeholders & Vanish Input**: Dynamic input with animations
- **Multi-Step Loader**: Progress indicator
- **Glowing Effect**: Interactive glow effects
- **Bento Grid**: Grid layout for content
- **Expandable Card**: Collapsible sections

## Getting started

### What you need
- Node.js 18+
- Backend running on http://localhost:8000

### Setup
1. Install packages:
   ```bash
   npm install
   ```

2. The API URL is set in `src/lib/api.ts` (defaults to http://localhost:8000)

3. Start the dev server:
   ```bash
   npm run dev
   ```

4. Open http://localhost:3000 in your browser

## Tech stack

- **NextJS 15**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Framer Motion**: Animations
- **Aceternity UI**: UI components
- **ReactMarkdown**: Renders AI analysis
- **Lucide React**: Icons

## Project structure

```
src/
├── app/
│   ├── layout.tsx          # Root layout with favicon
│   ├── page.tsx           # Main page with all components
│   └── globals.css        # Global styles (dark theme)
├── components/
│   └── ui/                # UI components
│       ├── google-gemini-effect.tsx
│       ├── text-hover-effect.tsx
│       ├── layout-text-flip.tsx
│       ├── placeholders-and-vanish-input.tsx
│       ├── multi-step-loader.tsx
│       ├── glowing-effect.tsx
│       ├── amenities-bento-grid.tsx
│       ├── expandable-card.tsx
│       ├── bento-grid.tsx
│       ├── button.tsx
│       ├── input.tsx
│       ├── card.tsx
│       └── slider.tsx
├── hooks/
│   └── useAddressProcessor.ts  # Handles address processing
└── lib/
    ├── api.ts            # API calls with progress tracking
    └── utils.ts          # Helper functions
```

## How to use it

1. **Enter address**: Type any US address in the input field
2. **Adjust radius**: Use the slider to set search area (100m - 5km)
3. **Click search**: Hit the button to start processing
4. **Watch progress**: See real-time updates as it works
5. **View results**: Check out coordinates, amenities, and AI analysis

## Visual effects

### Google Gemini Effect
- Animated SVG background that stays fixed while scrolling
- Path animations that respond to loading state
- Creates a modern, immersive feel

### Text Hover Effect
- Large "SACO AI ASSISTANT" text with gradient colors
- Automatically simulates mouse movement for continuous effect
- Colors: yellow, red, blue, cyan, purple

### Layout Text Flip
- "Discover" text with rotating phrases
- Smooth transitions between different amenity types
- Compact design with proper spacing

### Placeholders & Vanish Input
- Dynamic placeholders that cycle through examples
- Canvas-based vanish animation when you submit
- Slim border design with good contrast

### Multi-Step Loader
- Real-time progress updates from the backend
- Step-by-step visual feedback
- Matches the app's black/white theme

### Glowing Effects
- Interactive glow on buttons and cards
- Configurable glow intensity and movement
- Adds a nice touch to interactive elements

## Configuration

### Environment
- API URL is in `src/lib/api.ts`
- Default: `http://localhost:8000`

### Customization
- Modify glow effects in `glowing-effect.tsx`
- Adjust text animations in `text-hover-effect.tsx`
- Change placeholder examples in `page.tsx`
- Customize Gemini background in `google-gemini-effect.tsx`

## Troubleshooting

### Common issues

1. **Hydration errors**:
   - Fixed with `suppressHydrationWarning` and mounted state
   - Shouldn't happen with current setup

2. **Animation performance**:
   - Uses hardware acceleration with `transform` properties
   - Optimized for smooth 60fps animations

3. **Mobile responsiveness**:
   - All components work on mobile
   - Touch interactions work fine

4. **API connection**:
   - Make sure backend is running on http://localhost:8000
   - Check CORS settings in backend

## Scripts

- `npm run dev`: Start dev server with Turbopack
- `npm run build`: Build for production with Turbopack
- `npm run start`: Start production server

## Customization

### Styling
- Modify `globals.css` for global styles and dark theme
- Use Tailwind classes for component styling
- Customize colors in CSS variables

### Components
- All Aceternity UI components are customizable
- Easy to modify animations, colors, and effects
- Built with TypeScript for type safety

## Production deployment

```bash
# Build for production
npm run build

# Start production server
npm start
```

---

That's it! The interface should be smooth and responsive.