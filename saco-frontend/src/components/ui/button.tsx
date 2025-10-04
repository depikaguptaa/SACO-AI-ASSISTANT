import React from 'react';
import { cn } from '@/lib/utils';
import { motion, HTMLMotionProps } from 'framer-motion';
import { MovingBorder } from './moving-border';

interface ButtonProps extends Omit<HTMLMotionProps<"button">, "children"> {
  variant?: 'default' | 'outline' | 'ghost' | 'moving-border';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', children, ...props }, ref) => {
    const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background';
    
    const variantClasses = {
      'bg-primary text-primary-foreground hover:bg-primary/90': variant === 'default',
      'border border-input hover:bg-accent hover:text-accent-foreground': variant === 'outline',
      'hover:bg-accent hover:text-accent-foreground': variant === 'ghost',
    };
    
    const sizeClasses = {
      'h-9 px-3 text-sm': size === 'sm',
      'h-10 px-4 py-2': size === 'md',
      'h-11 px-8 text-lg': size === 'lg',
    };

    if (variant === 'moving-border') {
      return (
        <MovingBorder
          duration={2000}
          className="rounded-md"
        >
          <motion.button
            className={cn(
              baseClasses,
              sizeClasses,
              'bg-black text-white border-0',
              className
            )}
            ref={ref}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            {...props}
          >
            {children}
          </motion.button>
        </MovingBorder>
      );
    }

    return (
      <motion.button
        className={cn(
          baseClasses,
          variantClasses,
          sizeClasses,
          className
        )}
        ref={ref}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        {...props}
      >
        {children}
      </motion.button>
    );
  }
);
Button.displayName = 'Button';
