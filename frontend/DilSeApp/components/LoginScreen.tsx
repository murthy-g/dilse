import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Image } from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';

// Define the types for the navigation stack's parameters
type RootStackParamList = {
  Splash: undefined;
  Login: undefined;
  Register: undefined;
  Home: undefined; // Add this line
  ProfilePhoto: undefined; // Add this line
  // ... You can add other screens here
};


// Define the type for the LoginScreen's props
type LoginScreenProps = {
  navigation: StackNavigationProp<RootStackParamList, 'Login'>;
};

const LoginScreen: React.FC<LoginScreenProps> = ({ navigation }) => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');


  const handleLogin = () => {
    // Construct the request body
    const requestBody = {
      email: email,
      password: password
    };

    // Send a POST request to /login endpoint
    fetch('https://qef7b6bqef.execute-api.us-east-1.amazonaws.com/prod/login', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })
      .then(response => response.json())  // Parse the response to JSON
      .then(data => {
        if (data.success) {  // Assuming the server returns { success: true } on valid credentials
          console.log("Login successful");
          navigation.navigate('Home');  // Navigate to home on successful login
        } else {
          console.log("Login failed", data.message);  // Display the error message returned from the server
        }
      })
      .catch(error => {
        console.error("There was an error logging in", error);
      });
  };


  return (
    <View style={styles.container}>
      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="Email"
        placeholderTextColor="white"
        style={styles.input}
        keyboardType="email-address"
      />
      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="Password"
        placeholderTextColor="white"
        secureTextEntry
        style={styles.input}
      />
      <View style={styles.buttonContainer}>
        <Button title="Login" onPress={handleLogin} color="white" />
      </View>
      <View style={styles.buttonContainer}>
        <Button title="Register" onPress={() => navigation.navigate('Register')} color="white" />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 20,
    backgroundColor: 'black',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingLeft: 8,
    color: 'white',
  },
  buttonContainer: {
    marginBottom: 10,
    borderWidth: 1,
    borderColor: 'white',
    borderRadius: 5,
    overflow: 'hidden',  // This makes sure the button color does not leak out
  },
  logo: {
    width: 200,      // adjust the width as per your need
    height: 80,      // adjust the height as per your need
    resizeMode: 'contain',
    alignSelf: 'center',
    marginBottom: 20,
  },
});

export default LoginScreen;
