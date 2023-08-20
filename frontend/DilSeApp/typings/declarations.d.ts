declare module 'react-native-fingerprint-scanner' {
    export function isSensorAvailable(): Promise<void>;
    export function authenticate(options: { title: string }): Promise<void>;
    // Add other methods and types as needed.
}
