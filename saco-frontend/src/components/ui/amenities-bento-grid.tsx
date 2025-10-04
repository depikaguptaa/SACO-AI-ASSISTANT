"use client";

import { cn } from "@/lib/utils";
import React from "react";
import { BentoGrid, BentoGridItem } from "./bento-grid";
import { GlowingEffect } from "./glowing-effect";

import { Amenity } from "@/lib/api";

interface AmenitiesBentoGridProps {
  amenities: Record<string, Amenity[]>;
}

const AmenityCard = ({ category, items }: { category: string; items: Amenity[] }) => {
  const [currentPage, setCurrentPage] = React.useState(0);
  const itemsPerPage = 8; // Show more items per page
  const totalPages = Math.ceil(items.length / itemsPerPage);

  const currentItems = items.slice(
    currentPage * itemsPerPage,
    (currentPage + 1) * itemsPerPage
  );

  const goToPrevious = () => {
    setCurrentPage((prev) => Math.max(0, prev - 1));
  };

  const goToNext = () => {
    setCurrentPage((prev) => Math.min(totalPages - 1, prev + 1));
  };

  return (
    <div className="flex flex-col w-full h-full min-h-[24rem] rounded-xl bg-black/80 backdrop-blur-sm border border-gray-800 p-6 shadow-2xl relative hover:border-gray-700 transition-all duration-300">
      {/* Category Header */}
      <div className="flex items-center gap-3 mb-4 pb-3 border-b border-gray-700">
        <div className="relative">
          {getCategoryIcon(category)}
        </div>
        <div className="flex-1">
          <h3 className="font-bold text-xl text-white">{category}</h3>
          <p className="text-sm text-gray-400">{items.length} {items.length === 1 ? 'location' : 'locations'}</p>
        </div>
      </div>

      {/* Amenities List */}
      <div className="flex-1 flex flex-col min-h-0">
        <div className="space-y-2 flex-1 overflow-y-auto custom-scrollbar">
          {currentItems.map((amenity, index) => (
            <div key={index} className="p-3 bg-gray-900/40 rounded-lg hover:bg-gray-900/60 transition-colors">
              <p className="font-medium text-white text-sm">{amenity.name}</p>
              <p className="text-gray-400 text-xs mt-1">
                {amenity.amenity_type.split(':')[0].replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                {amenity.coordinates && (
                  <span className="block text-xs text-gray-500 mt-1">
                    {amenity.coordinates.lat.toFixed(4)}, {amenity.coordinates.lon.toFixed(4)}
                  </span>
                )}
              </p>
            </div>
          ))}
        </div>

        {/* Pagination Controls */}
        <div className="flex-shrink-0 mt-4 pt-3 border-t border-gray-700">
          {totalPages > 1 ? (
            <div className="flex items-center justify-between">
              <button
                onClick={goToPrevious}
                disabled={currentPage === 0}
                className="flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-white bg-gray-900 hover:bg-gray-800 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span>←</span>
                <span>Previous</span>
              </button>

              <div className="px-3 py-1 text-sm font-semibold text-gray-300">
                {currentPage + 1} / {totalPages}
              </div>

              <button
                onClick={goToNext}
                disabled={currentPage === totalPages - 1}
                className="flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-white bg-gray-900 hover:bg-gray-800 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span>Next</span>
                <span>→</span>
              </button>
            </div>
          ) : (
            <div className="text-center text-sm text-gray-400">
              <span>All {items.length} items shown</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const getCategoryIcon = (category: string) => {
  const iconTexts: Record<string, string> = {
    'Education': '🎓',
    'Healthcare': '🏥',
    'Dining': '🍽️',
    'Transportation': '⛽',
    'Banking': '🏦',
    'Pharmacy': '💊',
    'Recreation': '🌳',
    'Shopping': '🛒',
    'Other': '📍'
  };
  
  const iconText = iconTexts[category] || '📍';
  
  return (
    <div className="relative w-8 h-8 flex items-center justify-center">
      <GlowingEffect 
        className="absolute inset-0 rounded-lg"
        variant="default"
        glow={true}
        disabled={false}
        movementDuration={3}
        spread={30}
        proximity={10}
      />
      <span className="relative z-10 text-lg">{iconText}</span>
    </div>
  );
};

const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    'Education': 'from-blue-600 to-blue-800',
    'Healthcare': 'from-red-600 to-red-800',
    'Dining': 'from-orange-600 to-orange-800',
    'Transportation': 'from-gray-600 to-gray-800',
    'Banking': 'from-green-600 to-green-800',
    'Pharmacy': 'from-pink-600 to-pink-800',
    'Recreation': 'from-emerald-600 to-emerald-800',
    'Shopping': 'from-purple-600 to-purple-800',
    'Other': 'from-slate-600 to-slate-800'
  };
  return colors[category] || 'from-slate-600 to-slate-800';
};

const getCategoryDescription = (category: string, count: number) => {
  const descriptions: Record<string, string> = {
    'Education': `Discover ${count} educational institutions and learning centers in the area.`,
    'Healthcare': `Find ${count} healthcare facilities and medical services nearby.`,
    'Dining': `Explore ${count} restaurants, cafes, and dining options in the vicinity.`,
    'Transportation': `Access ${count} transportation hubs and fuel stations in the area.`,
    'Banking': `Locate ${count} banking services and financial institutions nearby.`,
    'Pharmacy': `Find ${count} pharmacies and medical supply stores in the area.`,
    'Recreation': `Discover ${count} parks, recreational areas, and outdoor activities.`,
    'Shopping': `Explore ${count} shopping centers, stores, and retail locations.`,
    'Other': `Find ${count} other amenities and services in the surrounding area.`
  };
  return descriptions[category] || `Discover ${count} amenities in this category.`;
};

export function AmenitiesBentoGrid({ amenities }: AmenitiesBentoGridProps) {
  const categories = Object.entries(amenities).filter(([_, items]) => items.length > 0);
  
  if (categories.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="bg-gray-900/50 border border-gray-700 rounded-2xl p-8">
          <p className="text-gray-400">No amenities found in the specified radius.</p>
        </div>
      </div>
    );
  }

  // Create items array for BentoGrid
  const items = categories.map(([category, items]) => ({
    header: <AmenityCard category={category} items={items} />,
    className: items.length > 10 ? "md:col-span-2" : "md:col-span-1",
  }));

  return (
    <BentoGrid className="max-w-7xl mx-auto md:auto-rows-[28rem]">
      {items.map((item, i) => (
        <BentoGridItem
          key={i}
          header={item.header}
          className={item.className}
        />
      ))}
    </BentoGrid>
  );
}
