import { useState, useCallback } from 'react';
import { AddressService, AddressResponse } from '@/lib/api';

interface ProcessingState {
  loading: boolean;
  result: AddressResponse | null;
  error: string | null;
  currentStep: string;
  progressMessage: string;
}

export const useAddressProcessor = () => {
  const [state, setState] = useState<ProcessingState>({
    loading: false,
    result: null,
    error: null,
    currentStep: '',
    progressMessage: ''
  });

  const processAddress = useCallback(async (address: string, radius: number = 1000) => {
    setState({
      loading: true,
      result: null,
      error: null,
      currentStep: 'starting',
      progressMessage: 'Starting analysis...'
    });

    try {
      const result = await AddressService.processAddressWithProgress(
        address,
        radius,
        (step, data) => {
          console.log('Progress update:', step, data?.message);
          setState(prev => ({
            ...prev,
            currentStep: step,
            progressMessage: data?.message || 'Processing...'
          }));
        }
      );

      setState({
        loading: false,
        result,
        error: null,
        currentStep: 'complete',
        progressMessage: 'Analysis complete!'
      });
    } catch (error) {
      setState({
        loading: false,
        result: null,
        error: error instanceof Error ? error.message : 'An error occurred',
        currentStep: 'error',
        progressMessage: 'Error occurred'
      });
    }
  }, []);

  return {
    loading: state.loading,
    result: state.result,
    error: state.error,
    currentStep: state.currentStep,
    progressMessage: state.progressMessage,
    processAddress
  };
};
