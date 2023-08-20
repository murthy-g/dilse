import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import App from './App';

import RegisterScreen from './components/RegisterScreen';  // Assuming you have created this
import LoginScreen from './components/LoginScreen';
import ProfilePhoto from './components/ProfilePhoto';

type RootStackParamList = {
  Splash: undefined;
  Login: undefined;
  Register: undefined;
  ProfilePhoto: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

const AppNavigator: React.FC = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Splash">
        <Stack.Screen name="Splash" component={App} options={{ headerShown: false }} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="ProfilePhoto" component={ProfilePhoto} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
