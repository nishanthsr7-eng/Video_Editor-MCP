import React, { createContext, useContext } from 'react';
import { useSettings } from '@/contexts/SettingsContext';

export type Integration = "davinci" | "premiere" | "aftereffects";

interface IntegrationContextType {
  selectedIntegration: Integration;
  setSelectedIntegration: (integration: Integration) => void;
}

const IntegrationContext = createContext<IntegrationContextType | null>(null);

export function IntegrationProvider({ children }: { children: React.ReactNode }) {
  const { settings, updateSetting } = useSettings();
  const selectedIntegration = settings.preferredEditorIntegration;
  const setSelectedIntegration = React.useCallback((integration: Integration) => {
    updateSetting("preferredEditorIntegration", integration);
  }, [updateSetting]);

  return (
    <IntegrationContext.Provider value={{ selectedIntegration, setSelectedIntegration }}>
      {children}
    </IntegrationContext.Provider>
  );
}

export const useIntegration = () => {
  const context = useContext(IntegrationContext);
  if (!context) {
    throw new Error('useIntegration must be used within an IntegrationProvider');
  }
  return context;
};
