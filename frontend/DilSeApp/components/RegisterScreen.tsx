import React, { useState } from 'react';
import { View, TextInput, StyleSheet, TouchableOpacity, Text } from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import ModalDropdown from 'react-native-modal-dropdown';

type RootStackParamList = {
  Splash: undefined;
  Login: undefined;
  Register: undefined;
  Home: undefined;
  ProfilePhoto: undefined;
};

const ageItems = Array.from({ length: 36 }, (_, index) => ({
  label: `${19 + index}`,
  value: `${19 + index}`,
}));

type RegisterScreenProps = {
  navigation: StackNavigationProp<RootStackParamList, 'Register'>;
};

const RegisterScreen: React.FC<RegisterScreenProps> = ({ navigation }) => {
  const [name, setName] = useState<string>('');
  const [age, setAge] = useState<number | string>('');
  const [gender, setGender] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [location, setLocation] = useState<string>('');
  const [phoneNumber, setPhoneNumber] = useState<string>('');

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
      <ModalDropdown
        options={['Male', 'Female', 'Other']}
        defaultValue="Select Gender"
        style={[styles.input, styles.modalDropdown]}
        textStyle={styles.modalDropdownText}
        dropdownStyle={styles.modalDropdownList}
        dropdownTextStyle={styles.modalDropdownListText}
        onSelect={(index: any, value: React.SetStateAction<string>) => setGender(value)}
      />
      <ModalDropdown
        options={ageItems.map(item => item.label)}
        defaultValue="Select Age"
        style={[styles.input, styles.modalDropdown]}
        textStyle={styles.modalDropdownText}
        dropdownStyle={styles.modalDropdownList}
        dropdownTextStyle={styles.modalDropdownListText}
        onSelect={(index: any, value: React.SetStateAction<string>) => setAge(value.toString())}
      />
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
        value={location}
        placeholder="Enter Location"
        placeholderTextColor="white"
        style={styles.input}
        onChangeText={setLocation}
      />
      <TextInput
        value={phoneNumber}
        onChangeText={setPhoneNumber}
        placeholder="Phone Number"
        placeholderTextColor="white"
        keyboardType="phone-pad"
        style={styles.input}
      />
      <TouchableOpacity onPress={handleRegister} style={styles.customButton}>
        <Text style={styles.buttonText}>Register</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.customButton}>
        <Text style={styles.buttonText}>Back to Login</Text>
      </TouchableOpacity>
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
  customButton: {
    backgroundColor: '#555',
    padding: 10,
    alignItems: 'center',
    borderRadius: 5,
    marginBottom: 10,
  },
  buttonText: {
    color: 'white',
  },
  logo: {
    width: 200,
    height: 80,
    resizeMode: 'contain',
    alignSelf: 'center',
    marginBottom: 20,
  },
  modalDropdown: {
    // Styles for the dropdown button/main component
    height: 40,
    minWidth: 150,  // Set minimum width here. Adjust the value as needed.
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingLeft: 8,
    borderRadius: 4,
    justifyContent: 'center',  // Vertically center the text
  },

  modalDropdownText: {
    color: 'white',  // Color of the text on the dropdown button
  },

  modalDropdownList: {
    // Styles for the dropdown list
    backgroundColor: '#333',  // Darker background for contrast
    borderColor: 'gray',
    borderWidth: 1,
    marginTop: -10,  // To make it visually connect with the dropdown button
  },

  modalDropdownListText: {
    color: 'black',  // Color of the text in the dropdown list
    padding: 8,  // Padding for each item in the dropdown list
  },
});

export default RegisterScreen;
