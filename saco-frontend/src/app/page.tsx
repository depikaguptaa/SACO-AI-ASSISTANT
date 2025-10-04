"use client";

import { useState, useEffect } from 'react';
import { motion, useMotionValue } from 'framer-motion';
import { TextHoverEffect } from '@/components/ui/text-hover-effect';
import { GoogleGeminiEffect } from '@/components/ui/google-gemini-effect';
import { LayoutTextFlip } from '@/components/ui/layout-text-flip';
import { ExpandableCard } from '@/components/ui/expandable-card';
import { GlowingEffect } from '@/components/ui/glowing-effect';
import { useAddressProcessor } from '@/hooks/useAddressProcessor';
import { PlaceholdersAndVanishInput } from '@/components/ui/placeholders-and-vanish-input';
import { MultiStepLoader } from '@/components/ui/multi-step-loader';
import { AmenitiesBentoGrid } from '@/components/ui/amenities-bento-grid';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Slider } from '@/components/ui/slider';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function AddressProcessor() {
  const [address, setAddress] = useState('');
  const [radius, setRadius] = useState([1000]);
  const [mounted, setMounted] = useState(false);
  const { loading, result, error, currentStep, progressMessage, processAddress } = useAddressProcessor();

  // Motion values for Google Gemini Effect
  const pathLengths = [
    useMotionValue(0),
    useMotionValue(0),
    useMotionValue(0),
    useMotionValue(0),
    useMotionValue(0),
  ];

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!address.trim()) return;
    await processAddress(address, radius[0]);
  };

  if (!mounted) {
    return null;
  }

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Google Gemini Effect Background */}
      <GoogleGeminiEffect
        pathLengths={pathLengths}
        title=""
        description=""
        className="fixed inset-0 z-0"
      />

      {/* Large SACO AI ASSISTANT Text Hover Effect - Background Layer */}
      <div className="fixed inset-0 z-10 flex items-center justify-center pointer-events-none">
        <div className="text-center w-full h-full">
          <TextHoverEffect
            text="SACO AI ASSISTANT"
            duration={0.5}
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="relative z-20 min-h-screen flex flex-col pointer-events-none">
        {/* Header */}
        <div className="container mx-auto px-4 py-8 pointer-events-auto">
          {/* Small SACO AI ASSISTANT Title */}
          <div className="text-center mb-6 mt-16 relative z-20">
            <h1 className="text-3xl md:text-5xl font-light text-white mb-2 tracking-wide">SACO AI ASSISTANT</h1>
            <p className="text-sm md:text-lg text-gray-300">Intelligent Location Analysis & Amenity Discovery</p>
          </div>
          
          {/* Layout Text Flip Subtitle */}
          <div className="text-center mb-8 relative z-20">
            <LayoutTextFlip
              text="Discover"
              words={["Nearby Amenities", "Location Insights", "Smart Analysis", "AI-Powered Data"]}
              duration={2000}
            />
        </div>

          {/* Search Card with Glowing Effect */}
          <div className="max-w-2xl mx-auto mb-8 pointer-events-auto">
            <div className="bg-black/80 backdrop-blur-sm border border-gray-800 rounded-2xl p-8 shadow-2xl relative">
              <GlowingEffect className="absolute inset-0 rounded-2xl" />
              <div className="space-y-6 relative z-10">
                {/* Address Input */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">
                    Enter US Address
                  </label>
                  <PlaceholdersAndVanishInput
                    placeholders={[
                      "e.g., 123 Main St, New York, NY 10001",
                      "e.g., 1600 Pennsylvania Ave, Washington, DC 20500",
                      "e.g., 1 Apple Park Way, Cupertino, CA 95014",
                      "e.g., 350 5th Ave, New York, NY 10118"
                    ]}
                    onChange={(e) => setAddress(e.target.value)}
                    onSubmit={handleSubmit}
                  />
                </div>

                {/* Radius Slider */}
                <div className="space-y-3">
                  <label className="text-sm font-medium text-gray-300">
                    Search Radius: {radius[0]}m
                  </label>
                  <Slider
                    value={radius}
                    onValueChange={setRadius}
                    max={5000}
                    min={100}
                    step={100}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-400">
                    <span>100m</span>
                    <span>5000m</span>
                  </div>
                </div>

              </div>
            </div>
          </div>

          {/* Results Section */}
          {result && (
            <div className="max-w-7xl mx-auto space-y-8 pointer-events-auto">
              {/* Location Details */}
              {result.coordinates && (
                <div className="bg-gray-900/30 backdrop-blur-sm border border-gray-700 rounded-2xl p-6 shadow-2xl relative">
                  <GlowingEffect className="absolute inset-0 rounded-2xl" glow={true} disabled={false} />
                  <div className="relative z-10">
                    <h3 className="text-xl font-semibold mb-6 text-white">Location Details</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                      <div className="space-y-4">
                        <div>
                          <span className="text-gray-400 font-medium">Full Address:</span>
                          <p className="text-white mt-1 leading-relaxed">{result.coordinates.address}</p>
                        </div>
                        <div>
                          <span className="text-gray-400 font-medium">Coordinates:</span>
                          <p className="text-white mt-1 font-mono">{result.coordinates.latitude}, {result.coordinates.longitude}</p>
                        </div>
                        <div>
                          <span className="text-gray-400 font-medium">Search Radius:</span>
                          <p className="text-white mt-1">{radius[0]}m ({Math.round(radius[0] * 3.28084)} ft)</p>
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div>
                          <span className="text-gray-400 font-medium">Total Amenities Found:</span>
                          <p className="text-white mt-1 text-lg font-semibold">
                            {result.categorized_amenities ? 
                              Object.values(result.categorized_amenities).reduce((total, items) => total + items.length, 0) 
                              : 0} locations
                          </p>
                        </div>
                        <div>
                          <span className="text-gray-400 font-medium">Categories:</span>
                          <p className="text-white mt-1">
                            {result.categorized_amenities ? 
                              Object.keys(result.categorized_amenities).length 
                              : 0} categories
                          </p>
                        </div>
                        <div>
                          <span className="text-gray-400 font-medium">Analysis Status:</span>
                          <p className="text-green-400 mt-1 font-medium">✓ Complete</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Amenities Grid */}
              {result.categorized_amenities && Object.keys(result.categorized_amenities).length > 0 && (
                <div>
                  <h3 className="text-2xl font-semibold mb-6 text-center text-white">Nearby Amenities</h3>
                  <AmenitiesBentoGrid amenities={result.categorized_amenities} />
                </div>
              )}

              {/* AI Analysis - Expandable Card */}
              {result.result && (
                <div className="mb-8">
                  <ExpandableCard
                    title="AI Location Analysis"
                    content={
                      <div className="space-y-6 prose prose-invert max-w-none prose-headings:text-white prose-headings:mb-4 prose-headings:mt-6 prose-h1:text-2xl prose-h1:font-bold prose-h2:text-xl prose-h2:font-semibold prose-h3:text-lg prose-h3:font-medium prose-p:text-gray-300 prose-p:mb-6 prose-p:leading-relaxed prose-li:text-gray-300 prose-li:mb-3 prose-li:leading-relaxed prose-strong:text-white prose-strong:font-semibold prose-ul:space-y-2 prose-ol:space-y-2">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {result.result}
                        </ReactMarkdown>
                      </div>
                    }
                  />
                </div>
              )}
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="max-w-2xl mx-auto pointer-events-auto">
              <div className="bg-red-900/20 border border-red-700 rounded-2xl p-6 relative">
                <GlowingEffect className="absolute inset-0 rounded-2xl" />
                <div className="relative z-10">
                  <h3 className="text-lg font-semibold text-red-400 mb-2">Error</h3>
                  <p className="text-red-300">{error}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Multi Step Loader */}
      <MultiStepLoader
        loadingStates={[
          { text: "Finding coordinates..." },
          { text: "Searching for amenities..." },
          { text: "Categorizing amenities..." },
          { text: "Generating AI analysis..." },
          { text: "Complete!" }
        ]}
        loading={loading}
        duration={1000}
        loop={false}
        currentStep={
          currentStep === 'geocoding' ? 0 :
          currentStep === 'amenities' ? 1 :
          currentStep === 'categorizing' ? 2 :
          currentStep === 'analyzing' ? 3 :
          currentStep === 'complete' ? 4 : 0
        }
      />
    </div>
  );
}