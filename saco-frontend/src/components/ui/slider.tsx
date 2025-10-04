import React from 'react';
import { cn } from '@/lib/utils';

interface SliderProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number[];
  onValueChange?: (value: number[]) => void;
  min?: number;
  max?: number;
  step?: number;
}

export const Slider = React.forwardRef<HTMLDivElement, SliderProps>(
  ({ className, value = [0], onValueChange, min = 0, max = 100, step = 1, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = [parseInt(e.target.value)];
      onValueChange?.(newValue);
    };

    return (
      <div
        ref={ref}
        className={cn('relative flex w-full touch-none select-none items-center', className)}
        {...props}
      >
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value[0]}
          onChange={handleChange}
          className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-white/50 slider-white-thumb"
          style={{
            background: `linear-gradient(to right, #ffffff 0%, #ffffff ${((value[0] - min) / (max - min)) * 100}%, #374151 ${((value[0] - min) / (max - min)) * 100}%, #374151 100%)`
          }}
        />
      </div>
    );
  }
);
Slider.displayName = 'Slider';
