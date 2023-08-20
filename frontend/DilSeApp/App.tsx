import React, { useState, useEffect } from 'react';
import { View, Image, StyleSheet, Animated, TouchableOpacity, Text, Alert } from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';

type RootStackParamList = {
  Splash: undefined;
  Login: undefined;
  Register: undefined;
};

type Props = {
  navigation: StackNavigationProp<RootStackParamList, 'Splash'>;
};

const App: React.FC<Props> = ({ navigation }) => {
  const [opacity] = useState(new Animated.Value(0)); 
  const scale = new Animated.Value(1); 

  const onLogoPress = () => {
    Alert.alert(
      "Navigate",
      "Go to Login or Register page?",
      [
        {
          text: "Cancel",
          onPress: () => console.log("Cancel Pressed"),
          style: "cancel"
        },
        {
          text: "OK",
          onPress: () => navigation.navigate('Login')  // Navigate to Login on pressing OK
        }
      ]
    );
  };

  useEffect(() => {
    Animated.timing(opacity, {
      toValue: 1,
      duration: 2000,
      useNativeDriver: true,
    }).start();

    // Heart pump animation
    Animated.loop(
      Animated.sequence([
        Animated.timing(scale, {
          toValue: 1.2,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(scale, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
        }),
      ])
    ).start();

  }, [opacity]);

  return (
    <View style={styles.container}>
      <TouchableOpacity onPress={onLogoPress}>
        <Animated.Image
          source={require('./assets/dilse4.png')}
          style={{ ...styles.logo, opacity, transform: [{ scale }] }}
        />
      </TouchableOpacity>
      <View style={styles.textContainer}>
        <Text style={styles.d}>D</Text>
        <Text style={styles.i}>i</Text>
        <Text style={styles.l}>l</Text>
        <Text style={styles.s}>s</Text>
        <Text style={styles.e}>e</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    width: 100,
    height: 100,
    resizeMode: 'contain'
  },
  textContainer: {
    flexDirection: 'row',
    marginTop: 10
  },
  d: {
    color: '#FF0000', // Red
    fontSize: 24,
    fontWeight: 'bold'
  },
  i: {
    color: '#00FF00', // Green
    fontSize: 24,
    fontWeight: 'bold'
  },
  l: {
    color: '#00A2FF', // Lighter Blue
    fontSize: 24,
    fontWeight: 'bold'
  },
  s: {
    color: '#FFFF00', // Yellow
    fontSize: 24,
    fontWeight: 'bold'
  },
  e: {
    color: '#FF00FF', // Magenta
    fontSize: 24,
    fontWeight: 'bold'
  }
});

export default App;
