"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronUp } from "lucide-react";
import { GlowingEffect } from "@/components/ui/glowing-effect";

interface ExpandableCardProps {
  title: string;
  content: React.ReactNode;
  className?: string;
}

export const ExpandableCard: React.FC<ExpandableCardProps> = ({ 
  title, 
  content, 
  className = "" 
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={`bg-gray-900/30 backdrop-blur-sm border border-gray-700 rounded-2xl overflow-hidden relative ${className}`}>
      <GlowingEffect className="absolute inset-0 rounded-2xl" glow={true} disabled={false} />
      <div className="relative z-10">
        <motion.button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full p-6 text-left flex items-center justify-between hover:bg-gray-800/50 transition-colors"
        >
          <h3 className="text-xl font-semibold text-white">{title}</h3>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-400">click to reveal</span>
            <motion.div
              animate={{ rotate: isExpanded ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <ChevronDown className="h-5 w-5 text-gray-400" />
            </motion.div>
          </div>
        </motion.button>
        
        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3, ease: "easeInOut" }}
              className="overflow-hidden"
            >
                      <div className="px-6 pb-8 border-t border-gray-700">
                        <div className="pt-6">
                          {content}
                        </div>
                      </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
