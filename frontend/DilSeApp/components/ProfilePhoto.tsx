import React, { useState } from 'react';
import { View, Button, Image, StyleSheet, ScrollView } from 'react-native';
import ImagePicker, { ImageLibraryOptions, ImagePickerResponse } from 'react-native-image-picker';
import S3 from 'react-native-s3';
import { StackNavigationProp } from '@react-navigation/stack';

interface Avatar {
  uri: string;
  key: string;
}

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
type ProfilePhotoProps = {
  navigation: StackNavigationProp<RootStackParamList, 'ProfilePhoto'>;
};


const ProfilePhoto: React.FC<ProfilePhotoProps> = () => {
  const [avatars, setAvatars] = useState<Avatar[]>([]);

  const pickImages = () => {
    const options: ImageLibraryOptions = {
      mediaType: 'photo',
      selectionLimit: 5,
      includeBase64: false,
    };

    ImagePicker.launchImageLibrary(options, (responses: ImagePickerResponse) => {
      if (responses.didCancel) {
        console.log('User cancelled image picker');
      } else if (responses.errorMessage) {
        console.log('ImagePicker Error: ', responses.errorMessage);
      } else {
        if (responses.assets?.length === 0) return;
        const selectedAvatars: Avatar[] = (responses.assets || [])
          .filter((asset) => asset.uri) // Filter out assets without URI
          .map((asset) => ({
            uri: asset.uri || '',
            key: asset.fileName || '', // Provide a default value to avoid potential null or undefined
          }));
        setAvatars(selectedAvatars);
        // Upload the selected images to S3 bucket
        uploadToS3(selectedAvatars);
      }
    });
  };

  const uploadToS3 = async (images: Avatar[]) => {
    const options = {
      keyPrefix: 'uploads/', // Adjust key prefix as needed
      bucket: 'dilse-bucket',
      region: 'us-east-1', // Add a comma here
      successActionStatus: 201, // HTTP response status on success
    };

    const s3 = new S3(options);

    for (const image of images) {
      const response = await s3.upload({
        uri: image.uri,
        key: image.key,
        contentType: 'image/jpeg', // Adjust content type as needed
      });

      console.log('Upload response:', response);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {avatars.map((avatar, index) => (
        <Image key={index} source={{ uri: avatar.uri }} style={styles.avatar} />
      ))}
      <Button title="Pick Photos" onPress={pickImages} />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingVertical: 20,
    paddingHorizontal: 10,
    alignItems: 'center',
    backgroundColor: 'black',
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginBottom: 20,
  },
});


export default ProfilePhoto;
