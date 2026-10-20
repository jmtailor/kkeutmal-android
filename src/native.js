// Bundled into www/native.js. Exposes the Capacitor plugins to the game page.
import { Capacitor } from '@capacitor/core';
import { SpeechRecognition } from '@capacitor-community/speech-recognition';
import { TextToSpeech } from '@capacitor-community/text-to-speech';

if (Capacitor.isNativePlatform()) {
  window.KK_NATIVE = { SpeechRecognition, TextToSpeech };
}
