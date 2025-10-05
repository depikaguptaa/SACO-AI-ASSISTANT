// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://saco-ai-assistant.onrender.com';

// Types for TypeScript
export interface Coordinates {
  latitude: number;
  longitude: number;
  address: string;
}

export interface Amenity {
  name: string;
  amenity_type: string;
  distance?: number;
  coordinates?: {
    lat: number;
    lon: number;
  };
}

export interface AddressResponse {
  success: boolean;
  address: string;
  coordinates?: Coordinates;
  amenities: Amenity[];
  categorized_amenities?: Record<string, Amenity[]>;
  result?: string;
  error?: string;
  radius_used: number;
}

export interface AddressRequest {
  address: string;
  radius: number;
}

// API Service
export class AddressService {
  static async processAddress(address: string, radius: number = 1000): Promise<AddressResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/process-address`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          address,
          radius,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      // Check if the API returned success: false
      if (!result.success && result.error) {
        throw new Error(result.error);
      }
      
      return result;
    } catch (error) {
      console.error('Error processing address:', error);
      throw error;
    }
  }

  static async processAddressWithProgress(
    address: string, 
    radius: number = 1000,
    onProgress?: (step: string, data?: any) => void
  ): Promise<AddressResponse> {
    try {
      // Step 1: Geocoding
      onProgress?.('geocoding', { message: 'Finding coordinates...' });
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Step 2: Amenities
      onProgress?.('amenities', { message: 'Searching for amenities...' });
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Step 3: Categorizing
      onProgress?.('categorizing', { message: 'Categorizing amenities...' });
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Step 4: Analyzing
      onProgress?.('analyzing', { message: 'Generating AI analysis...' });
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const response = await fetch(`${API_BASE_URL}/process-address`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          address,
          radius,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      // Check if the API returned success: false
      if (!result.success && result.error) {
        throw new Error(result.error);
      }
      
      // Add a small delay to show the analyzing step
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Step 5: Complete
      onProgress?.('complete', { message: 'Complete!', data: result });
      
      return result;
    } catch (error) {
      console.error('Error processing address:', error);
      onProgress?.('error', { message: 'Error occurred', error });
      throw error;
    }
  }

  static async getAmenityTypes() {
    try {
      const response = await fetch(`${API_BASE_URL}/amenity-types`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching amenity types:', error);
      throw error;
    }
  }

  static async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return await response.json();
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  }
}
