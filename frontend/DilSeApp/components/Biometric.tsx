import React, { useEffect } from 'react';
import { Text, TouchableOpacity } from 'react-native';
import { FingerprintJsProProvider, useVisitorData } from '@fingerprintjs/fingerprintjs-pro-react-native';


const Biometric: React.FC = () => {
  const visitorData = useVisitorData();

  React.useEffect(() => {
    if (visitorData) {
      console.log('Visitor ID:', visitorData);
      // Use visitor data as required
    }
  }, [visitorData]);

  const handleAuthentication = () => {
    console.log('handleAuthentication');
  };

  return (
    <FingerprintJsProProvider
      token="e7xltkrnybW5H8kOeSy3"
      region="us">
      {/* <TouchableOpacity onPress={handleAuthentication}> */}
      <Text>Authenticate</Text>
      {/* </TouchableOpacity> */}
    </FingerprintJsProProvider>
  );
}

export default Biometric;
