import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, PermissionsAndroid } from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import Geolocation from 'react-native-geolocation-service';
import { Picker } from '@react-native-picker/picker'; // Import Picker from the correct package

// Define the types for the navigation stack's parameters
type RootStackParamList = {
  Splash: undefined;
  Login: undefined;
  Register: undefined;
  Home: undefined; // Add this line
  ProfilePhoto: undefined; // Add this line
  // ... You can add other screens here
};


// Define the type for the RegisterScreen's props
type RegisterScreenProps = {
  navigation: StackNavigationProp<RootStackParamList, 'Register'>;
};

const RegisterScreen: React.FC<RegisterScreenProps> = ({ navigation }) => {
  const [name, setName] = useState<string>('');
  const [age, setAge] = useState<number | string>('');  // Use string here to make it compatible with TextInput
  const [gender, setGender] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [location, setLocation] = useState<string>('');
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [detectedLocation, setDetectedLocation] = useState<string>('');


  const handleRegister = () => {
    // Construct the request body
    const requestBody = {
      name: name,
      email: email,
      password: password,
      age: Number(age),  // Convert the age back to a number
      gender: gender,
      location: location,
      phone_number: phoneNumber
    };

    if (!validateEmail(email)) {
      console.log('Invalid email format');
      return;
    }

    if (!validateAge(age)) {
      console.log('Age should be between 19 and 55');
      return;
    }

    // Send a POST request to /register endpoint
    fetch('https://qef7b6bqef.execute-api.us-east-1.amazonaws.com/prod/register', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })
      .then(response => response.json())  // Parse the response to JSON
      .then(data => {
        if (data.ResponseMetadata.HTTPStatusCode == 200) {
          console.log("Registration successful");
          navigation.navigate('ProfilePhoto');  // Navigate to the photo upload screen
        } else {
          console.log("Registration failed", data);
        }
      })
      .catch(error => {
        console.error("There was an error during registration", error);
      });
  };

  const detectLocation = () => {
    Geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setDetectedLocation(`Latitude: ${latitude}, Longitude: ${longitude}`);
        setLocation(`Latitude: ${latitude}, Longitude: ${longitude}`);
      },
      (error) => {
        console.log('Error getting location:', error);
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
    );
  };

  const requestLocationPermission = async () => {
    try {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
        {
          title: 'Location Permission',
          message: 'DilSeApp needs access to your location.',
          buttonNeutral: 'Ask Me Later',
          buttonNegative: 'Cancel',
          buttonPositive: 'OK',
        }
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        console.log('Location permission granted');
        detectLocation();
      } else {
        console.log('Location permission denied');
      }
    } catch (err) {
      console.warn(err);
    }
  };

  const validateEmail = (email: string): boolean => {
    // Implement your email validation logic here
    return /^\S+@\S+\.\S+$/.test(email);
  };

  const validateAge = (age: number | string): boolean => {
    const ageNumber = Number(age);
    return ageNumber >= 19 && ageNumber <= 55;
  };

  return (
    <View style={styles.container}>
      <TextInput
        value={name}
        onChangeText={setName}
        placeholder="Name"
        placeholderTextColor="white"
        style={styles.input}
      />
      <Picker
        selectedValue={age}
        onValueChange={(itemValue) => setAge(itemValue)}
        style={styles.input}
      >
        {Array.from({ length: 36 }, (_, index) => (
          <Picker.Item key={index} label={`${19 + index}`} value={`${19 + index}`} />
        ))}
      </Picker>
      <Picker
        selectedValue={gender}
        onValueChange={(itemValue) => setGender(itemValue)}
        style={styles.input}
      >
        <Picker.Item label="Male" value="male" />
        <Picker.Item label="Female" value="female" />
        <Picker.Item label="Other" value="other" />
      </Picker>
      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="Email"
        placeholderTextColor="white"
        keyboardType="email-address"
        style={styles.input}
      />
      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="Password"
        placeholderTextColor="white"
        secureTextEntry
        style={styles.input}
      />
      <TextInput
        value={detectedLocation} // Display the detected location
        placeholder="Detected Location"
        placeholderTextColor="white"
        editable={false} // Disable editing for detected location
        style={styles.input}
      />
      <TextInput
        value={phoneNumber}
        onChangeText={setPhoneNumber}
        placeholder="Phone Number"
        placeholderTextColor="white"
        keyboardType="phone-pad"
        style={styles.input}
      />
      <View style={styles.buttonContainer}>
        <Button title="Register" onPress={handleRegister} color="white" />
      </View>
      <View style={styles.buttonContainer}>
        <Button title="Back to Login" onPress={() => navigation.goBack()} color="white" />
      </View>
      <View style={styles.buttonContainer}>
        <Button title="Detect Location" onPress={requestLocationPermission} color="white" />
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
    overflow: 'hidden',
  },
  logo: {
    width: 200,
    height: 80,
    resizeMode: 'contain',
    alignSelf: 'center',
    marginBottom: 20,
  },
});

export default RegisterScreen;