import React from 'react';
import { AppRegistry } from 'react-native';
import AppNavigator from './AppNavigator';
import { name as appName } from './app.json';
import { enableScreens } from 'react-native-screens';
import { SafeAreaProvider } from 'react-native-safe-area-context';


enableScreens();

const AppRoot = () => {
  return (
    <SafeAreaProvider>
      <AppNavigator />
    </SafeAreaProvider>
  );
}

AppRegistry.registerComponent(appName, () => AppRoot);
